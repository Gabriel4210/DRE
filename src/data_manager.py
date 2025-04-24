import pandas as pd
import os
from datetime import datetime

# Caminho para o arquivo de dados
DATA_PATH = "data/user_data.csv"

def initialize_data():
    """
    Inicializa o arquivo de dados se não existir.
    Retorna um DataFrame vazio ou carrega o existente.
    """
    # Cria o diretório data se não existir
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    
    # Verifica se o arquivo existe
    if not os.path.exists(DATA_PATH):
        # Cria um DataFrame vazio com as colunas necessárias
        df = pd.DataFrame(columns=[
            'id', 'empresa', 'data', 'tipo', 'descricao', 'valor'
        ])
        # Salva o DataFrame vazio como CSV
        df.to_csv(DATA_PATH, index=False)
        return df
    
    # Carrega o arquivo existente
    return pd.read_csv(DATA_PATH)

def add_transaction(empresa, data, tipo, descricao, valor):
    """
    Adiciona uma nova transação ao arquivo de dados.
    
    Args:
        empresa: Nome da empresa
        data: Data da transação (formato YYYY-MM-DD)
        tipo: Tipo da transação (Receita, Custo, Despesa)
        descricao: Descrição da transação
        valor: Valor da transação
        
    Returns:
        int: ID da transação
    """
    # Carrega os dados existentes
    df = pd.read_csv(DATA_PATH)
    
    # Gera ID único baseado no timestamp
    transaction_id = int(datetime.now().timestamp())
    
    # Cria nova linha
    new_row = {
        'id': transaction_id,
        'empresa': empresa,
        'data': data,
        'tipo': tipo,
        'descricao': descricao,
        'valor': valor
    }
    
    # Adiciona ao DataFrame e salva
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    
    return transaction_id

def get_transactions(empresa=None, periodo=None):
    """
    Recupera transações com filtros opcionais.
    
    Args:
        empresa: Nome da empresa para filtrar (opcional)
        periodo: Tuple (data_inicio, data_fim) para filtrar (opcional)
        
    Returns:
        DataFrame: Transações filtradas
    """
    # Carrega os dados
    df = pd.read_csv(DATA_PATH)
    
    # Se não houver dados, retorna DataFrame vazio
    if df.empty:
        return df
    
    # Aplica filtro de empresa
    if empresa:
        df = df[df['empresa'] == empresa]
    
    # Aplica filtro de período
    if periodo and len(periodo) == 2:
        # Converte datas para string se forem objetos datetime
        inicio = periodo[0]
        fim = periodo[1]
        
        if hasattr(inicio, 'strftime'):
            inicio = inicio.strftime('%Y-%m-%d')
        
        if hasattr(fim, 'strftime'):
            fim = fim.strftime('%Y-%m-%d')
        
        df = df[(df['data'] >= inicio) & (df['data'] <= fim)]
    
    return df
