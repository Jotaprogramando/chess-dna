# Chess DNA - Plataforma Completa de Análise de Xadrez

Uma plataforma profissional de análise de performance em xadrez usando **Machine Learning, Clustering e Dashboard Interativo**. Perfila o estilo de jogo e compara com legendários Grandes Mestres.

## 🎯 Objetivos

O **Chess DNA** analisa seu desempenho em xadrez através de:

1. **Análise de Partidas PGN** 
   - ACPL (Average Centipawn Loss)
   - Mega Blunders (>300 cp)
   - Análise por fase (Abertura, Meio de Jogo, Final)

2. **Machine Learning - Perfil de DNA**
   - 10 features técnicas extraídas automaticamente
   - Comparação com 6 Grandes Mestres famosos
   - Distribuição percentual de estilo
   - Análise psicológica sob pressão de tempo

3. **Dashboard Interativo Streamlit**
   - Blunder Heatmap (Fase vs. Centipawns)
   - Gráfico de Radar (4 dimensões de estilo)
   - Timeline de Precisão com mega blunders
   - Análise completa de DNA com visualizações

## 📋 Versão Atual

**Chess DNA v0.3.0** - Incluindo módulo Player DNA  
Data de Lançamento: 15 de Janeiro de 2026  
Status: ✅ Produção  

## 📦 Módulos Disponíveis

| Módulo | Descrição | Status |
|--------|-----------|--------|
| **ChessProfiler** | Análise de partidas PGN com Stockfish | ✅ v0.1.0 |
| **StockfishManager** | Gerenciador cross-platform do motor | ✅ v0.1.0 |
| **Dashboard Streamlit** | Visualizações interativas | ✅ v0.2.0 |
| **PlayerDNA** ⭐ | Machine Learning - Perfil de Estilo | ✅ v0.3.0 |
| **PressaoTempoAnalyzer** ⭐ | Análise psicológica | ✅ v0.3.0 |
| **DatasetGenerator** | Geração de dados de análise | ✅ v0.2.0 |

## 🧬 Novo: Módulo Player DNA (v0.3.0)

### Feature Engineering
Extrai 10 características técnicas de um DataFrame de análise:

```python
from src.player_dna import FeatureEngineer

features = FeatureEngineer.calcular_features_do_dataset(df)
# Output: {
#   'agressividade': 65.3,
#   'solidez': 82.1,
#   'precisao': 78.4,
#   'velocidade_decisao': 85.2,
#   ... (6 mais features)
# }
```

### Análise de DNA com Machine Learning
Compara seu estilo com legendários Grandes Mestres:

```python
from src.player_dna import get_player_dna

dna = get_player_dna(df_analysis, tempo_limite=30)

print(dna['estilo_principal'])
# Output: ('Magnus Carlsen', 48.5)
#         (Nome GM, Percentual)

print(dna['dna'])
# Output: {
#   'Magnus Carlsen': 48.5,
#   'Garry Kasparov': 25.3,
#   'José Raúl Capablanca': 18.2,
#   ... (mais 3 GMs)
# }
```

### Algoritmos de Clustering
- **Similaridade de Cosseno**: Score 0-1 para cada GM
- **K-Nearest Neighbors**: Top 3 estilos mais similares
- **Normalização StandardScaler**: Peso igual para features

### Grandes Mestres Inclusos

| Mestre | Era | Estilo Principal |
|--------|-----|-----------------|
| **Magnus Carlsen** | 1990-Atual | Dinâmico e Preciso |
| **Garry Kasparov** | 1963-Atual | Agressivo e Tático |
| **José Raúl Capablanca** | 1888-1942 | Clássico Posicional |
| **Mikhail Tal** | 1936-2000 | Ultra Tático |
| **Tigran Petrosian** | 1929-1984 | Defensivo Sólido |
| **Anatoly Karpov** | 1951-Atual | Especialista em Finais |

### Análise Psicológica
Compara desempenho sob pressão de tempo:

```python
pressao = dna['pressao_tempo']
# Retorna:
# {
#   'com_pressao': {'acpl_medio': 73.9, ...},
#   'sem_pressao': {'acpl_medio': 49.2, ...},
#   'psicologia': {
#     'reacao_tempo': '🔴 INSTÁVEL SOB PRESSÃO',
#     'taxa_sucesso': '⚠️ VULNERÁVEL'
#   }
# }
```

## 🚀 Instalação

### 1. Clone ou Crie o Projeto
```bash
cd chessDna
```

### 2. Crie Ambiente Virtual (Recomendado)
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Instale Dependências
```bash
pip install -r requirements.txt
```

### 4. Instale Stockfish
- **Windows**: https://stockfishchess.org/download/
- **Linux**: `sudo apt-get install stockfish`
- **macOS**: `brew install stockfish`

