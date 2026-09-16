# Mercado

Lista de compras em **Python + Streamlit**, com interface mobile-first inspirada em aplicativos de tarefas.

## Persistência

Não usa banco de dados. A lista é salva no **localStorage do navegador** por meio do componente `streamlit-local-storage`.

Isso significa que:

- os itens permanecem após fechar e abrir o navegador;
- cada navegador/dispositivo mantém sua própria lista;
- limpar os dados do site no navegador também apaga a lista;
- nenhum banco precisa ser configurado no servidor.

## Recursos

- adicionar itens rapidamente;
- quantidade, unidade e categoria opcionais;
- concluir/desfazer conclusão;
- favoritar;
- editar e excluir;
- busca;
- seção recolhível de concluídos;
- interface responsiva para celular, tablet e desktop.

## Executar

```bash
pip install -r requirements.txt
streamlit run app.py
```
