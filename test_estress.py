import time
import requests
import pytest
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier

URL_API = "http://localhost:3301/objetos"

# Fixture que cria a lista, entrega para os 100 testes e, ao final, roda o ML e o gráfico
@pytest.fixture(scope="session")
def historico_testes():
    dados = []
    yield dados  # Pausa aqui enquanto os 100 testes rodam e preenchem 'dados'
    
    # Assim que os 100 testes acabam, o código continua automaticamente daqui:
    analisar_com_ml_e_gerar_grafico(dados)


@pytest.mark.parametrize("execucao", range(1, 101))
def test_requisicao_json_server(execucao, historico_testes):
    inicio = time.time()
    
    try:
        resposta = requests.get(URL_API, timeout=2)
        tempo_ms = round((time.time() - inicio) * 1000, 2)
        status = resposta.status_code
        qtd_objetos = len(resposta.json()) if status == 200 else 0
    except Exception:
        tempo_ms = 2000.0
        status = 500
        qtd_objetos = 0

    historico_testes.append({
        "Execucao": execucao,
        "Tempo_Resposta_ms": tempo_ms,
        "Qtd_Objetos": qtd_objetos,
        "Status_HTTP": status
    })

    assert status == 200, f"Falha na execução {execucao}: Status {status}"


def analisar_com_ml_e_gerar_grafico(historico):
    if not historico:
        print("Nenhum dado de teste foi coletado.")
        return

    df_real = pd.DataFrame(historico)

    # Treinando a Árvore de Decisão
    dados_treino = {
        'Tempo_Resposta_ms': [10, 25, 40, 80, 120, 180, 250, 500, 15, 300],
        'Qtd_Objetos':       [14, 14, 14, 14,  14,  14,  14,   0,  0,   5],
        'Avaliacao':         ['Bom', 'Bom', 'Bom', 'Bom', 'Bom', 'Ruim', 'Ruim', 'Ruim', 'Ruim', 'Ruim']
    }
    df_treino = pd.DataFrame(dados_treino)

    modelo = DecisionTreeClassifier()
    modelo.fit(df_treino[['Tempo_Resposta_ms', 'Qtd_Objetos']], df_treino['Avaliacao'])

    # Robô classificando os 100 testes
    df_real['Veredito_Robo'] = modelo.predict(df_real[['Tempo_Resposta_ms', 'Qtd_Objetos']])

    print("\n=== RESULTADO DOS TESTES CLASSIFICADOS PELO ROBÔ ===")
    print(df_real.head(15))
    print("\nResumo geral:")
    print(df_real['Veredito_Robo'].value_counts())

    # Gerando o gráfico
    plt.figure(figsize=(10, 6))
    bons = df_real[df_real['Veredito_Robo'] == 'Bom']
    ruins = df_real[df_real['Veredito_Robo'] == 'Ruim']

    plt.scatter(bons['Execucao'], bons['Tempo_Resposta_ms'], color='green', label='Teste Bom (ML)', alpha=0.7)
    plt.scatter(ruins['Execucao'], ruins['Tempo_Resposta_ms'], color='red', label='Teste Ruim (ML)', alpha=0.7)

    plt.title('Análise de Performance da API (JSON-Server) com Pytest + ML')
    plt.xlabel('Número da Execução (1 a 100)')
    plt.ylabel('Tempo de Resposta (ms)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Salva a imagem na pasta do projeto e abre na tela
    plt.savefig("resultado_testes_ML.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    # O '-s' permite que os prints da IA apareçam no terminal do VS Code
    pytest.main([__file__, "-v", "-s"])