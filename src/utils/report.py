from fpdf import FPDF
from fpdf.enums import XPos, YPos
import tempfile
import os

class ReportGenerator:
    """Service dédié à la génération de rapports de simulation."""
    
    @staticmethod
    def generate_pdf(params: dict, figures: list, bench_results: list) -> bytes:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 20)
        pdf.cell(0, 15, "Rapport de Simulation - Alterna Energie", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(5)
        
        # Paramètres
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "1. Configuration de la simulation", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("helvetica", "", 11)
        for k, v in params.items():
            v_text = str(v).replace("€", "EUR")
            pdf.cell(0, 7, f"- {k} : {v_text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5)

        # Graphiques
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "2. Analyse Visuelle", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            for i, fig in enumerate(figures):
                img_path = os.path.join(tmpdir, f"fig_{i}.png")
                fig.write_image(img_path)
                pdf.image(img_path, x=15, w=180)
                pdf.ln(5)
                
        # Benchmarking
        pdf.add_page()
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "3. Positionnement Concurrentiel", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("helvetica", "", 11)
        
        effective_width = pdf.w - 2 * pdf.l_margin
        for line in bench_results:
            clean_line = line.replace("€", "EUR").replace("🟢", "(+) ").replace("🔴", "(-) ").replace("⚪️", "(=) ")
            pdf.multi_cell(w=effective_width, h=8, txt=clean_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)

        return bytes(pdf.output())
