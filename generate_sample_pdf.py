"""
Generate Sample PDF Report

This script generates a sample analytical report for demonstration purposes.
Run this after setting up the backend and uploading sample data.
"""

import os
import sys
from datetime import datetime

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from api.services.pdf_generator import generate_analytics_report


def create_sample_report():
    """Generate a sample PDF report with demo data."""
    
    # Sample data matching the sample CSV
    sample_summary = {
        'total_equipment': 10,
        'average_flowrate': 125.45,
        'average_pressure': 850.30,
        'average_temperature': 75.20,
        'equipment_distribution': [
            {'type': 'Pump', 'count': 4},
            {'type': 'Valve', 'count': 3},
            {'type': 'Compressor', 'count': 3}
        ]
    }
    
    # Generate PDF
    print("Generating sample PDF report...")
    
    pdf_buffer = generate_analytics_report(
        dataset_filename='sample_equipment_data.csv',
        upload_timestamp=datetime.now().isoformat(),
        summary=sample_summary,
        distribution=sample_summary['equipment_distribution']
    )
    
    # Save to sample_reports folder
    output_path = os.path.join(
        os.path.dirname(__file__),
        'sample_reports',
        'sample_analysis_report.pdf'
    )
    
    with open(output_path, 'wb') as f:
        f.write(pdf_buffer.getvalue())
    
    print(f"✓ Sample report generated: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    print("\nYou can now open this PDF to verify the report generation functionality.")


if __name__ == '__main__':
    try:
        create_sample_report()
    except Exception as e:
        print(f"Error generating report: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure you're in the project root directory")
        print("2. Install backend dependencies: cd backend && pip install -r requirements.txt")
        print("3. Run migrations: cd backend && python manage.py migrate")
        sys.exit(1)
