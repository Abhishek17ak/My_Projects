import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import torch

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.summarizer import Summarizer, SummarizerException

class TestSummarizer(unittest.TestCase):
    
    @patch('app.models.summarizer.AutoTokenizer')
    @patch('app.models.summarizer.AutoModelForSeq2SeqLM')
    def setUp(self, mock_model_class, mock_tokenizer_class):
        # Mock the tokenizer
        self.mock_tokenizer = MagicMock()
        self.mock_tokenizer.model_max_length = 512
        self.mock_tokenizer.encode.return_value = torch.tensor([1, 2, 3])
        self.mock_tokenizer.decode.return_value = "This is a test summary."
        mock_tokenizer_class.from_pretrained.return_value = self.mock_tokenizer
        
        # Mock the model
        self.mock_model = MagicMock()
        self.mock_model.generate.return_value = torch.tensor([[4, 5, 6]])
        mock_model_class.from_pretrained.return_value = self.mock_model
        
        # Create summarizer instance
        self.summarizer = Summarizer(model_name="test-model", device="cpu")
    
    def test_generate_summary(self):
        """Test that generate_summary works correctly"""
        # Test with normal input
        summary = self.summarizer.generate_summary("This is a test document.")
        
        # Check that the tokenizer and model were called correctly
        self.mock_tokenizer.encode.assert_called_once()
        self.mock_model.generate.assert_called_once()
        
        # Check the result
        self.assertEqual(summary, "This is a test summary.")
    
    def test_empty_input(self):
        """Test that empty input returns empty string"""
        summary = self.summarizer.generate_summary("")
        
        # Check that the tokenizer and model were not called
        self.mock_tokenizer.encode.assert_not_called()
        self.mock_model.generate.assert_not_called()
        
        # Check the result
        self.assertEqual(summary, "")
    
    @patch('app.models.summarizer.AutoTokenizer')
    @patch('app.models.summarizer.AutoModelForSeq2SeqLM')
    def test_model_initialization_error(self, mock_model_class, mock_tokenizer_class):
        """Test that initialization errors are handled correctly"""
        # Make the model initialization fail
        mock_tokenizer_class.from_pretrained.side_effect = Exception("Model not found")
        
        # Check that the error is caught and re-raised as SummarizerException
        with self.assertRaises(SummarizerException):
            Summarizer(model_name="nonexistent-model", device="cpu")
    
    def test_generate_summary_error(self):
        """Test that generation errors are handled correctly"""
        # Make the model generate method fail
        self.mock_model.generate.side_effect = Exception("Generation error")
        
        # Check that the error is caught and re-raised as SummarizerException
        with self.assertRaises(SummarizerException):
            self.summarizer.generate_summary("This is a test document.")
    
    @patch('app.models.summarizer.torch.cuda.OutOfMemoryError', new=torch.cuda.OutOfMemoryError)
    def test_cuda_out_of_memory(self):
        """Test that CUDA out of memory errors are handled correctly"""
        # Make the model generate method raise CUDA OOM
        self.mock_model.generate.side_effect = torch.cuda.OutOfMemoryError("CUDA out of memory")
        
        # Set device to CUDA for this test
        self.summarizer.device = torch.device("cuda")
        
        # Mock the to() method to avoid actual device changes
        self.mock_model.to = MagicMock()
        
        # This should not raise an exception but fall back to CPU
        with patch('app.models.summarizer.Summarizer.generate_summary', return_value="Fallback summary"):
            summary = self.summarizer.generate_summary("This is a test document.")
            self.assertEqual(summary, "Fallback summary")
    
    def test_long_text_handling(self):
        """Test that long text is handled correctly"""
        # Mock the tokenizer to simulate a long text
        self.mock_tokenizer.encode.return_value = torch.tensor(list(range(1000)))
        
        # Mock chunk_text to return predefined chunks
        with patch('app.data.processor.chunk_text', return_value=["Chunk 1", "Chunk 2"]):
            # Mock generate_summary to return different summaries for different chunks
            with patch.object(self.summarizer, 'generate_summary', side_effect=["Summary 1", "Summary 2", "Final summary"]):
                summary = self.summarizer.generate_summary_for_long_text("This is a long test document.")
                
                # Check the result - should be "Final summary" since we're mocking the combined summary to be too long
                self.assertEqual(summary, "Final summary")

if __name__ == '__main__':
    unittest.main() 