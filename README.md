# Teste de Estresse e Classificação Automatizada com Pytest, JSON-Server e Machine Learning

Projeto de automação de testes de carga e estresse em uma API local (`json-server`), integrando **Pytest** para execução repetitiva, **Scikit-Learn (Árvore de Decisão)** para classificação automática dos resultados e **Matplotlib** para visualização gráfica de performance — eliminando a necessidade de planilhas intermediárias.

---

## Sobre o Projeto

O objetivo deste projeto é submeter um endpoint local (`http://localhost:3301/objetos`) a **100 requisições/aberturas consecutivas**, coletar métricas de tempo de resposta em tempo real e utilizar um modelo de aprendizado de máquina (`DecisionTreeClassifier`) para julgar de forma autônoma quais execuções tiveram desempenho **Bom** ou **Ruim** (gargalo/latência alta).

O repositório contempla três abordagens distintas de teste:

1. **Teste de API (`requests`):** Focado na velocidade e integridade dos dados JSON retornados.
2. **Teste de Navegador Real (`playwright`):** Mede o tempo total de renderização da página completa (HTML, CSS, JS e DOM).
3. **Teste de Estresse de Interface (`webbrowser`):** Dispara a abertura real de 100 abas no navegador padrão do sistema para medir o gargalo de resposta do sistema operacional e consumo de memória.

---

## Tecnologias Utilizadas

- **[Python 3.10+](https://www.python.org/)**
- **[JSON-Server](https://github.com/typicode/json-server):** Simulação de API REST a partir de um arquivo `db.json`.
- **[Pytest](https://docs.pytest.org/):** Framework de testes parametrizados e gerenciamento de ciclo de vida via `fixtures`.
- **[Pandas](https://pandas.pydata.org/):** Estruturação e manipulação dos dados coletados em memória.
- **[Scikit-Learn](https://scikit-learn.org/):** Treinamento e predição utilizando `DecisionTreeClassifier`.
- **[Matplotlib](https://matplotlib.org/):** Geração de gráficos de dispersão (`scatter plot`) e exportação em `.png`.
- **[Requests](https://requests.readthedocs.io/) / [Playwright](https://playwright.dev/python/):** Clientes HTTP e automação de navegador.

---

## Pré-requisitos e Instalação

### 1. Clonar o repositório

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```


### 2. Instalar as dependências do Python
```bash
pip install pytest requests pandas scikit-learn matplotlib playwright
playwright install chromium
```

### 3. Configurar e iniciar o JSON-Server
Certifique-se de ter o Node.js instalado e o arquivo db.json estruturado na raiz do projeto:
```json
{
  "objetos": [
    {
      "id": "1",
      "nome": "Objeto 1",
      "local": "Casa",
      "valor": "Doido demaissss",
      "extra": "Não sei oq colocar aqui"
    }
  ]
}
```
Inicie o servidor na porta 3301:
```bash
npx json-server --watch db.json --port 3301
```

### 4. Iniciar os testes
Basta Rodar no terminal qual teste você quer fazer
```bash
python test_estress.py
``` 

## Atenção: este comando abrirá 100 abas reais no seu navegador padrão, Feche abas importantes antes de iniciar 
```bash
python test_estressweb.py
```

## Observação: test_estress.py analisa o tempo em ms que a requisição da API é respondida, enquanto o test_estressweb.py analisa o tempo em ms que a página da API carrega
