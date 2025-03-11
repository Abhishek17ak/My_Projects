import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import app
from app.models.summarizer import SummarizerException

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    @patch('app.api.get_summarizer')
    def test_summarize_endpoint(self, mock_get_summarizer):
        """Test the summarize endpoint with valid input"""
        # Mock the summarizer
        mock_summarizer = MagicMock()
        mock_summarizer.generate_summary_for_long_text.return_value = "This is a test summary."
        mock_get_summarizer.return_value = mock_summarizer
        
        # Mock the database operations
        with patch('app.api.get_session') as mock_get_session:
            mock_session = MagicMock()
            mock_get_session.return_value = mock_session
            
            # Mock the TextChunk
            mock_chunk = MagicMock()
            mock_chunk.id = 1
            mock_session.add.return_value = None
            mock_session.commit.return_value = None
            
            with patch('app.api.TextChunk', return_value=mock_chunk):
                with patch('app.api.store_summary') as mock_store_summary:
                    # Test the API endpoint
                    response = self.app.post(
                        '/summarizer/summarize',
                        headers={"X-API-Key": "your_api_key_1", "Content-Type": "application/json"},
                        json={"text": "This is a test document that needs to be summarized." * 20}
                    )
                    
                    # Check the response
                    self.assertEqual(response.status_code, 200)
                    data = json.loads(response.data)
                    self.assertEqual(data["summary"], "This is a test summary.")
                    self.assertTrue("original_length" in data)
                    self.assertTrue("summary_length" in data)
                    self.assertTrue("processing_time" in data)
                    
                    # Check that the summarizer was called correctly
                    mock_summarizer.generate_summary_for_long_text.assert_called_once()
                    
                    # Check that the database operations were called
                    mock_session.add.assert_called_once()
                    mock_session.commit.assert_called_once()
                    mock_store_summary.assert_called_once()
    
    def test_unauthorized_access(self):
        """Test that unauthorized access is rejected"""
        # Test without API key
        response = self.app.post(
            '/summarizer/summarize',
            json={"text": "This is a test."}
        )
        self.assertEqual(response.status_code, 401)
        
        # Test with invalid API key
        response = self.app.post(
            '/summarizer/summarize',
            headers={"X-API-Key": "invalid_key"},
            json={"text": "This is a test."}
        )
        self.assertEqual(response.status_code, 401)
    
    @patch('app.api.get_summarizer')
    def test_input_validation(self, mock_get_summarizer):
        """Test that input validation works correctly"""
        # Test with empty text
        response = self.app.post(
            '/summarizer/summarize',
            headers={"X-API-Key": "your_api_key_1", "Content-Type": "application/json"},
            json={"text": ""}
        )
        self.assertEqual(response.status_code, 400)
        
        # Test with text that's too short
        response = self.app.post(
            '/summarizer/summarize',
            headers={"X-API-Key": "your_api_key_1", "Content-Type": "application/json"},
            json={"text": "Short text."}
        )
        self.assertEqual(response.status_code, 400)
        
        # Test with invalid parameters
        response = self.app.post(
            '/summarizer/summarize',
            headers={"X-API-Key": "your_api_key_1", "Content-Type": "application/json"},
            json={"text": "This is a test document that needs to be summarized." * 20, "max_length": -10}
        )
        self.assertEqual(response.status_code, 400)
    
    @patch('app.api.get_summarizer')
    def test_summarizer_exception(self, mock_get_summarizer):
        """Test that summarizer exceptions are handled correctly"""
        # Mock the summarizer to raise an exception
        mock_summarizer = MagicMock()
        mock_summarizer.generate_summary_for_long_text.side_effect = SummarizerException("Test error")
        mock_get_summarizer.return_value = mock_summarizer
        
        # Test the API endpoint
        response = self.app.post(
            '/summarizer/summarize',
            headers={"X-API-Key": "your_api_key_1", "Content-Type": "application/json"},
            json={"text": "This is a test document that needs to be summarized." * 20}
        )
        
        # Check only the status code
        self.assertEqual(response.status_code, 500)
    
    def test_health_check(self):
        """Test the health check endpoint"""
        # Mock the database and summarizer checks
        with patch('app.api.get_session') as mock_get_session:
            mock_session = MagicMock()
            mock_session.execute.return_value = True
            mock_get_session.return_value = mock_session
            
            with patch('app.api.get_summarizer') as mock_get_summarizer:
                mock_summarizer = MagicMock()
                mock_get_summarizer.return_value = mock_summarizer
                
                # Test the health check endpoint
                response = self.app.get('/health')
                
                # Check the response
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertEqual(data["status"], "healthy")
                self.assertEqual(data["database"], "healthy")
                self.assertEqual(data["model"], "healthy")

if __name__ == '__main__':
    unittest.main() 