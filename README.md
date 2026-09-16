# Mercado

Lista de compras em **Python + Streamlit**, com interface mobile-first inspirada em aplicativos de tarefas.

## Persistência

Não usa banco de dados. A lista é salva diretamente no **localStorage do navegador**.

Isso significa que:

- os itens permanecem após fechar e abrir o navegador;
- cada navegador/dispositivo mantém sua própria lista;
- limpar os dados do site no navegador também apaga a lista;
- nenhum banco precisa ser configurado no servidor.

## Interação

- cada item possui um seletor circular à esquerda;
- tocar no seletor marca o item como concluído e tacha o texto;
- tocar novamente devolve o item para pendente;
- segurar o item por aproximadamente meio segundo revela a lixeira;
- tocar na lixeira exclui o item;
- após excluir, há opção de desfazer;
- quantidade, unidade e categoria são opcionais;
- a interface é responsiva para celular, tablet e desktop.

## Estrutura

O projeto usa apenas `app.py` e o próprio Streamlit. A interface interativa é entregue pelo Python dentro de um iframe do mesmo app, permitindo usar o armazenamento local do navegador sem dependências externas.

## Executar

```bash
pip install -r requirements.txt
streamlit run app.py
```
