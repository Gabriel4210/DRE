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
    import plotly.graph_objects as go
    
    # Verificação se o DataFrame está vazio
    if dre_mensal is None or dre_mensal.empty:
        # Retorna um gráfico vazio com mensagem informativa
        fig = go.Figure()
        fig.update_layout(
            title="Sem dados para exibir",
            xaxis_title="Mês",
            yaxis_title="Valor (R$)",
            annotations=[
                dict(
                    text="Não há dados disponíveis para o período selecionado",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5
                )
            ]
        )
        return fig
    
    try:
        # Prepara os dados - Importante: Garantimos que o índice seja usado como coluna 'mes'
        # Isso resolve o problema de KeyError: 'mes'
        df = dre_mensal.reset_index()
        
        # Verifica se a coluna do índice tem o nome correto
        if 'index' in df.columns and 'mes' not in df.columns:
            df = df.rename(columns={'index': 'mes'})
        
        # Se ainda não tiver a coluna 'mes', cria uma mensagem de erro
        if 'mes' not in df.columns:
            raise KeyError("A coluna 'mes' não foi encontrada no DataFrame. Verifique o formato dos dados.")
        
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
        
    except KeyError as e:
        # Log do erro para debugging
        print(f"Erro ao criar gráfico de evolução: {e}")
        print(f"Colunas disponíveis: {df.columns.tolist()}")
        
        # Retorna um gráfico com mensagem de erro
        fig = go.Figure()
        fig.update_layout(
            title="Erro ao gerar gráfico",
            xaxis_title="Mês",
            yaxis_title="Valor (R$)",
            annotations=[
                dict(
                    text=f"Erro ao processar dados: {str(e)}",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5
                )
            ]
        )
        return fig
    
    except Exception as e:
        # Log do erro para debugging
        print(f"Erro inesperado ao criar gráfico de evolução: {e}")
        
        # Retorna um gráfico com mensagem de erro genérica
        fig = go.Figure()
        fig.update_layout(
            title="Erro ao gerar gráfico",
            xaxis_title="Mês",
            yaxis_title="Valor (R$)",
            annotations=[
                dict(
                    text="Ocorreu um erro ao gerar o gráfico. Por favor, verifique os dados.",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5
                )
            ]
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
