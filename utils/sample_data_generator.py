import pandas as pd
import random
from datetime import datetime, timedelta

def gerar_dados_exemplo():
    """Gera dados de exemplo para 6 meses e 2 empresas"""
    empresas = ["Empresa A", "Empresa B"]
    tipos = ["Receita", "Custo", "Despesa"]
    
    # Categorias por tipo
    categorias = {
        "Receita": ["Vendas", "Serviços", "Assinaturas", "Outros"],
        "Custo": ["Matéria-prima", "Produção", "Logística", "Outros"],
        "Despesa": ["Aluguel", "Salários", "Marketing", "Utilities", "Outros"]
    }
    
    # Data inicial (6 meses atrás)
    data_inicial = datetime.now() - timedelta(days=180)
    
    # Lista para armazenar os dados
    dados = []
    
    # Gera transações para cada mês
    for mes in range(6):
        data_mes = data_inicial + timedelta(days=30 * mes)
        
        for empresa in empresas:
            # Gera receitas (3-5 por mês)
            for _ in range(random.randint(3, 5)):
                categoria = random.choice(categorias["Receita"])
                valor = random.randint(3000, 8000)
                
                dados.append({
                    'id': random.randint(10000, 99999),
                    'empresa': empresa,
                    'data': (data_mes + timedelta(days=random.randint(1, 28))).strftime('%Y-%m-%d'),
                    'tipo': "Receita",
                    'descricao': categoria,
                    'valor': valor
                })
            
            # Gera custos (2-4 por mês)
            for _ in range(random.randint(2, 4)):
                categoria = random.choice(categorias["Custo"])
                valor = random.randint(1000, 4000)
                
                dados.append({
                    'id': random.randint(10000, 99999),
                    'empresa': empresa,
                    'data': (data_mes + timedelta(days=random.randint(1, 28))).strftime('%Y-%m-%d'),
                    'tipo': "Custo",
                    'descricao': categoria,
                    'valor': valor
                })
            
            # Gera despesas (3-6 por mês)
            for _ in range(random.randint(3, 6)):
                categoria = random.choice(categorias["Despesa"])
                valor = random.randint(500, 3000)
                
                dados.append({
                    'id': random.randint(10000, 99999),
                    'empresa': empresa,
                    'data': (data_mes + timedelta(days=random.randint(1, 28))).strftime('%Y-%m-%d'),
                    'tipo': "Despesa",
                    'descricao': categoria,
                    'valor': valor
                })
    
    # Cria DataFrame e salva como CSV
    df = pd.DataFrame(dados)
    df.to_csv("data/sample_data.csv", index=False)
    
    return df
