from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import os
from ..config import config
from ..utils.logging import logger

# Create database directory if it doesn't exist
db_path = config["database"]["url"]
if db_path.startswith("sqlite:///"):
    db_file = db_path.replace("sqlite:///", "")
    db_dir = os.path.dirname(db_file)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

# Database setup
engine = create_engine(config["database"]["url"])
Base = declarative_base()
Session = sessionmaker(bind=engine)

class FinancialReport(Base):
    """Model for storing financial reports"""
    __tablename__ = 'financial_reports'
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String(10), nullable=False)
    year = Column(Integer, nullable=False)
    filing_type = Column(String(10), nullable=False)
    content_hash = Column(String(64), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship to sections
    sections = relationship("ReportSection", back_populates="report", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<FinancialReport(ticker='{self.ticker}', year={self.year})>"

class ReportSection(Base):
    """Model for storing sections of financial reports"""
    __tablename__ = 'report_sections'
    
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('financial_reports.id'), nullable=False)
    section_name = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship to report
    report = relationship("FinancialReport", back_populates="sections")
    
    # Relationship to chunks
    chunks = relationship("TextChunk", back_populates="section", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ReportSection(report_id={self.report_id}, section_name='{self.section_name}')>"

class TextChunk(Base):
    """Model for storing chunks of text from report sections"""
    __tablename__ = 'text_chunks'
    
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey('report_sections.id'), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship to section
    section = relationship("ReportSection", back_populates="chunks")
    
    # Relationship to summaries
    summaries = relationship("Summary", back_populates="chunk", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<TextChunk(section_id={self.section_id}, chunk_index={self.chunk_index})>"

class Summary(Base):
    """Model for storing generated summaries"""
    __tablename__ = 'summaries'
    
    id = Column(Integer, primary_key=True)
    chunk_id = Column(Integer, ForeignKey('text_chunks.id'), nullable=False)
    summary_text = Column(Text, nullable=False)
    max_length = Column(Integer, nullable=False)
    min_length = Column(Integer, nullable=False)
    model_version = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship to chunk
    chunk = relationship("TextChunk", back_populates="summaries")
    
    def __repr__(self):
        return f"<Summary(chunk_id={self.chunk_id}, model_version='{self.model_version}')>"

def init_db():
    """Initialize the database by creating all tables"""
    try:
        Base.metadata.create_all(engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def get_session():
    """Get a new database session"""
    return Session()

def store_report(ticker, year, filing_type, content, content_hash=None):
    """
    Store a financial report in the database
    
    Args:
        ticker (str): Company ticker symbol
        year (int): Year of filing
        filing_type (str): Type of filing (e.g., '10-K')
        content (str): Text content of the report
        content_hash (str, optional): Hash of the content
        
    Returns:
        FinancialReport: The created report object
    """
    if content_hash is None:
        import hashlib
        content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    session = get_session()
    try:
        # Check if report already exists
        existing_report = session.query(FinancialReport).filter_by(
            content_hash=content_hash
        ).first()
        
        if existing_report:
            logger.info(f"Report for {ticker} ({year}) already exists in database")
            session.close()
            return existing_report
        
        # Create new report
        report = FinancialReport(
            ticker=ticker,
            year=year,
            filing_type=filing_type,
            content=content,
            content_hash=content_hash
        )
        
        session.add(report)
        session.commit()
        
        logger.info(f"Stored report for {ticker} ({year}) in database")
        return report
    
    except Exception as e:
        session.rollback()
        logger.error(f"Error storing report for {ticker} ({year}): {str(e)}")
        raise
    
    finally:
        session.close()

def store_summary(chunk_id, summary_text, max_length, min_length, model_version):
    """
    Store a generated summary in the database
    
    Args:
        chunk_id (int): ID of the text chunk
        summary_text (str): Generated summary
        max_length (int): Maximum length parameter
        min_length (int): Minimum length parameter
        model_version (str): Version of the model used
        
    Returns:
        Summary: The created summary object
    """
    session = get_session()
    try:
        # Check if summary already exists
        existing_summary = session.query(Summary).filter_by(
            chunk_id=chunk_id,
            max_length=max_length,
            min_length=min_length,
            model_version=model_version
        ).first()
        
        if existing_summary:
            logger.info(f"Summary for chunk {chunk_id} already exists in database")
            session.close()
            return existing_summary
        
        # Create new summary
        summary = Summary(
            chunk_id=chunk_id,
            summary_text=summary_text,
            max_length=max_length,
            min_length=min_length,
            model_version=model_version
        )
        
        session.add(summary)
        session.commit()
        
        logger.info(f"Stored summary for chunk {chunk_id} in database")
        return summary
    
    except Exception as e:
        session.rollback()
        logger.error(f"Error storing summary for chunk {chunk_id}: {str(e)}")
        raise
    
    finally:
        session.close() 