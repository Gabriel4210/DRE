from datetime import datetime

def validar_formulario(empresa, data, tipo, descricao, valor):
    """Valida os campos do formulário de lançamento"""
    if not empresa or empresa == "":
        return False
    
    if not data:
        return False
    
    if not tipo or tipo not in ["Receita", "Custo", "Despesa"]:
        return False
    
    if not descricao or descricao.strip() == "":
        return False
    
    if not valor or valor <= 0:
        return False
    
    return True
