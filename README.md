# Herdeiro do Destino

Uma visual novel interativa desenvolvida em Python usando Tkinter.

## Requisitos

- Python 3.8+
- Pillow (PIL) - Para processamento de imagens
- Pygame - Para sistema de áudio
- Tkinter - Para interface gráfica
- Sistema operacional com interface gráfica (Windows, Linux com X11, macOS)

## Arquivos de Áudio

O jogo espera os seguintes arquivos de áudio:

```
assets/
├── sounds/
│   ├── click.wav    - Som de clique
│   ├── type.wav     - Som de digitação
│   ├── transition.wav - Som de transição
│   ├── save.wav     - Som de salvamento
│   └── load.wav     - Som de carregamento
└── music/
    └── background.mp3 - Música de fundo
```

Nota: Os arquivos de áudio não estão incluídos no repositório. Você precisa fornecer seus próprios arquivos de som nos formatos correspondentes.

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar

```bash
python main.py
```

**Importante**: É necessário um ambiente com interface gráfica para executar o jogo.

## Características Técnicas

- Arquitetura Modular:
  - Sistema de capítulos extensível
  - Classe base reutilizável
  - Componentes independentes
  - Fácil adição de novos capítulos

- Otimizações:
  - Cache de imagens
  - Gerenciamento de memória
  - Transições suaves
  - Carregamento eficiente

- Sistema de salvamento/carregamento:
  - Salvamento manual
  - Auto-save configurável
  - Carregamento com preview
  - Gerenciamento de estados do jogo

- Narrativa com imagens:
  - Suporte a múltiplos capítulos
  - Sistema de transições suaves
  - Controle de progresso

- Animações e efeitos visuais:
  - Transições suaves entre cenas
  - Efeitos de fade in/out nas imagens
  - Animações de texto configuráveis:
    - Velocidade ajustável
    - Avanço automático opcional
    - Clique para completar animação
  - Indicador visual de continuação animado

- Sistema de áudio:
  - Música de fundo
  - Efeitos sonoros para interações
  - Controles de volume independentes
  - Fade in/out em transições

- Interface e controles:
  - Tela cheia ou modo janela
  - Controles personalizáveis:
    - Mouse/Teclado para avançar
    - Ctrl+S para modo skip
    - Histórico de texto acessível
  - Menu de configurações completo
  - Tela de créditos

- Configurações:
  - Velocidade do texto
  - Volume de música e efeitos
  - Intervalo de auto-save
  - Modo de exibição
  - Avanço automático
  - Pular texto não lido
  - Histórico de texto (últimas 100 linhas)

## Estrutura do Projeto

```
HerdeirodoDestino/
├── assets/
│   ├── imagens/      - Imagens do jogo
│   ├── music/        - Músicas de fundo
│   └── sounds/       - Efeitos sonoros
├── chapters/
│   ├── base_chapter.py   - Classe base para capítulos
│   ├── one/
│   │   └── ato1/        - Primeiro ato
│   ├── two/
│   │   └── ato2/        - Segundo ato
│   └── three/
│       └── ato3/        - Terceiro ato
├── audio_manager.py      - Sistema de áudio
├── game_state.py        - Gerenciamento de estado
├── image_cache.py       - Cache de imagens
├── settings.py          - Sistema de configurações
├── screens.py           - Telas do jogo
└── main.py             - Ponto de entrada
├── assets/imagens/     # Imagens do jogo
├── chapters/one/ato1/  # Primeiro ato
├── saves/              # Arquivos de save
├── main.py            # Entrada do programa
├── game_state.py      # Gerenciamento de estado
└── screens.py         # Interface do usuário
```

## Próximas Atualizações

- Sons e música
- Sistema de escolhas
- Mais capítulos
- Melhorias visuais
- Configurações de texto
