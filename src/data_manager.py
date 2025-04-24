import pandas as pd
import os
from datetime import datetime

DATA_PATH = "data/user_data.csv"

def initialize_data():
    """Cria o arquivo CSV se não existir ou carrega o existente"""
    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=[
            'id', 'empresa', 'data', 'tipo', 'descricao', 'valor'
        ])
        df.to_csv(DATA_PATH, index=False)
        return df
    return pd.read_csv(DATA_PATH)

def add_transaction(empresa, data, tipo, descricao, valor):
    """Adiciona uma nova transação ao CSV"""
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
    df = df.append(new_row, ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    return transaction_id

def get_transactions(empresa=None, periodo=None):
    """Recupera transações com filtros opcionais"""
    df = pd.read_csv(DATA_PATH)
    
    if empresa:
        df = df[df['empresa'] == empresa]
    
    if periodo:
        # Assumindo que periodo é um tuple (data_inicio, data_fim)
        df = df[(df['data'] >= periodo[0]) & (df['data'] <= periodo[1])]
    
    return df
