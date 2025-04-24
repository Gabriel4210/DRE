import locale
from datetime import datetime

# Configura o locale para formatação de moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_moeda(valor):
    """Formata um valor como moeda (R$)"""
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def formatar_data(data_str):
    """Formata uma string de data para o formato dd/mm/yyyy"""
    data = datetime.strptime(data_str, '%Y-%m-%d')
    return data.strftime('%d/%m/%Y')
