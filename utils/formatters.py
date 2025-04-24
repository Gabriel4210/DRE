# utils/formatters.py
import locale
from datetime import datetime

# Tenta configurar o locale, mas com fallback seguro
try:
    # Tenta primeiro o locale brasileiro
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except (locale.Error, ValueError):
    try:
        # Tenta uma alternativa comum
        locale.setlocale(locale.LC_ALL, 'pt_BR')
    except (locale.Error, ValueError):
        try:
            # Tenta o locale do sistema
            locale.setlocale(locale.LC_ALL, '')
        except (locale.Error, ValueError):
            # Se tudo falhar, não altera o locale
            pass

def formatar_moeda(valor):
    """Formata um valor como moeda (R$) sem depender do locale"""
    # Implementação manual que não depende do locale
    if valor is None:
        return "R$ 0,00"
    
    # Converte para string com 2 casas decimais
    valor_str = f"{abs(valor):.2f}"
    
    # Separa parte inteira e decimal
    partes = valor_str.split('.')
    parte_inteira = partes[0]
    parte_decimal = partes[1] if len(partes) > 1 else "00"
    
    # Adiciona separadores de milhar
    chars = list(parte_inteira)
    resultado = ""
    for i, char in enumerate(reversed(chars)):
        if i > 0 and i % 3 == 0:
            resultado = "." + resultado
        resultado = char + resultado
    
    # Monta o valor final
    valor_formatado = f"R$ {'-' if valor < 0 else ''}{resultado},{parte_decimal}"
    
    return valor_formatado

def formatar_data(data_str):
    """Formata uma string de data para o formato dd/mm/yyyy"""
    if isinstance(data_str, str):
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d')
            return data.strftime('%d/%m/%Y')
        except ValueError:
            return data_str
    elif isinstance(data_str, datetime):
        return data_str.strftime('%d/%m/%Y')
    else:
        return str(data_str)
