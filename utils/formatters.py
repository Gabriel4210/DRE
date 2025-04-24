from datetime import datetime

def formatar_moeda(valor):
    """
    Formata um valor como moeda brasileira (R$).
    
    Args:
        valor: Valor numérico a ser formatado
        
    Returns:
        str: Valor formatado como moeda (ex: R$ 1.234,56)
    """
    if valor is None:
        return "R$ 0,00"
    
    # Garante que o valor é numérico
    try:
        valor_num = float(valor)
    except (ValueError, TypeError):
        return "R$ 0,00"
    
    # Formata o valor
    negativo = valor_num < 0
    valor_abs = abs(valor_num)
    
    # Separa parte inteira e decimal
    parte_inteira = int(valor_abs)
    parte_decimal = int(round((valor_abs - parte_inteira) * 100))
    
    # Formata parte inteira com separadores de milhar
    str_inteira = str(parte_inteira)
    grupos = []
    
    while str_inteira:
        grupos.insert(0, str_inteira[-3:])
        str_inteira = str_inteira[:-3]
    
    # Junta os grupos com ponto
    parte_inteira_formatada = '.'.join(grupos)
    
    # Formata parte decimal
    parte_decimal_formatada = f"{parte_decimal:02d}"
    
    # Monta o resultado final
    sinal = "-" if negativo else ""
    resultado = f"R$ {sinal}{parte_inteira_formatada},{parte_decimal_formatada}"
    
    return resultado

def formatar_data(data, formato_saida='%d/%m/%Y'):
    """
    Formata uma data para o formato especificado.
    
    Args:
        data: Data a ser formatada (string, datetime ou timestamp)
        formato_saida: Formato de saída desejado
        
    Returns:
        str: Data formatada
    """
    if data is None:
        return ""
    
    try:
        # Se for string, tenta converter para datetime
        if isinstance(data, str):
            # Tenta diferentes formatos comuns
            for formato in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S']:
                try:
                    data_dt = datetime.strptime(data, formato)
                    return data_dt.strftime(formato_saida)
                except ValueError:
                    continue
            
            # Se nenhum formato funcionar, retorna a string original
            return data
        
        # Se já for um objeto datetime
        elif isinstance(data, datetime):
            return data.strftime(formato_saida)
        
        # Se for timestamp (int ou float)
        elif isinstance(data, (int, float)):
            return datetime.fromtimestamp(data).strftime(formato_saida)
        
        else:
            return str(data)
    
    except Exception:
        # Em caso de erro, retorna a entrada original como string
        return str(data)
