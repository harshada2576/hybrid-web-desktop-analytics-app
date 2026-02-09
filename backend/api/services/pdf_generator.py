"""
PDF Report Generation Service for IIT Bombay Analytics Backend.

Generates structured analytical reports with:
- Title section
- Context explanation
- Summary statistics table
- Distribution visualization
- Footer with metadata
"""

import io
from datetime import datetime
from typing import Dict, Any, List

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class PDFReportGenerator:
    """
    Generate analytical PDF reports from dataset analytics.
    
    Academic-style formatting with clear sections and professional layout.
    """
    
    def __init__(self):
        """Initialize PDF generator with standard page settings."""
        self.page_width, self.page_height = letter
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Define custom paragraph styles for the report."""
        # Title style
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ))
        
        # Subtitle style
        if 'CustomSubtitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomSubtitle',
                parent=self.styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#555555'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica'
            ))
        
        # Section heading style
        if 'SectionHeading' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionHeading',
                parent=self.styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=10,
                spaceBefore=15,
                fontName='Helvetica-Bold'
            ))
        
        # Body text style
        if 'BodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='BodyText',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#333333'),
                spaceAfter=10,
                alignment=TA_LEFT,
                fontName='Helvetica'
            ))
    
    def generate_report(
        self, 
        dataset_filename: str,
        upload_timestamp: str,
        summary: Dict[str, Any],
        distribution: List[Dict[str, Any]]
    ) -> io.BytesIO:
        """
        Generate complete PDF report.
        
        Args:
            dataset_filename: Original CSV filename
            upload_timestamp: ISO format timestamp
            summary: Summary statistics dictionary
            distribution: Equipment type distribution list
            
        Returns:
            BytesIO buffer containing PDF data
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build document content
        story = []
        
        # Title section
        story.extend(self._create_title_section(dataset_filename, upload_timestamp))
        
        # Context section
        story.extend(self._create_context_section())
        
        # Summary statistics section
        story.extend(self._create_summary_section(summary))
        
        # Distribution chart section
        story.extend(self._create_distribution_section(distribution))
        
        # Footer
        story.extend(self._create_footer())
        
        # Build PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer
    
    def _create_title_section(
        self, 
        dataset_filename: str, 
        upload_timestamp: str
    ) -> List:
        """Create title page section."""
        elements = []
        
        # Main title
        title = Paragraph(
            "Equipment Analytics Report",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Subtitle with metadata
        try:
            dt = datetime.fromisoformat(upload_timestamp.replace('Z', '+00:00'))
            formatted_date = dt.strftime('%B %d, %Y at %I:%M %p')
        except:
            formatted_date = upload_timestamp
        
        subtitle_text = f"""
        <b>Dataset:</b> {dataset_filename}<br/>
        <b>Generated:</b> {formatted_date}
        """
        subtitle = Paragraph(subtitle_text, self.styles['CustomSubtitle'])
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_context_section(self) -> List:
        """Create context explanation section."""
        elements = []
        
        # Section heading
        heading = Paragraph("Report Overview", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Context paragraph
        context_text = """
        This report presents a comprehensive statistical analysis of equipment data 
        uploaded to the IIT Bombay Analytics system. The analysis includes summary 
        statistics (mean values and counts) as well as distribution patterns across 
        equipment types. All calculations are performed using the Pandas data processing 
        library to ensure accuracy and reliability.
        """
        context = Paragraph(context_text, self.styles['BodyText'])
        elements.append(context)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_summary_section(self, summary: Dict[str, Any]) -> List:
        """Create summary statistics table section."""
        elements = []
        
        # Section heading
        heading = Paragraph("Summary Statistics", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Create table data
        table_data = [
            ['Metric', 'Value'],
            ['Total Equipment', str(summary.get('total_equipment', 0))],
            ['Average Flowrate', f"{summary.get('average_flowrate', 0):.2f}"],
            ['Average Pressure', f"{summary.get('average_pressure', 0):.2f}"],
            ['Average Temperature', f"{summary.get('average_temperature', 0):.2f}"]
        ]
        
        # Create table
        table = Table(table_data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_distribution_section(self, distribution: List[Dict[str, Any]]) -> List:
        """Create distribution chart section."""
        elements = []
        
        # Section heading
        heading = Paragraph("Equipment Type Distribution", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Generate chart
        if distribution:
            chart_buffer = self._generate_distribution_chart(distribution)
            
            # Add chart image to PDF
            img = Image(chart_buffer, width=5*inch, height=3*inch)
            elements.append(img)
        else:
            # No data available
            no_data = Paragraph(
                "No distribution data available.",
                self.styles['BodyText']
            )
            elements.append(no_data)
        
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _generate_distribution_chart(self, distribution: List[Dict[str, Any]]) -> io.BytesIO:
        """
        Generate matplotlib bar chart for equipment distribution.
        
        Args:
            distribution: List of {type, count} dictionaries
            
        Returns:
            BytesIO buffer containing PNG image data
        """
        # Extract data
        types = [item['type'] for item in distribution]
        counts = [item['count'] for item in distribution]
        
        # Create figure
        fig = Figure(figsize=(6, 3.5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Create bar chart
        bars = ax.bar(types, counts, color='steelblue', alpha=0.7, edgecolor='navy')
        
        # Customize chart
        ax.set_xlabel('Equipment Type', fontsize=10, fontweight='bold')
        ax.set_ylabel('Count', fontsize=10, fontweight='bold')
        ax.set_title('Distribution by Equipment Type', fontsize=11, fontweight='bold', pad=10)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Rotate x-axis labels if needed
        if len(types) > 3:
            ax.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., 
                height,
                f'{int(height)}',
                ha='center', 
                va='bottom',
                fontsize=9
            )
        
        fig.tight_layout()
        
        # Save to buffer
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        
        # Close figure to free memory
        plt.close(fig)
        
        return buffer
    
    def _create_footer(self) -> List:
        """Create report footer with metadata."""
        elements = []
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Divider line
        line_data = [['', '']]
        line = Table(line_data, colWidths=[6*inch])
        line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.grey)
        ]))
        elements.append(line)
        elements.append(Spacer(1, 0.1*inch))
        
        # Footer text
        footer_text = f"""
        <i>Report generated by IIT Bombay Analytics System<br/>
        Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i>
        """
        footer = Paragraph(footer_text, self.styles['CustomSubtitle'])
        elements.append(footer)
        
        return elements


def generate_analytics_report(
    dataset_filename: str,
    upload_timestamp: str,
    summary: Dict[str, Any],
    distribution: List[Dict[str, Any]]
) -> io.BytesIO:
    """
    Convenience function to generate PDF report.
    
    Args:
        dataset_filename: Original CSV filename
        upload_timestamp: ISO format timestamp
        summary: Summary statistics
        distribution: Equipment distribution data
        
    Returns:
        BytesIO buffer with PDF data
    """
    generator = PDFReportGenerator()
    return generator.generate_report(
        dataset_filename,
        upload_timestamp,
        summary,
        distribution
    )
