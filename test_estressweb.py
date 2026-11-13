import time
from webbrowser import open_new_tab
import matplotlib.pyplot as plt
import pandas as pd
import pytest
from sklearn.tree import DecisionTreeClassifier

URL_SITE = "http://localhost:3301/objetos"


@pytest.fixture(scope="session")
def historico_testes():
    dados = []
    yield dados
    # Roda automaticamente após as 100 abas serem disparadas
    analisar_com_ml_e_gerar_grafico(dados)


@pytest.mark.parametrize("execucao", range(1, 101))
def test_abrir_aba_navegador(execucao, historico_testes):
    inicio = time.time()

    # Dispara a abertura de uma nova aba no navegador padrão do sistema
    abriu_comando = open_new_tab(URL_SITE)

    # Mede quanto tempo (em ms) o sistema levou para processar o comando de abertura
    tempo_disparo_ms = round((time.time() - inicio) * 1000, 2)

    # Pequena pausa opcional para não travar completamente a interface gráfica do navegador
    time.sleep(0.05)

    historico_testes.append({
        "Execucao": execucao,
        "Tempo_Disparo_ms": tempo_disparo_ms,
        "Comando_Aceito": 1 if abriu_comando else 0,
    })

    # O Pytest valida se o sistema operacional aceitou o comando de abrir o navegador
    assert abriu_comando is True, f"Falha ao disparar aba na execução {execucao}"


def analisar_com_ml_e_gerar_grafico(historico):
    if not historico:
        return

    df_real = pd.DataFrame(historico)

    # --- TREINANDO O ROBÔ (DecisionTreeClassifier) ---
    # Como o webbrowser não lê o conteúdo da página, o ML avalia a velocidade de resposta
    # do navegador para abrir a aba (ex: < 50ms = Bom; > 50ms por gargalo de memória = Ruim)
    dados_treino = {
        "Tempo_Disparo_ms": [5, 12, 20, 35, 45, 60, 100, 200, 350, 500],
        "Comando_Aceito": [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        "Avaliacao": [
            "Bom",
            "Bom",
            "Bom",
            "Bom",
            "Bom",
            "Ruim",
            "Ruim",
            "Ruim",
            "Ruim",
            "Ruim",
        ],
    }
    df_treino = pd.DataFrame(dados_treino)

    modelo = DecisionTreeClassifier()
    modelo.fit(
        df_treino[["Tempo_Disparo_ms", "Comando_Aceito"]],
        df_treino["Avaliacao"],
    )

    # Robô classifica os 100 disparos de abas
    df_real["Veredito_Robo"] = modelo.predict(
        df_real[["Tempo_Disparo_ms", "Comando_Aceito"]]
    )

    print("\n=== RESULTADO DAS 100 ABERTURAS DE ABA (WEBBROWSER + ML) ===")
    print(df_real.head(15))
    print("\nResumo geral:")
    print(df_real["Veredito_Robo"].value_counts())

    # --- GERANDO O GRÁFICO (Matplotlib) ---
    plt.figure(figsize=(10, 6))

    bons = df_real[df_real["Veredito_Robo"] == "Bom"]
    ruins = df_real[df_real["Veredito_Robo"] == "Ruim"]

    plt.scatter(
        bons["Execucao"],
        bons["Tempo_Disparo_ms"],
        color="green",
        label="Abertura Rápida / Boa (ML)",
        alpha=0.7,
    )
    plt.scatter(
        ruins["Execucao"],
        ruins["Tempo_Disparo_ms"],
        color="red",
        label="Abertura Lenta / Gargalo (ML)",
        alpha=0.7,
    )

    plt.title(
        "Teste de Estresse com webbrowser (100 Abas no localhost:3301) + IA"
    )
    plt.xlabel("Número da Aba Aberta (1 a 100)")
    plt.ylabel("Tempo de Resposta do Sistema (ms)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.savefig("resultado_webbrowser_100.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])