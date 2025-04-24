import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def criar_grafico_evolucao(dre_mensal):
    """
    Cria gráfico de evolução mensal de receitas, custos e lucros.
    
    Args:
        dre_mensal: DataFrame com o DRE mensal
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de evolução
    """
    # Se o DataFrame estiver vazio, retorna um gráfico vazio
    if dre_mensal.empty:
        fig = go.Figure()
        fig.update_layout(
            title="Sem dados para exibir",
            xaxis_title="Mês",
            yaxis_title="Valor (R$)"
        )
        return fig
    
    # Prepara os dados
    df = dre_mensal.reset_index()
    
    # Cria o gráfico
    fig = go.Figure()
    
    # Adiciona linhas para cada métrica
    fig.add_trace(go.Scatter(
        x=df['mes'], 
        y=df['Receita'], 
        name='Receita',
        line=dict(color='green', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['mes'], 
        y=df['Custo'], 
        name='Custo',
        line=dict(color='red', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['mes'], 
        y=df['Despesa'], 
        name='Despesa',
        line=dict(color='orange', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['mes'], 
        y=df['Lucro Líquido'], 
        name='Lucro Líquido',
        line=dict(color='blue', width=3)
    ))
    
    # Atualiza layout
    fig.update_layout(
        title='Evolução Mensal',
        xaxis_title='Mês',
        yaxis_title='Valor (R$)',
        legend_title='Categoria',
        hovermode='x unified'
    )
    
    return fig

def criar_grafico_distribuicao_despesas(df, empresa=None, periodo=None):
    """
    Cria gráfico de pizza para distribuição das despesas.
    
    Args:
        df: DataFrame com os lançamentos
        empresa: Nome da empresa para filtrar (opcional)
        periodo: Tuple (data_inicio, data_fim) para filtrar (opcional)
        
    Returns:
        plotly.graph_objects.Figure: Gráfico de distribuição de despesas
    """
    # Filtra dados
    dados = df.copy()
    
    # Filtra por empresa
    if empresa:
        dados = dados[dados['empresa'] == empresa]
    
    # Filtra por período
    if periodo and len(periodo) == 2:
        # Converte datas para string se forem objetos datetime
        inicio = periodo[0]
        fim = periodo[1]
        
        if hasattr(inicio, 'strftime'):
            inicio = inicio.strftime('%Y-%m-%d')
        
        if hasattr(fim, 'strftime'):
            fim = fim.strftime('%Y-%m-%d')
        
        dados = dados[(dados['data'] >= inicio) & (dados['data'] <= fim)]
    
    # Filtra apenas despesas
    dados = dados[dados['tipo'] == 'Despesa']
    
    # Se não houver dados, retorna um gráfico vazio
    if dados.empty:
        fig = go.Figure()
        fig.update_layout(
            title="Sem despesas para exibir",
            xaxis_title="",
            yaxis_title=""
        )
        return fig
    
    # Agrupa por descrição
    despesas_por_categoria = dados.groupby('descricao')['valor'].sum().reset_index()
    
    # Cria gráfico
    fig = px.pie(
        despesas_por_categoria, 
        values='valor', 
        names='descricao',
        title='Distribuição de Despesas',
        hole=0.4,  # Para criar um donut chart
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    return fig
