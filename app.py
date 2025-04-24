# app.py
import base64
from io import StringIO
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# Importa módulos personalizados
from src.data_manager import initialize_data, add_transaction, get_transactions
from src.dre_calculator import calcular_dre
from src.visualizations import criar_grafico_evolucao, criar_grafico_distribuicao_despesas
from utils.validators import validar_formulario
from utils.formatters import formatar_moeda, formatar_data

# Configuração da página
st.set_page_config(
    page_title="DRE App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa o estado da sessão
if 'data_initialized' not in st.session_state:
    try:
        # Tenta inicializar os dados
        initialize_data()
        st.session_state.data_initialized = True
    except Exception as e:
        st.error(f"Erro ao inicializar dados: {e}")
        st.session_state.data_initialized = False

# Lista de empresas (poderia vir de um banco de dados)
empresas = ["🚗 Transmaster", "💵 JM"]

# Sidebar para navegação
st.sidebar.title("DRE App")
pagina = st.sidebar.radio(
    "Navegação",
    ["Dashboard", "Lançamentos", "DRE", "Gráficos"]
)

# Função para gerar dados de exemplo
def gerar_dados_exemplo():
    """Gera dados de exemplo para 6 meses e 2 empresas"""
    import random
    
    # Empresas e tipos
    empresas_exemplo = ["🚗 Transmaster", "💵 JM"]
    
    # Categorias por tipo
    categorias = {
        "Receita": ["Vendas", "Serviços", "Assinaturas", "Outros"],
        "Custo": ["Matéria-prima", "Produção", "Logística", "Outros"],
        "Despesa": ["Aluguel", "Salários", "Marketing", "Utilities", "Outros"]
    }
    
    # Data inicial (6 meses atrás)
    data_inicial = datetime.now() - timedelta(days=180)
    
    # Contador de transações
    contador = 0
    
    # Gera transações para cada mês
    for mes in range(6):
        data_mes = data_inicial + timedelta(days=30 * mes)
        
        for empresa in empresas_exemplo:
            # Gera receitas (3-5 por mês)
            for _ in range(random.randint(3, 5)):
                categoria = random.choice(categorias["Receita"])
                valor = random.randint(3000, 8000)
                
                # Adiciona transação
                add_transaction(
                    empresa=empresa,
                    data=(data_mes + timedelta(days=random.randint(1, 28))).strftime('%Y-%m-%d'),
                    tipo="Receita",
                    descricao=categoria,
                    valor=valor
                )
                contador += 1
            
            # Gera custos (2-4 por mês)
            for _ in range(random.randint(2, 4)):
                categoria = random.choice(categorias["Custo"])
                valor = random.randint(1000, 4000)
                
                # Adiciona transação
                add_transaction(
                    empresa=empresa,
                    data=(data_mes + timedelta(days=random.randint(1, 28))).strftime('%Y-%m-%d'),
                    tipo="Custo",
                    descricao=categoria,
                    valor=valor
                )
                contador += 1
            
            # Gera despesas (3-6 por mês)
            for _ in range(random.randint(3, 6)):
                categoria = random.choice(categorias["Despesa"])
                valor = random.randint(500, 3000)
                
                # Adiciona transação
                add_transaction(
                    empresa=empresa,
                    data=(data_mes + timedelta(days=random.randint(1, 28))).strftime('%Y-%m-%d'),
                    tipo="Despesa",
                    descricao=categoria,
                    valor=valor
                )
                contador += 1
    
    return contador

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
    
    # Carrega os dados
    df = get_transactions()
    
    # Verifica se há dados
    if df.empty:
        st.info("Não há dados disponíveis. Adicione lançamentos na página 'Lançamentos' ou use o botão abaixo para gerar dados de exemplo.")
        
        if st.button("Gerar Dados de Exemplo"):
            contador = gerar_dados_exemplo()
            st.success(f"{contador} registros de exemplo foram gerados com sucesso!")
            st.experimental_rerun()
    else:
        # Calcula o DRE para a empresa e período selecionados
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
                try:
                    # Adiciona a transação
                    transaction_id = add_transaction(
                        empresa, 
                        data.strftime('%Y-%m-%d'), 
                        tipo, 
                        descricao, 
                        valor
                    )
                    
                    st.success(f"Lançamento registrado com sucesso! ID: {transaction_id}")
                except Exception as e:
                    st.error(f"Erro ao salvar lançamento: {e}")
            else:
                st.error("Por favor, preencha todos os campos corretamente.")
    
    # Exibe os últimos lançamentos
    st.subheader("Últimos Lançamentos")
    
    df = get_transactions()
    if not df.empty:
        # Ordena por data decrescente e exibe os últimos 10
        df_sorted = df.sort_values(by='data', ascending=False).head(10)
        
        # Formata para exibição
        df_display = df_sorted.copy()
        df_display['data'] = df_display['data'].apply(lambda x: formatar_data(x))
        df_display['valor'] = df_display['valor'].apply(lambda x: formatar_moeda(x))
        
        st.dataframe(df_display[['empresa', 'data', 'tipo', 'descricao', 'valor']])
    else:
        st.info("Não há lançamentos registrados.")
        
        # Botão para gerar dados de exemplo
        if st.button("Gerar Dados de Exemplo"):
            contador = gerar_dados_exemplo()
            st.success(f"{contador} registros de exemplo foram gerados com sucesso!")
            st.experimental_rerun()
    
        # Adicione esta seção ao final da função
    st.subheader("Importar/Exportar Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Exportar Dados")
        df_export = get_transactions()  # Obtém todos os dados atuais
        if not df_export.empty:
            # Função para gerar link de download
            csv = df_export.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="dados_financeiros.csv">Baixar CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("Não há dados para exportar.")
    
    with col2:
        st.markdown("### Importar Dados")
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
        
        if uploaded_file is not None:
            if st.button("Processar Importação"):
                try:
                    # Lê o arquivo enviado
                    df_imported = pd.read_csv(uploaded_file)
                    
                    # Verifica se o arquivo tem as colunas necessárias
                    required_columns = ['empresa', 'data', 'tipo', 'descricao', 'valor']
                    missing_columns = [col for col in required_columns if col not in df_imported.columns]
                    
                    if missing_columns:
                        st.error(f"Arquivo inválido. Colunas ausentes: {', '.join(missing_columns)}")
                    else:
                        # Se não tiver coluna 'id', adiciona IDs baseados no timestamp
                        if 'id' not in df_imported.columns:
                            base_timestamp = int(datetime.now().timestamp())
                            df_imported['id'] = [base_timestamp + i for i in range(len(df_imported))]
                        
                        # Carrega os dados existentes
                        DATA_PATH = "data/user_data.csv"  # Use o mesmo caminho definido no seu código
                        if os.path.exists(DATA_PATH):
                            df_existing = pd.read_csv(DATA_PATH)
                            
                            # Adicionar apenas os novos (evitando duplicatas de ID)
                            existing_ids = set(df_existing['id'].values)
                            new_records = df_imported[~df_imported['id'].isin(existing_ids)]
                            df_combined = pd.concat([df_existing, new_records], ignore_index=True)
                            
                            # Salva o DataFrame combinado
                            df_combined.to_csv(DATA_PATH, index=False)
                        else:
                            # Se não existir arquivo, salva o importado diretamente
                            os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
                            df_imported.to_csv(DATA_PATH, index=False)
                        
                        st.success(f"Importação concluída com sucesso! {len(df_imported)} registros processados.")
                        st.experimental_rerun()
                
                except Exception as e:
                    st.error(f"Erro ao importar dados: {str(e)}")

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
    
    # Carrega os dados
    df = get_transactions()
    
    # Verifica se há dados
    if df.empty:
        st.info("Não há dados disponíveis. Adicione lançamentos na página 'Lançamentos' ou use o botão abaixo para gerar dados de exemplo.")
        
        if st.button("Gerar Dados de Exemplo"):
            contador = gerar_dados_exemplo()
            st.success(f"{contador} registros de exemplo foram gerados com sucesso!")
            st.experimental_rerun()
    else:
        # Calcula o DRE
        resultado_dre = calcular_dre(df, empresa, periodo)
        
        # Exibe o DRE mensal
        st.subheader("DRE Mensal")
        
        # Formata o DRE para exibição
        dre_display = resultado_dre['mensal'].copy()
        
        # Aplica formatação de moeda a todas as colunas
        for coluna in dre_display.columns:
            dre_display[coluna] = dre_display[coluna].apply(lambda x: formatar_moeda(x))
        
        st.dataframe(dre_display)
        
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
        
        # Formata os valores
        dre_consolidado['Valor'] = dre_consolidado['Valor'].apply(lambda x: formatar_moeda(x))
        
        st.dataframe(dre_consolidado)
        
        # Botão para exportar
        if st.button("Exportar DRE (CSV)"):
            # Cria CSV
            csv = resultado_dre['mensal'].to_csv(index=True)
            
            # Cria botão de download
            st.download_button(
                label="Clique para baixar",
                data=csv,
                file_name=f"dre_{empresa}_{periodo[0].strftime('%Y-%m-%d')}_{periodo[1].strftime('%Y-%m-%d')}.csv",
                mime="text/csv"
            )

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
    
    # Carrega os dados
    df = get_transactions()
    
    # Verifica se há dados
    if df.empty:
        st.info("Não há dados disponíveis. Adicione lançamentos na página 'Lançamentos' ou use o botão abaixo para gerar dados de exemplo.")
        
        if st.button("Gerar Dados de Exemplo"):
            contador = gerar_dados_exemplo()
            st.success(f"{contador} registros de exemplo foram gerados com sucesso!")
            st.experimental_rerun()
    else:
        if tipo_grafico == "Evolução Mensal":
            resultado_dre = calcular_dre(df, empresa, periodo)
            st.plotly_chart(criar_grafico_evolucao(resultado_dre['mensal']), use_container_width=True)
            
        elif tipo_grafico == "Distribuição de Despesas":
            st.plotly_chart(criar_grafico_distribuicao_despesas(df, empresa, periodo), use_container_width=True)
            
        elif tipo_grafico == "Comparação de Empresas":
            # Cria um gráfico comparativo entre empresas
            st.subheader("Comparação entre Empresas")
            
            # Calcula DRE para cada empresa
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
            
            for empresa_nome, valores in resultados.items():
                for metrica, valor in valores.items():
                    df_comparacao = pd.concat([
                        df_comparacao, 
                        pd.DataFrame({
                            'Empresa': [empresa_nome],
                            'Métrica': [metrica],
                            'Valor': [valor]
                        })
                    ], ignore_index=True)
            
            # Cria gráfico de barras
            import plotly.express as px
            
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

# Renderiza a página selecionada
if pagina == "Dashboard":
    pagina_dashboard()
elif pagina == "Lançamentos":
    pagina_lancamentos()
elif pagina == "DRE":
    pagina_dre()
elif pagina == "Gráficos":
    pagina_graficos()
