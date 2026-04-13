PDF para XML Asgard
Projeto simples para:
subir um PDF
extrair dados principais
gerar XML base para Asgard
O que ele faz
Interface web em Flask
Leitura de PDF com texto usando `pdfplumber`
Geração de XML para 3 cenários:
compra simples
compra + financiamento
alienação fiduciária
Limitações
Este projeto funciona melhor com PDF nativo com texto
Para PDF escaneado por imagem, será preciso adicionar OCR
Os padrões de extração estão em `src/extractor.py` e podem precisar de ajuste para o layout do seu contrato
Instalação
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```
Acesse:
`http://127.0.0.1:5000`
Estrutura
`app.py`: servidor Flask
`templates/index.html`: tela de upload
`src/extractor.py`: extrai dados do PDF
`src/validators.py`: valida dados mínimos
`src/xml_generator.py`: monta o XML
Como adaptar
Se o contrato tiver outro padrão, ajuste os regex em:
`src/extractor.py`
Próximos passos recomendados
adicionar OCR para PDF escaneado
criar formulário de revisão antes de gerar XML
salvar histórico das gerações
adicionar autenticação interna