## 📖 Uso

### Opção 1: Via Dashboard Streamlit ⭐ (Recomendado)

```bash
streamlit run dashboard.py
```

Acessa automaticamente:
- Blunder Heatmap
- Gráfico de Radar
- Timeline de Precisão
- **Análise de DNA com 6 GMs** ⭐ (v0.3.0)

### Opção 2: Via Função Python

```python
from src.player_dna import get_player_dna
import pandas as pd

# Carregar análise de partidas
df = pd.read_csv('chess_analysis.csv')

# Análise completa de DNA
dna = get_player_dna(df, tempo_limite=30)

# Ver estilo principal
estilo, percentual = dna['estilo_principal']
print(f"Você joga como: {estilo} ({percentual:.1f}%)")
```

### Opção 3: Via Linha de Comando

```bash
python main.py --pgn data/partidas.pgn --user "username"
```

## 📊 Documentação Completa

| Arquivo | Conteúdo |
|---------|----------|
| **PLAYER_DNA_GUIDE.md** | ⭐ Guia completo do novo módulo DNA (500+ linhas) |
| **PLAYER_DNA_RELEASE.md** | ⭐ Notas de lançamento v0.3.0 |
| **DASHBOARD_GUIDE.md** | Guia do Dashboard Streamlit |
| **API_DOCUMENTATION.md** | Documentação de APIs |
| **GUIA_RAPIDO.md** | Quick start em 5 minutos |
| **ESTRUTURA_PROJETO.md** | Arquitetura técnica |

## 🧪 Testes e Validação

### Executar Testes do DNA

```bash
python teste_player_dna.py
```

Resultado esperado:
```
✅ Teste 1: Feature Engineering
✅ Teste 2: Dataset Vazio  
✅ Teste 3: Similaridade Cosseno
✅ Teste 4: KNN Estilos
✅ Teste 5: Distribuição Percentual
✅ Teste 6: Estilo Principal
✅ Teste 7: Pressão de Tempo
✅ Teste 8: Função Principal
✅ Teste 9: Relatório Texto
✅ Teste 10: Perfis de GMs

✅ TODOS OS 10 TESTES PASSARAM!
```

### Executar Exemplo

```bash
python exemplo_player_dna.py
```

## 🏗️ Estrutura do Projeto

```
chessDna/
├── src/
│   ├── __init__.py              # Exports v0.3.0
│   ├── stockfish_manager.py     # Motor Stockfish
│   ├── chess_profiler.py        # Análise de PGN
│   ├── player_dna.py            # ⭐ ML de DNA (NOVO)
│   └── utils.py                 # Utilidades
├── dashboard.py                 # Streamlit app
├── dashboard_dna_integration.py # ⭐ Integração DNA (NOVO)
├── dataset_generator.py         # Gerador de dados
├── integrador.py                # Pipeline de análise
├── main.py                      # CLI
│
├── exemplo_player_dna.py        # ⭐ Exemplo DNA (NOVO)
├── teste_player_dna.py          # ⭐ Testes DNA (NOVO)
│
├── data/
│   ├── exemplo_partidas.pgn
│   └── chess_analysis_detailed.csv
├── results/                     # Outputs
│
├── PLAYER_DNA_GUIDE.md          # ⭐ Guia DNA (NOVO)
├── PLAYER_DNA_RELEASE.md        # ⭐ Release DNA (NOVO)
├── DASHBOARD_GUIDE.md
├── API_DOCUMENTATION.md
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências
└── CHANGELOG.md
```

## 🔧 Dependências Principais

```
python-chess==1.10.0             # Parsing PGN
pandas>=2.0.0                    # Análise de dados
stockfish>=16.0                  # Motor xadrez
numpy>=1.24.0                    # Numéricos
scikit-learn>=1.3.0              # ⭐ ML - NOVO
streamlit>=1.28.0                # Dashboard
plotly>=5.17.0                   # Visualizações
matplotlib>=3.7.0
seaborn>=0.12.0
```

## 📈 Performance

| Operação | Tempo |
|----------|-------|
| Feature Extraction | ~100ms |
| Similaridade Cosseno | ~10ms |
| KNN (k=3) | ~20ms |
| Análise Pressão | ~30ms |
| **Total DNA** | **~200ms** |

## 🎯 Casos de Uso

1. **Identificar seu estilo pessoal**
   ```python
   dna['estilo_principal']  # Qual GM você mais se parece?
   ```

2. **Encontrar fraquezas**
   ```python
   dna['features']['solidez']  # Preciso melhorar defesa?
   ```

3. **Analisar pressão psicológica**
   ```python
   dna['pressao_tempo']['psicologia']
   ```

