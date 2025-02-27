import pandas as pd
from typing import Dict, List, Any

def get_risk_profile(age: int, investment_horizon: int, risk_tolerance: str) -> str:
    """
    Determine investment risk profile based on user inputs
    """
    profiles = {
        'conservative': {
            'stocks': 30,
            'bonds': 50,
            'cash': 15,
            'other': 5
        },
        'moderate': {
            'stocks': 60,
            'bonds': 30,
            'cash': 5,
            'other': 5
        },
        'aggressive': {
            'stocks': 80,
            'bonds': 15,
            'cash': 2,
            'other': 3
        }
    }
    
    # Basic risk profile determination
    if age > 60 or investment_horizon < 5 or risk_tolerance == 'low':
        return profiles['conservative']
    elif age > 40 or investment_horizon < 10 or risk_tolerance == 'medium':
        return profiles['moderate']
    else:
        return profiles['aggressive']

def get_investment_options() -> Dict[str, Dict[float, float]]:
    """
    Get risk-reward data for different investment options
    """
    return {
        'Government Bonds': {'risk': 1, 'return': 3},
        'Corporate Bonds': {'risk': 3, 'return': 5},
        'Blue Chip Stocks': {'risk': 5, 'return': 8},
        'Index Funds': {'risk': 4, 'return': 7},
        'Growth Stocks': {'risk': 7, 'return': 12},
        'Real Estate': {'risk': 6, 'return': 9},
        'Cryptocurrencies': {'risk': 9, 'return': 15}
    }

def create_investment_timeline_data(initial_amount: float, years: int) -> List[Dict[str, Any]]:
    """
    Create investment timeline goals
    """
    goals = []
    current_amount = initial_amount
    
    for year in range(5, years + 1, 5):
        # Compound growth calculation (simplified)
        current_amount *= (1.07 ** 5)  # Assuming 7% annual return
        goals.append({
            'year': 2025 + year,
            'amount': round(current_amount, 2),
            'description': f'Year {year}: ${round(current_amount/1000, 1)}K'
        })
    
    return goals

def get_sustainable_investments() -> Dict[str, float]:
    """
    Get allocation for sustainable investment portfolio
    """
    return {
        'Clean Energy': 30,
        'Sustainable Agriculture': 20,
        'Water Conservation': 15,
        'Green Buildings': 15,
        'Electric Vehicles': 20
    }
