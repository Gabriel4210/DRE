import plotly.express as px
import plotly.graph_objects as go

def criar_grafico_evolucao(dre_mensal):
    """Cria gráfico de evolução mensal de receitas, custos e lucros"""
    df = dre_mensal.reset_index()
    
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

def criar_grafico_distribuicao_despesas(df, empresa, periodo=None):
    """Cria gráfico de pizza para distribuição das despesas"""
    # Filtra dados
    dados = df[(df['empresa'] == empresa) & (df['tipo'] == 'Despesa')].copy()
    
    if periodo:
        dados = dados[(dados['data'] >= periodo[0]) & (dados['data'] <= periodo[1])]
    
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
