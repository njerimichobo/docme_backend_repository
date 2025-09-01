from weasyprint import HTML
import os


def generate_report_pdf(patient_name, diagnosis, recommendations, report_id):
    html = f"""
    <html><body style="font-family:sans-serif;">
        <h1>Medical Blood Test Report</h1>
        <p><strong>Patient:</strong> {patient_name}</p>
        <p><strong>Diagnosis:</strong> {diagnosis}</p>
        <p><strong>Recommendations:</strong> {recommendations}</p>
    </body></html>
    """
    output_path = f"reports_output/report_{report_id}.pdf"
    HTML(string=html).write_pdf(output_path)
    return output_path
