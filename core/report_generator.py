# core/report_generator.py

from fpdf import FPDF
import pandas as pd
import datetime

class PDFReport(FPDF):
    def header(self):
        # Título / Logo (Texto simples por enquanto)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'CardioGuardian - Relatorio de Monitoramento', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        # Rodapé com número da página
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def generate_pdf(df: pd.DataFrame, profile: dict):
    """
    Gera o binário de um arquivo PDF com as estatísticas do DataFrame.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # --- 1. Cabeçalho do Relatório ---
    # Data de Geração
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(0, 10, f"Gerado em: {now}", 0, 1, 'R')
    pdf.ln(5)

    # --- 2. Dados do Paciente ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "Dados do Paciente", 0, 1)
    pdf.set_font('Arial', '', 12)
    
    name = profile.get('name', 'N/A')
    age = profile.get('age', 'N/A')
    conditions = profile.get('conditions', 'N/A')
    
    pdf.cell(0, 8, f"Nome: {name}", 0, 1)
    pdf.cell(0, 8, f"Idade: {age} anos", 0, 1)
    pdf.cell(0, 8, f"Condicoes Clinicas: {conditions}", 0, 1)
    pdf.ln(10)

    # --- 3. Estatísticas do Período ---
    # Cálculos simples com Pandas
    avg_bpm = df['bpm'].mean()
    max_bpm = df['bpm'].max()
    min_bpm = df['bpm'].min()
    total_readings = len(df)
    # Conta quantas vezes a anomalia foi -1
    total_anomalies = df[df['anomaly'] == -1].shape[0]

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "Resumo Estatistico (Historico Recente)", 0, 1)
    pdf.set_font('Arial', '', 12)

    pdf.cell(0, 8, f"Total de Leituras: {total_readings}", 0, 1)
    pdf.cell(0, 8, f"BPM Medio: {avg_bpm:.1f}", 0, 1)
    pdf.cell(0, 8, f"BPM Maximo: {max_bpm}", 0, 1)
    pdf.cell(0, 8, f"BPM Minimo: {min_bpm}", 0, 1)
    
    # Destaque para anomalias
    if total_anomalies > 0:
        pdf.set_text_color(255, 0, 0) # Vermelho
        pdf.cell(0, 8, f"Anomalias Detectadas: {total_anomalies}", 0, 1)
        pdf.set_text_color(0, 0, 0)   # Volta para Preto
    else:
        pdf.set_text_color(0, 128, 0) # Verde
        pdf.cell(0, 8, "Nenhuma anomalia detectada no periodo.", 0, 1)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(10)
    
    # --- 4. Aviso Legal ---
    pdf.set_font('Arial', 'I', 10)
    pdf.multi_cell(0, 5, "Nota: Este relatorio foi gerado automaticamente pelo sistema CardioGuardian baseados nos dados coletados pelo biossensor. Consulte um medico para diagnostico clinico.")

    # Retorna o conteúdo do PDF como string binária (para download)
    return pdf.output(dest='S').encode('latin-1')