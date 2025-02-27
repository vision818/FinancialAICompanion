import pandas as pd
from typing import Dict, List, Any

def get_risk_profile(age: int, investment_horizon: int, risk_tolerance: str) -> Dict[str, float]:
    """
    Determine investment risk profile based on user inputs
    """
    profiles = {
        'conservative': {
            'Stocks': 30.0,
            'Bonds': 50.0,
            'Cash': 15.0,
            'Other': 5.0
        },
        'moderate': {
            'Stocks': 60.0,
            'Bonds': 30.0,
            'Cash': 5.0,
            'Other': 5.0
        },
        'aggressive': {
            'Stocks': 80.0,
            'Bonds': 15.0,
            'Cash': 2.0,
            'Other': 3.0
        }
    }

    # Basic risk profile determination
    if age > 60 or investment_horizon < 5 or risk_tolerance == 'low':
        return profiles['conservative']
    elif age > 40 or investment_horizon < 10 or risk_tolerance == 'medium':
        return profiles['moderate']
    else:
        return profiles['aggressive']

def get_investment_options() -> Dict[str, Dict[str, float]]:
    """
    Get risk-reward data for different investment options
    """
    return {
        'Government Bonds': {'risk': 1.0, 'return': 3.0},
        'Corporate Bonds': {'risk': 3.0, 'return': 5.0},
        'Blue Chip Stocks': {'risk': 5.0, 'return': 8.0},
        'Index Funds': {'risk': 4.0, 'return': 7.0},
        'Growth Stocks': {'risk': 7.0, 'return': 12.0},
        'Real Estate': {'risk': 6.0, 'return': 9.0},
        'Cryptocurrencies': {'risk': 9.0, 'return': 15.0}
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
        'Clean Energy': 30.0,
        'Sustainable Agriculture': 20.0,
        'Water Conservation': 15.0,
        'Green Buildings': 15.0,
        'Electric Vehicles': 20.0
    }