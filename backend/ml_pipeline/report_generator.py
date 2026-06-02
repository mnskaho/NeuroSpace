from fpdf import FPDF
import matplotlib.pyplot as plt
from datetime import datetime
import os
import io
import base64

class PDFReport(FPDF):
    """PDF Report generator for NeuroSpace"""
    
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'NeuroSpace - Rapport d\'entraînement', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, text)
        self.ln()

    def add_plot(self, img_path, w=180):
        if os.path.exists(img_path):
            self.image(img_path, x=10, w=w)
            self.ln(5)

def generate_report(job_id, output_dir, model_names, metrics, class_names, plot_paths):
    """Génère un rapport PDF complet"""
    pdf = PDFReport()
    pdf.add_page()
    
    # Informations générales
    pdf.chapter_title("Informations du job")
    pdf.chapter_body(f"Job ID: {job_id}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Métriques
    pdf.chapter_title("Résultats des modèles")
    for model in model_names:
        if model in metrics:
            m = metrics[model]
            pdf.chapter_body(
                f"{model.upper()}:\n"
                f"- Accuracy: {m.get('accuracy', 0):.4f}\n"
                f"- F1 Score: {m.get('f1_score', 0):.4f}\n"
                f"- Precision: {m.get('precision', 0):.4f}\n"
                f"- Recall: {m.get('recall', 0):.4f}"
            )
    
    # Comparaison
    if 'comparison' in plot_paths and os.path.exists(plot_paths['comparison']):
        pdf.add_page()
        pdf.chapter_title("Comparaison des modèles")
        pdf.add_plot(plot_paths['comparison'])
    
    # Courbes d'entraînement
    for model in model_names:
        key = f'{model}_curves'
        if key in plot_paths and os.path.exists(plot_paths[key]):
            pdf.add_page()
            pdf.chapter_title(f"Courbes d'entraînement - {model.upper()}")
            pdf.add_plot(plot_paths[key])
    
    # Matrices de confusion
    for model in model_names:
        key = f'{model}_cm'
        if key in plot_paths and os.path.exists(plot_paths[key]):
            pdf.add_page()
            pdf.chapter_title(f"Matrice de confusion - {model.upper()}")
            pdf.add_plot(plot_paths[key])
    
    # Sauvegarde
    pdf_path = os.path.join(output_dir, f"{job_id}_report.pdf")
    pdf.output(pdf_path)
    return pdf_path

def figure_to_base64(fig):
    """Convertit une figure matplotlib en base64 pour l'API"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')