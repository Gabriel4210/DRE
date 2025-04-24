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
def get_csv_download_link(df, filename="dados_financeiros.csv", text="Baixar CSV"):
    """Gera um link para download do DataFrame como CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def import_csv(uploaded_file):
    """Importa dados de um arquivo CSV enviado pelo usuário"""
    try:
        # Lê o arquivo enviado
        df_imported = pd.read_csv(uploaded_file)
        
        # Verifica se o arquivo tem as colunas necessárias
        required_columns = ['empresa', 'data', 'tipo', 'descricao', 'valor']
        missing_columns = [col for col in required_columns if col not in df_imported.columns]
        
        if missing_columns:
            return False, f"Arquivo inválido. Colunas ausentes: {', '.join(missing_columns)}"
        
        # Se não tiver coluna 'id', adiciona IDs baseados no timestamp
        if 'id' not in df_imported.columns:
            base_timestamp = int(datetime.now().timestamp())
            df_imported['id'] = [base_timestamp + i for i in range(len(df_imported))]
        
        # Carrega os dados existentes
        if os.path.exists(DATA_PATH):
            df_existing = pd.read_csv(DATA_PATH)
            
            # Opção 1: Substituir todos os dados
            # df_existing = df_imported
            
            # Opção 2: Adicionar apenas os novos (evitando duplicatas de ID)
            existing_ids = set(df_existing['id'].values)
            new_records = df_imported[~df_imported['id'].isin(existing_ids)]
            df_combined = pd.concat([df_existing, new_records], ignore_index=True)
            
            # Salva o DataFrame combinado
            df_combined.to_csv(DATA_PATH, index=False)
        else:
            # Se não existir arquivo, salva o importado diretamente
            os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
            df_imported.to_csv(DATA_PATH, index=False)
        
        return True, f"Importação concluída com sucesso! {len(df_imported)} registros processados."
    
    except Exception as e:
        return False, f"Erro ao importar dados: {str(e)}"

# Adicione esta seção à sua interface, por exemplo na página de lançamentos
def adicionar_secao_importacao_exportacao():
    st.subheader("Importar/Exportar Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Exportar Dados")
        df = get_transactions()  # Obtém todos os dados atuais
        if not df.empty:
            st.markdown(get_csv_download_link(df), unsafe_allow_html=True)
        else:
            st.info("Não há dados para exportar.")
    
    with col2:
        st.markdown("### Importar Dados")
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
        
        if uploaded_file is not None:
            if st.button("Processar Importação"):
                success, message = import_csv(uploaded_file)
                if success:
                    st.success(message)
                    # Opcional: recarregar a página para mostrar os novos dados
                    st.experimental_rerun()
                else:
                    st.error(message)
