import requests
import time
from bs4 import BeautifulSoup
import hashlib
from ..utils.logging import logger, log_performance
from ..config import config

class SECEdgarException(Exception):
    """Exception raised for SEC EDGAR API errors"""
    pass

@log_performance(logger)
def fetch_10k_filing(ticker, year, max_retries=None, timeout=None):
    """
    Fetch 10-K filing for a company from SEC EDGAR
    
    Args:
        ticker (str): Company ticker symbol
        year (int): Year of filing
        max_retries (int, optional): Maximum number of retry attempts
        timeout (int, optional): Request timeout in seconds
        
    Returns:
        str: Text content of the 10-K filing or None if not found
        
    Raises:
        SECEdgarException: If there's an error with the SEC EDGAR API
    """
    # Get configuration values
    sec_config = config["sec_edgar"]
    max_retries = max_retries or sec_config["max_retries"]
    timeout = timeout or sec_config["timeout"]
    backoff_factor = sec_config["backoff_factor"]
    user_agent = sec_config["user_agent"]
    
    logger.info(f"Fetching 10-K filing for {ticker} ({year})")
    
    for attempt in range(max_retries):
        try:
            # Base URL for SEC EDGAR search
            base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
            
            # Parameters for the request
            params = {
                'action': 'getcompany',
                'CIK': ticker,
                'type': '10-K',
                'dateb': f'{year}1231',
                'owner': 'exclude',
                'count': '10'
            }
            
            # Send request to SEC EDGAR with timeout
            response = requests.get(
                base_url, 
                params=params, 
                headers={'User-Agent': user_agent},
                timeout=timeout
            )
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Parse the response
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the link to the 10-K filing
            filing_links = soup.find_all('a', {'id': 'documentsbutton'})
            
            if not filing_links:
                logger.warning(f"No 10-K filing found for {ticker} ({year})")
                return None
            
            filing_url = 'https://www.sec.gov' + filing_links[0]['href']
            
            # Add delay to be nice to SEC servers
            time.sleep(1)
            
            # Get the filing document page
            filing_response = requests.get(
                filing_url, 
                headers={'User-Agent': user_agent},
                timeout=timeout
            )
            filing_response.raise_for_status()
            
            filing_soup = BeautifulSoup(filing_response.content, 'html.parser')
            
            # Find the actual text file
            text_links = filing_soup.find_all('a', {'href': lambda x: x and x.endswith('.htm') and not x.endswith('_index.htm')})
            
            if not text_links:
                logger.warning(f"No text document found in 10-K filing for {ticker} ({year})")
                return None
            
            text_url = 'https://www.sec.gov' + text_links[0]['href']
            
            # Add delay to be nice to SEC servers
            time.sleep(1)
            
            # Get the text content
            text_response = requests.get(
                text_url, 
                headers={'User-Agent': user_agent},
                timeout=timeout
            )
            text_response.raise_for_status()
            
            # Parse the text content
            document_soup = BeautifulSoup(text_response.content, 'html.parser')
            
            # Extract text
            text = document_soup.get_text()
            
            logger.info(f"Successfully fetched 10-K filing for {ticker} ({year}), size: {len(text)} characters")
            return text
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to fetch filing for {ticker} after {max_retries} attempts: {str(e)}")
                raise SECEdgarException(f"Failed to fetch filing: {str(e)}")
            
            # Calculate backoff time with exponential backoff
            backoff_time = backoff_factor ** attempt
            logger.warning(f"Attempt {attempt+1} failed, retrying in {backoff_time:.1f}s: {str(e)}")
            time.sleep(backoff_time)
            
        except Exception as e:
            logger.error(f"Unexpected error processing {ticker}: {str(e)}")
            raise SECEdgarException(f"Unexpected error: {str(e)}")

@log_performance(logger)
def fetch_multiple_filings(tickers, years):
    """
    Fetch multiple 10-K filings for a list of companies and years
    
    Args:
        tickers (list): List of company ticker symbols
        years (list): List of years
        
    Returns:
        list: List of dictionaries with ticker, year, and text
    """
    collected_data = []
    
    for ticker in tickers:
        for year in years:
            try:
                filing_text = fetch_10k_filing(ticker, year)
                
                if filing_text:
                    # Generate a hash of the content for identification
                    content_hash = hashlib.sha256(filing_text.encode()).hexdigest()
                    
                    collected_data.append({
                        'ticker': ticker,
                        'year': year,
                        'text': filing_text,
                        'content_hash': content_hash
                    })
                
                # Be nice to SEC servers
                time.sleep(2)
                
            except SECEdgarException as e:
                logger.error(f"Error fetching {ticker} ({year}): {str(e)}")
                continue
    
    logger.info(f"Fetched {len(collected_data)} filings in total")
    return collected_data 