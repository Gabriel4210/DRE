import pandas as pd

def calcular_dre(df, empresa=None, periodo=None):
    """
    Calcula o DRE com base nos lançamentos.
    
    Args:
        df: DataFrame com os lançamentos
        empresa: Nome da empresa para filtrar (opcional)
        periodo: Tuple (data_inicio, data_fim) para filtrar (opcional)
        
    Returns:
        dict: Dicionário com os valores do DRE mensal e totais
    """
    # Se o DataFrame estiver vazio, retorna valores zerados
    if df.empty:
        return {
            'mensal': pd.DataFrame(columns=['Receita', 'Custo', 'Despesa', 'Lucro Bruto', 'Lucro Líquido']),
            'totais': {
                'Receita': 0,
                'Custo': 0,
                'Despesa': 0,
                'Lucro Bruto': 0,
                'Lucro Líquido': 0
            }
        }
    
    # Filtra por empresa se especificado
    if empresa:
        df = df[df['empresa'] == empresa]
    
    # Filtra por período se especificado
    if periodo and len(periodo) == 2:
        # Converte datas para string se forem objetos datetime
        inicio = periodo[0]
        fim = periodo[1]
        
        if hasattr(inicio, 'strftime'):
            inicio = inicio.strftime('%Y-%m-%d')
        
        if hasattr(fim, 'strftime'):
            fim = fim.strftime('%Y-%m-%d')
        
        df = df[(df['data'] >= inicio) & (df['data'] <= fim)]
    
    # Se após os filtros o DataFrame estiver vazio, retorna valores zerados
    if df.empty:
        return {
            'mensal': pd.DataFrame(columns=['Receita', 'Custo', 'Despesa', 'Lucro Bruto', 'Lucro Líquido']),
            'totais': {
                'Receita': 0,
                'Custo': 0,
                'Despesa': 0,
                'Lucro Bruto': 0,
                'Lucro Líquido': 0
            }
        }
    
    # Converte para datetime para agrupar por mês
    df['data'] = pd.to_datetime(df['data'])
    df['mes'] = df['data'].dt.strftime('%Y-%m')
    
    # Agrupa por mês e tipo
    receitas = df[df['tipo'] == 'Receita'].groupby('mes')['valor'].sum()
    custos = df[df['tipo'] == 'Custo'].groupby('mes')['valor'].sum()
    despesas = df[df['tipo'] == 'Despesa'].groupby('mes')['valor'].sum()
    
    # Cria DataFrame do DRE mensal
    meses = sorted(list(set(receitas.index) | set(custos.index) | set(despesas.index)))
    dre_mensal = pd.DataFrame(index=meses, columns=['Receita', 'Custo', 'Despesa', 'Lucro Bruto', 'Lucro Líquido'])
    
    # Preenche valores
    dre_mensal['Receita'] = receitas
    dre_mensal['Custo'] = custos
    dre_mensal['Despesa'] = despesas
    
    # Preenche NaN com zeros
    dre_mensal = dre_mensal.fillna(0)
    
    # Calcula lucro bruto e líquido
    dre_mensal['Lucro Bruto'] = dre_mensal['Receita'] - dre_mensal['Custo']
    dre_mensal['Lucro Líquido'] = dre_mensal['Lucro Bruto'] - dre_mensal['Despesa']
    
    # Calcula totais
    totais = {
        'Receita': dre_mensal['Receita'].sum(),
        'Custo': dre_mensal['Custo'].sum(),
        'Despesa': dre_mensal['Despesa'].sum(),
        'Lucro Bruto': dre_mensal['Lucro Bruto'].sum(),
        'Lucro Líquido': dre_mensal['Lucro Líquido'].sum()
    }
    
    return {
        'mensal': dre_mensal,
        'totais': totais
    }
    
    return {
        'mensal': dre,
        'totais': totais
    }
