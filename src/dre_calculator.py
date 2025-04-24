import pandas as pd

def calcular_dre(df, empresa, periodo=None):
    """
    Calcula o DRE com base nos lançamentos filtrados
    
    Args:
        df: DataFrame com os lançamentos
        empresa: Nome da empresa para filtrar
        periodo: Tuple (data_inicio, data_fim) opcional
        
    Returns:
        dict: Dicionário com os valores do DRE
    """
    # Filtra por empresa
    dados = df[df['empresa'] == empresa].copy()
    
    # Filtra por período se fornecido
    if periodo:
        dados = dados[(dados['data'] >= periodo[0]) & (dados['data'] <= periodo[1])]
    
    # Converte para datetime para agrupar por mês
    dados['data'] = pd.to_datetime(dados['data'])
    dados['mes'] = dados['data'].dt.strftime('%Y-%m')
    
    # Agrupa por mês e tipo
    receitas = dados[dados['tipo'] == 'Receita'].groupby('mes')['valor'].sum()
    custos = dados[dados['tipo'] == 'Custo'].groupby('mes')['valor'].sum()
    despesas = dados[dados['tipo'] == 'Despesa'].groupby('mes')['valor'].sum()
    
    # Cria DataFrame do DRE
    dre = pd.DataFrame({
        'Receita': receitas,
        'Custo': custos,
        'Despesa': despesas
    }).fillna(0)
    
    # Calcula lucro bruto e líquido
    dre['Lucro Bruto'] = dre['Receita'] - dre['Custo']
    dre['Lucro Líquido'] = dre['Lucro Bruto'] - dre['Despesa']
    
    # Calcula totais
    totais = {
        'Receita': dre['Receita'].sum(),
        'Custo': dre['Custo'].sum(),
        'Despesa': dre['Despesa'].sum(),
        'Lucro Bruto': dre['Lucro Bruto'].sum(),
        'Lucro Líquido': dre['Lucro Líquido'].sum()
    }
    
    return {
        'mensal': dre,
        'totais': totais
    }
