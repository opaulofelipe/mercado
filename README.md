# Mercado

Aplicativo de lista de compras em Python + Streamlit, com interface minimalista inspirada na lógica visual do Microsoft To Do.

## Interface

- Lista principal simples e limpa
- Adição rápida de item
- Detalhes opcionais de categoria, quantidade e unidade
- Filtros por status e categoria
- Busca
- Itens concluídos separados dos pendentes
- Exclusão individual e limpeza dos concluídos
- Layout responsivo para desktop e celular

## Paleta

- `#9EE493`
- `#DAF7DC`
- `#ABC8C0`
- `#70566D`
- `#42273B`

As cores são usadas de forma discreta para não poluir a interface.

## Executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

O banco SQLite `mercado.db` é criado automaticamente na primeira execução.