4. **Comparar com outros jogadores**
   ```python
   for jogador, df in jogadores.items():
       dna = get_player_dna(df)
       print(f"{jogador}: {dna['estilo_principal']}")
   ```

## 📞 Suporte e Documentação

### Para DNA (v0.3.0) ⭐
- Leia: [PLAYER_DNA_GUIDE.md](PLAYER_DNA_GUIDE.md)
- Exemplo: [exemplo_player_dna.py](exemplo_player_dna.py)
- Testes: [teste_player_dna.py](teste_player_dna.py)

### Para Dashboard
- Leia: [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md)

### Para Análise PGN
- Leia: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 🚀 Próximas Versões

**v0.4.0** (Planejado):
- Integração completa de DNA no Dashboard
- Mais visualizações de estilo
- Análise por fase específica

**v0.5.0+** (Futuro):
- Redes Neurais para features automáticas
- Clustering com K-means
- API REST
- Integração Chess.com/Lichess

## 📝 Changelog

Veja [CHANGELOG.md](CHANGELOG.md) para histórico completo.

### v0.3.0
- ⭐ Novo módulo Player DNA com ML
- ⭐ 10 features técnicas automatizadas
- ⭐ Comparação com 6 Grandes Mestres
- ⭐ Análise psicológica de pressão
- ⭐ Similaridade de Cosseno + KNN
- Suite de 10 testes (100% passing)
- Documentação completa (500+ linhas)

## 🏆 Status do Projeto

- ✅ Análise PGN com Stockfish
- ✅ Dashboard Streamlit
- ✅ **Machine Learning e DNA** (NEW v0.3.0)
- ✅ Testes automatizados
- ✅ Documentação completa
- 🔄 Integração DNA no Dashboard (v0.4.0)
- 🔄 API REST (v0.5.0+)

## 📄 Licença

MIT License

## 👨‍💻 Desenvolvido por

Chess DNA Development Team  
Especialização: Análise de Xadrez com ML

## 🔧 Arquitetura

### StockfishManager
Gerencia a localização e inicialização do motor Stockfish:
- Procura automaticamente o executável no sistema
- Suporta Windows, Linux e macOS
- Gerencia ciclo de vida do motor (inicialização e encerramento)

### ChessProfiler
Classe principal que realiza a análise:
- Lê e parseia arquivos PGN
- Identifica partidas do usuário
- Análise movimento a movimento
- Calcula métricas ACPL e Blunders

### Utils
Funções auxiliares:
- Validação de arquivos PGN
- Geração de relatórios
- Exportação de resultados (CSV/XLSX)
- Análise de aberturas

## ⚠️ Tratamento de Erros

O programa trata os seguintes cenários:

1. **Stockfish não encontrado**
   ```
   ❌ Stockfish não foi encontrado no sistema.
   Por favor, instale o Stockfish de: https://stockfishchess.org/download/
   ```

2. **Arquivo PGN inválido**
   ```
   ❌ Arquivo PGN inválido ou corrompido: data/arquivo.pgn
   ```

3. **Usuário não encontrado**
   ```
   ❌ Nenhuma partida do usuário 'Username' encontrada no arquivo PGN
   ```

## 📝 Exemplo de Arquivo PGN

```pgn
[Event "Chess.com"]
[Site "Chess.com"]
[Date "2024.01.15"]
[Round "?"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]
[Opening "Ruy Lopez"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 ...
```

## 🔍 Métricas Explicadas

### ACPL (Average Centipawn Loss)
Média aritmética da perda de centipawns por movimento.
- **< 30 cp**: Desempenho excelente
- **30-50 cp**: Desempenho muito bom
- **50-80 cp**: Desempenho bom
- **> 80 cp**: Desempenho que precisa de melhoria

### Mega Blunders
Movimentos onde o jogador pierde > 300 centipawns de uma só vez.
Indicam erros significativos na partida.

## 🐛 Debugging

### Aumentar Tempo de Análise
Para análise mais profunda (mais precisa, mas mais lenta):
```bash
python main.py --pgn data/partidas.pgn --user "Username" --tempo 2.0
```

### Salvar em Excel
```bash
python main.py --pgn data/partidas.pgn --user "Username" --formato xlsx
```

## 📚 Referências

- [python-chess Documentation](https://python-chess.readthedocs.io/)
- [Stockfish Documentation](https://stockfishchess.org/)
- [Pandas Documentation](https://pandas.pydata.org/)

## 📄 Licença

Projeto aberto sob licença MIT.

## 👤 Autor

Desenvolvido como ferramenta de análise de dados de xadrez.

---

**Dúvidas ou sugestões?** Abra uma issue no repositório!
