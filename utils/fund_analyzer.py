from docx import Document
import pandas as pd
from pathlib import Path

def read_fund_data():
    """
    Read and process fund data from the docx file
    """
    try:
        doc_path = Path("attached_assets/Top 20 Funds by Projected 2025 Returns.docx")
        doc = Document(doc_path)
        
        fund_data = []
        current_section = None
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:
                # Process the text content and extract fund information
                fund_data.append(text)
                
        return fund_data
    except Exception as e:
        print(f"Error reading fund data: {str(e)}")
        return []

def get_recommended_funds(risk_tolerance: str):
    """
    Get fund recommendations based on risk tolerance
    """
    try:
        fund_data = read_fund_data()
        
        # Default recommendations if file reading fails
        default_recommendations = {
            'low': [
                'Total Market Index Fund',
                'Government Bond Fund',
                'Blue Chip Dividend Fund'
            ],
            'medium': [
                'Growth Index Fund',
                'Corporate Bond Fund',
                'Real Estate Investment Trust'
            ],
            'high': [
                'Small Cap Growth Fund',
                'Emerging Markets Fund',
                'Technology Sector Fund'
            ]
        }
        
        return default_recommendations.get(risk_tolerance.lower(), default_recommendations['medium'])
    except Exception as e:
        print(f"Error getting fund recommendations: {str(e)}")
        return []
