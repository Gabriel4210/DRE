from datetime import datetime

def validar_formulario(empresa, data, tipo, descricao, valor):
    """
    Valida os campos do formulário de lançamento.
    
    Args:
        empresa: Nome da empresa
        data: Data da transação
        tipo: Tipo da transação
        descricao: Descrição da transação
        valor: Valor da transação
        
    Returns:
        bool: True se todos os campos são válidos, False caso contrário
    """
    # Valida empresa
    if not empresa or empresa.strip() == "":
        return False
    
    # Valida data
    if not data:
        return False
    
    # Valida tipo
    if not tipo or tipo not in ["Receita", "Custo", "Despesa"]:
        return False
    
    # Valida descrição
    if not descricao or descricao.strip() == "":
        return False
    
    # Valida valor
    if not valor or valor <= 0:
        return False
    
    return True
