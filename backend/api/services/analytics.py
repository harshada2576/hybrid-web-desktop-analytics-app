"""
Analytics Service Layer for IIT Bombay Analytics Backend.

This module contains all Pandas-based data processing logic.
Views should NEVER contain Pandas code - all analytics logic is centralized here.

Required CSV columns:
    - Equipment Name
    - Type
    - Flowrate (numeric)
    - Pressure (numeric)
    - Temperature (numeric)
"""

import pandas as pd
from typing import Dict, List, Any
from django.core.exceptions import ValidationError


class CSVValidationError(Exception):
    """
    Custom exception for CSV validation errors.
    
    Raised when CSV doesn't meet the required format specifications.
    """
    pass


def validate_csv_format(df: pd.DataFrame) -> None:
    """
    Validate that CSV contains all required columns with correct data types.
    
    Args:
        df: Pandas DataFrame loaded from CSV
        
    Raises:
        CSVValidationError: If validation fails with detailed error message
    """
    # Define required columns
    required_columns = [
        'Equipment Name',
        'Type',
        'Flowrate',
        'Pressure',
        'Temperature'
    ]
    
    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise CSVValidationError(
            f"Missing required columns: {', '.join(missing_columns)}. "
            f"Required columns are: {', '.join(required_columns)}"
        )
    
    # Validate numeric columns
    numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
    
    for col in numeric_columns:
        # Try to convert to numeric
        try:
            # Use pd.to_numeric with errors='coerce' to find non-numeric values
            converted = pd.to_numeric(df[col], errors='coerce')
            
            # Check if any values couldn't be converted (became NaN)
            if converted.isna().any() and not df[col].isna().all():
                # Find the problematic rows
                invalid_mask = converted.isna() & df[col].notna()
                invalid_values = df.loc[invalid_mask, col].head(3).tolist()
                
                raise CSVValidationError(
                    f"Column '{col}' must contain only numeric values. "
                    f"Found invalid values: {invalid_values}"
                )
        except Exception as e:
            if isinstance(e, CSVValidationError):
                raise
            raise CSVValidationError(
                f"Error validating column '{col}': {str(e)}"
            )


def compute_summary_statistics(file_path: str) -> Dict[str, Any]:
    """
    Compute summary statistics from uploaded CSV file.
    
    This is the main analytics function that:
    1. Loads CSV using Pandas
    2. Validates format and data types
    3. Computes all required statistics
    4. Returns clean JSON-serializable dictionary
    
    Args:
        file_path: Absolute path to the CSV file
        
    Returns:
        Dictionary containing:
            - total_equipment: Total number of equipment entries
            - average_flowrate: Mean flowrate
            - average_pressure: Mean pressure
            - average_temperature: Mean temperature
            - equipment_distribution: List of dicts with type counts
            
    Raises:
        CSVValidationError: If CSV format is invalid
        Exception: For other file/processing errors
    """
    try:
        # Load CSV with Pandas
        df = pd.read_csv(file_path)
        
        # Validate CSV format
        validate_csv_format(df)
        
        # Compute statistics
        total_equipment = len(df)
        
        # Convert numeric columns to proper numeric type
        df['Flowrate'] = pd.to_numeric(df['Flowrate'], errors='coerce')
        df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')
        df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
        
        # Compute averages (handle NaN values)
        average_flowrate = float(df['Flowrate'].mean())
        average_pressure = float(df['Pressure'].mean())
        average_temperature = float(df['Temperature'].mean())
        
        # Compute equipment type distribution
        type_counts = df['Type'].value_counts()
        equipment_distribution = [
            {'type': str(type_name), 'count': int(count)}
            for type_name, count in type_counts.items()
        ]
        
        # Return clean dictionary
        return {
            'total_equipment': total_equipment,
            'average_flowrate': round(average_flowrate, 2),
            'average_pressure': round(average_pressure, 2),
            'average_temperature': round(average_temperature, 2),
            'equipment_distribution': equipment_distribution
        }
        
    except CSVValidationError:
        # Re-raise validation errors as-is
        raise
    except FileNotFoundError:
        raise CSVValidationError(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise CSVValidationError("CSV file is empty")
    except pd.errors.ParserError as e:
        raise CSVValidationError(f"Error parsing CSV file: {str(e)}")
    except Exception as e:
        raise CSVValidationError(f"Error processing CSV: {str(e)}")


def get_equipment_distribution(file_path: str) -> List[Dict[str, Any]]:
    """
    Get equipment type distribution from CSV file.
    
    Args:
        file_path: Absolute path to the CSV file
        
    Returns:
        List of dictionaries with 'type' and 'count' keys
        
    Raises:
        CSVValidationError: If CSV format is invalid
    """
    try:
        df = pd.read_csv(file_path)
        validate_csv_format(df)
        
        # Compute type distribution
        type_counts = df['Type'].value_counts()
        
        return [
            {'type': str(type_name), 'count': int(count)}
            for type_name, count in type_counts.items()
        ]
        
    except CSVValidationError:
        raise
    except Exception as e:
        raise CSVValidationError(f"Error processing CSV: {str(e)}")
