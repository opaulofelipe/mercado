# Mercado

Lista de mercado em Python + Streamlit, redesenhada com foco em simplicidade, leitura rápida e interação direta.

## Direção de interface

A interface segue uma lógica de lista de tarefas:

- navegação simples por **Minha lista**, **Pendentes** e **Concluídos**;
- adição rápida de item no topo;
- quantidade, unidade e categoria ficam como detalhes opcionais;
- cada item tem uma ação principal clara: marcar como concluído;
- edição aparece apenas quando solicitada;
- itens concluídos ficam recolhidos na visualização principal;
- sem dashboards, cards de métricas ou elementos decorativos desnecessários.

## Paleta

- `#9EE493` — estado/acento positivo
- `#DAF7DC` — superfícies de seleção e apoio
- `#ABC8C0` — bordas e separadores
- `#70566D` — texto secundário e acentos
- `#42273B` — texto principal e alto contraste

## Estrutura

```text
mercado/
├── app.py
├── database.py
├── styles.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── README.md
```

## Executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

O arquivo `mercado.db` é criado automaticamente na primeira execução.

> Observação: em hospedagens com sistema de arquivos efêmero, SQLite pode ser apagado quando a instância reinicia. Para persistência em produção, use um banco externo.
