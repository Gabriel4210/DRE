import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Importa módulos personalizados
from src.data_manager import initialize_data, add_transaction, get_transactions
from src.dre_calculator import calcular_dre
from src.visualizations import criar_grafico_evolucao, criar_grafico_distribuicao_despesas
from utils.validators import validar_formulario
from utils.formatters import formatar_moeda

# Configuração da página
st.set_page_config(
    page_title="DRE App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa o estado da sessão
if 'data' not in st.session_state:
    st.session_state.data = initialize_data()

# Sidebar para navegação
st.sidebar.title("DRE App")
pagina = st.sidebar.radio(
    "Navegação",
    ["Dashboard", "Lançamentos", "DRE", "Gráficos"]
)

# Lista de empresas (poderia vir de um banco de dados)
empresas = ["Empresa A", "Empresa B", "Empresa C"]

# Função para a página de Dashboard
def pagina_dashboard():
    st.title("Dashboard Financeiro")
    
    col1, col2 = st.columns(2)
    
    with col1:
        empresa = st.selectbox("Selecione a Empresa", empresas, key="dash_empresa")
    
    with col2:
        periodo = st.date_input(
            "Período",
            [datetime.now() - timedelta(days=180), datetime.now()],
            key="dash_periodo"
        )
    
    # Calcula o DRE para a empresa e período selecionados
    df = get_transactions()
    if not df.empty:
        resultado_dre = calcular_dre(df, empresa, periodo)
        
        # Exibe cards com os totais
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Receitas", formatar_moeda(resultado_dre['totais']['Receita']))
        
        with col2:
            st.metric("Custos", formatar_moeda(resultado_dre['totais']['Custo']))
        
        with col3:
            st.metric("Despesas", formatar_moeda(resultado_dre['totais']['Despesa']))
        
        with col4:
            st.metric("Lucro Bruto", formatar_moeda(resultado_dre['totais']['Lucro Bruto']))
        
        with col5:
            st.metric("Lucro Líquido", formatar_moeda(resultado_dre['totais']['Lucro Líquido']))
        
        # Exibe gráficos
        st.subheader("Evolução Mensal")
        st.plotly_chart(criar_grafico_evolucao(resultado_dre['mensal']), use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuição de Despesas")
            st.plotly_chart(criar_grafico_distribuicao_despesas(df, empresa, periodo), use_container_width=True)
    else:
        st.info("Não há dados disponíveis. Adicione lançamentos na página 'Lançamentos'.")

# Função para a página de Lançamentos
def pagina_lancamentos():
    st.title("Lançamento de Movimentações")
    
    with st.form("lancamento_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            empresa = st.selectbox("Empresa", empresas)
            data = st.date_input("Data", datetime.now())
            
        with col2:
            tipo = st.selectbox("Tipo", ["Receita", "Custo", "Despesa"])
            valor = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
        
        descricao = st.text_input("Descrição")
        
        submitted = st.form_submit_button("Salvar Lançamento")
        
        if submitted:
            # Valida o formulário
            if validar_formulario(empresa, data, tipo, descricao, valor):
                # Adiciona a transação
                transaction_id = add_transaction(
                    empresa, 
                    data.strftime('%Y-%m-%d'), 
                    tipo, 
                    descricao, 
                    valor
                )
                
                # Recarrega os dados
                st.session_state.data = get_transactions()
                
                st.success(f"Lançamento registrado com sucesso! ID: {transaction_id}")
            else:
                st.error("Por favor, preencha todos os campos corretamente.")
    
    # Exibe os últimos lançamentos
    st.subheader("Últimos Lançamentos")
    
    df = get_transactions()
    if not df.empty:
        # Ordena por data decrescente e exibe os últimos 10
        df_sorted = df.sort_values(by='data', ascending=False).head(10)
        st.dataframe(df_sorted)
    else:
        st.info("Não há lançamentos registrados.")

# Função para a página de DRE
def pagina_dre():
    st.title("Demonstrativo de Resultados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        empresa = st.selectbox("Selecione a Empresa", empresas, key="dre_empresa")
    
    with col2:
        periodo = st.date_input(
            "Período",
            [datetime.now() - timedelta(days=180), datetime.now()],
            key="dre_periodo"
        )
    
    # Calcula o DRE
    df = get_transactions()
    if not df.empty:
        resultado_dre = calcular_dre(df, empresa, periodo)
        
        # Exibe o DRE mensal
        st.subheader("DRE Mensal")
        st.dataframe(resultado_dre['mensal'].style.format("{:.2f}"))
        
        # Exibe o DRE consolidado
        st.subheader("DRE Consolidado")
        
        # Cria DataFrame para o DRE consolidado
        dre_consolidado = pd.DataFrame({
            'Item': ['Receita', 'Custo', 'Lucro Bruto', 'Despesa', 'Lucro Líquido'],
            'Valor': [
                resultado_dre['totais']['Receita'],
                resultado_dre['totais']['Custo'],
                resultado_dre['totais']['Lucro Bruto'],
                resultado_dre['totais']['Despesa'],
                resultado_dre['totais']['Lucro Líquido']
            ]
        })
        
        st.dataframe(dre_consolidado.style.format({'Valor': 'R$ {:.2f}'}))
        
        # Botão para exportar
        if st.button("Exportar DRE (CSV)"):
            # Cria um link para download
            csv = resultado_dre['mensal'].to_csv(index=True)
            st.download_button(
                label="Clique para baixar",
                data=csv,
                file_name=f"dre_{empresa}_{periodo[0]}_{periodo[1]}.csv",
                mime="text/csv"
            )
    else:
        st.info("Não há dados disponíveis. Adicione lançamentos na página 'Lançamentos'.")

# Função para a página de Gráficos
def pagina_graficos():
    st.title("Análise Gráfica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        empresa = st.selectbox("Selecione a Empresa", empresas, key="graf_empresa")
    
    with col2:
        periodo = st.date_input(
            "Período",
            [datetime.now() - timedelta(days=180), datetime.now()],
            key="graf_periodo"
        )
    
    # Tipo de gráfico
    tipo_grafico = st.radio(
        "Selecione o tipo de gráfico",
        ["Evolução Mensal", "Distribuição de Despesas", "Comparação de Empresas"]
    )
    
    df = get_transactions()
    if not df.empty:
        if tipo_grafico == "Evolução Mensal":
            resultado_dre = calcular_dre(df, empresa, periodo)
            st.plotly_chart(criar_grafico_evolucao(resultado_dre['mensal']), use_container_width=True)
            
        elif tipo_grafico == "Distribuição de Despesas":
            st.plotly_chart(criar_grafico_distribuicao_despesas(df, empresa, periodo), use_container_width=True)
            
        elif tipo_grafico == "Comparação de Empresas":
            # Cria um gráfico comparativo entre empresas
            resultados = {}
            for emp in empresas:
                resultado_dre = calcular_dre(df, emp, periodo)
                resultados[emp] = resultado_dre['totais']
            
            # Cria DataFrame para comparação
            df_comparacao = pd.DataFrame({
                'Empresa': [],
                'Métrica': [],
                'Valor': []
            })
            
            for empresa, valores in resultados.items():
                for metrica, valor in valores.items():
                    df_comparacao = df_comparacao.append({
                        'Empresa': empresa,
                        'Métrica': metrica,
                        'Valor': valor
                    }, ignore_index=True)
            
            # Cria gráfico de barras
            fig = px.bar(
                df_comparacao, 
                x='Empresa', 
                y='Valor', 
                color='Métrica',
                barmode='group',
                title='Comparação entre Empresas',
                labels={'Valor': 'Valor (R$)'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Não há dados disponíveis. Adicione lançamentos na página 'Lançamentos'.")

# Renderiza a página selecionada
if pagina == "Dashboard":
    pagina_dashboard()
elif pagina == "Lançamentos":
    pagina_lancamentos()
elif pagina == "DRE":
    pagina_dre()
elif pagina == "Gráficos":
    pagina_graficos()
