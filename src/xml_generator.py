from __future__ import annotations
from xml.sax.saxutils import escape

def tag(name: str, value: str | None) -> str:
    if value is None or str(value).strip() == "":
        return f"<{name}/>"
    return f"<{name}>{escape(str(value))}</{name}>"

def generate_xml(data: dict, template_type: str) -> str:
    if template_type == "compra_simples":
        return _compra_simples(data)
    if template_type == "alienacao_fiduciaria":
        return _alienacao_fiduciaria(data)
    return _compra_financiamento(data)

def _compra_simples(data: dict) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<TITULOS>
  <VERSAO>3.5.0</VERSAO>
  <CONTRATOS>
    <CONTRATO>
      <NATUREZA>1</NATUREZA>
      {tag("DATAINSTRUMENTO", data.get("data_instrumento"))}
      {tag("NUMCONTRATO", data.get("numero_contrato"))}
      {tag("LOCAL", data.get("local"))}
      <NEGOCIOS>
        <NEGOCIO>
          <SEQUENCIAL>1</SEQUENCIAL>
          <TIPOATO>1</TIPOATO>
          {tag("VALORNEGOCIO", data.get("valor_negocio"))}
          <IMOVEIS>
            <IMOVEL>
              <LIVRO>1</LIVRO>
              {tag("NUMEROMATRICULA", data.get("matricula"))}
              <ENDERECO>{tag("COMPLEMENTO", data.get("endereco_imovel"))}</ENDERECO>
            </IMOVEL>
          </IMOVEIS>
          <PARTES>
            <PARTE><QUALIFICACAO>12</QUALIFICACAO>{tag("CPFCNPJ", data.get("vendedor_cpf"))}<FRACAO>100</FRACAO></PARTE>
            <PARTE><QUALIFICACAO>1</QUALIFICACAO>{tag("CPFCNPJ", data.get("comprador_cpf"))}<FRACAO>100</FRACAO></PARTE>
          </PARTES>
        </NEGOCIO>
      </NEGOCIOS>
      <PARTESNEGOCIO>
        <PARTE><QUALIFICACAO>12</QUALIFICACAO>{tag("NOME", data.get("vendedor_nome"))}{tag("CPFCNPJ", data.get("vendedor_cpf"))}</PARTE>
        <PARTE><QUALIFICACAO>1</QUALIFICACAO>{tag("NOME", data.get("comprador_nome"))}{tag("CPFCNPJ", data.get("comprador_cpf"))}</PARTE>
      </PARTESNEGOCIO>
    </CONTRATO>
  </CONTRATOS>
</TITULOS>
'''

def _compra_financiamento(data: dict) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<TITULOS>
  <VERSAO>3.5.0</VERSAO>
  <CONTRATOS>
    <CONTRATO>
      <NATUREZA>1</NATUREZA>
      {tag("DATAINSTRUMENTO", data.get("data_instrumento"))}
      {tag("NUMCONTRATO", data.get("numero_contrato"))}
      {tag("LOCAL", data.get("local"))}
      <NEGOCIOS>
        <NEGOCIO>
          <SEQUENCIAL>1</SEQUENCIAL>
          <TIPOATO>1</TIPOATO>
          {tag("VALORNEGOCIO", data.get("valor_negocio"))}
          <IMOVEIS><IMOVEL><LIVRO>1</LIVRO>{tag("NUMEROMATRICULA", data.get("matricula"))}<ENDERECO>{tag("COMPLEMENTO", data.get("endereco_imovel"))}</ENDERECO></IMOVEL></IMOVEIS>
          <PARTES>
            <PARTE><QUALIFICACAO>12</QUALIFICACAO>{tag("CPFCNPJ", data.get("vendedor_cpf"))}<FRACAO>100</FRACAO></PARTE>
            <PARTE><QUALIFICACAO>1</QUALIFICACAO>{tag("CPFCNPJ", data.get("comprador_cpf"))}<FRACAO>100</FRACAO></PARTE>
          </PARTES>
        </NEGOCIO>
        <NEGOCIO>
          <SEQUENCIAL>2</SEQUENCIAL>
          <TIPOATO>3</TIPOATO>
          {tag("VALORNEGOCIO", data.get("valor_financiamento"))}
          <IMOVEIS><IMOVEL><LIVRO>1</LIVRO>{tag("NUMEROMATRICULA", data.get("matricula"))}<ENDERECO>{tag("COMPLEMENTO", data.get("endereco_imovel"))}</ENDERECO></IMOVEL></IMOVEIS>
          <PARTES>
            <PARTE><QUALIFICACAO>5</QUALIFICACAO>{tag("CPFCNPJ", data.get("comprador_cpf"))}<FRACAO>100</FRACAO></PARTE>
            <PARTE><QUALIFICACAO>3</QUALIFICACAO>{tag("CPFCNPJ", data.get("banco_cnpj"))}<FRACAO>100</FRACAO></PARTE>
          </PARTES>
        </NEGOCIO>
      </NEGOCIOS>
      <VENDACOMPRA>
        {tag("VALORVENDACOMPRA", data.get("valor_negocio"))}
        {tag("VALORFINANCIAMENTO", data.get("valor_financiamento"))}
        {tag("RECURSOSPROPRIOS", data.get("recursos_proprios"))}
      </VENDACOMPRA>
      <FINANCIAMENTO>
        <DADOS>
          {tag("VALORFINANCIAMENTO", data.get("valor_financiamento"))}
          {tag("JUROSANUALNOMINAL", data.get("juros_anual_nominal"))}
          {tag("JUROSANUALEFETIVO", data.get("juros_anual_efetivo"))}
          {tag("PRAZOAMORTIZACAO", data.get("prazo_amortizacao"))}
          {tag("VALORPRIMEIRAPARCELA", data.get("valor_primeira_parcela"))}
          {tag("DATAPRIMEIRAPARCELA", data.get("data_primeira_parcela"))}
        </DADOS>
      </FINANCIAMENTO>
      <PARTESNEGOCIO>
        <PARTE><QUALIFICACAO>12</QUALIFICACAO>{tag("NOME", data.get("vendedor_nome"))}{tag("CPFCNPJ", data.get("vendedor_cpf"))}</PARTE>
        <PARTE><QUALIFICACAO>1</QUALIFICACAO>{tag("NOME", data.get("comprador_nome"))}{tag("CPFCNPJ", data.get("comprador_cpf"))}</PARTE>
        <PARTE><QUALIFICACAO>5</QUALIFICACAO>{tag("NOME", data.get("comprador_nome"))}{tag("CPFCNPJ", data.get("comprador_cpf"))}</PARTE>
        <PARTE><QUALIFICACAO>3</QUALIFICACAO>{tag("NOME", data.get("banco_nome"))}{tag("CPFCNPJ", data.get("banco_cnpj"))}</PARTE>
      </PARTESNEGOCIO>
      <GARANTIAS>
        <GARANTIA>
          <TIPOGARANTIA>0427</TIPOGARANTIA>
          <TIPOBEM>02</TIPOBEM>
          {tag("VALOR", data.get("valor_financiamento"))}
          <PERCENTUALCOMPROMETIDO>100</PERCENTUALCOMPROMETIDO>
          <GRAU>1</GRAU>
        </GARANTIA>
      </GARANTIAS>
    </CONTRATO>
  </CONTRATOS>
</TITULOS>
'''

def _alienacao_fiduciaria(data: dict) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<TITULOS>
  <VERSAO>3.5.0</VERSAO>
  <CONTRATOS>
    <CONTRATO>
      <NATUREZA>1</NATUREZA>
      {tag("DATAINSTRUMENTO", data.get("data_instrumento"))}
      {tag("NUMCONTRATO", data.get("numero_contrato"))}
      {tag("LOCAL", data.get("local"))}
      <NEGOCIOS>
        <NEGOCIO>
          <SEQUENCIAL>1</SEQUENCIAL>
          <TIPOATO>3</TIPOATO>
          {tag("VALORNEGOCIO", data.get("valor_financiamento"))}
          <IMOVEIS><IMOVEL><LIVRO>1</LIVRO>{tag("NUMEROMATRICULA", data.get("matricula"))}<ENDERECO>{tag("COMPLEMENTO", data.get("endereco_imovel"))}</ENDERECO></IMOVEL></IMOVEIS>
          <PARTES>
            <PARTE><QUALIFICACAO>5</QUALIFICACAO>{tag("CPFCNPJ", data.get("comprador_cpf"))}<FRACAO>100</FRACAO></PARTE>
            <PARTE><QUALIFICACAO>3</QUALIFICACAO>{tag("CPFCNPJ", data.get("banco_cnpj"))}<FRACAO>100</FRACAO></PARTE>
          </PARTES>
        </NEGOCIO>
      </NEGOCIOS>
      <FINANCIAMENTO>
        <DADOS>
          {tag("VALORFINANCIAMENTO", data.get("valor_financiamento"))}
          {tag("JUROSANUALNOMINAL", data.get("juros_anual_nominal"))}
          {tag("JUROSANUALEFETIVO", data.get("juros_anual_efetivo"))}
          {tag("PRAZOAMORTIZACAO", data.get("prazo_amortizacao"))}
          {tag("VALORPRIMEIRAPARCELA", data.get("valor_primeira_parcela"))}
          {tag("DATAPRIMEIRAPARCELA", data.get("data_primeira_parcela"))}
        </DADOS>
      </FINANCIAMENTO>
      <PARTESNEGOCIO>
        <PARTE><QUALIFICACAO>5</QUALIFICACAO>{tag("NOME", data.get("comprador_nome"))}{tag("CPFCNPJ", data.get("comprador_cpf"))}</PARTE>
        <PARTE><QUALIFICACAO>3</QUALIFICACAO>{tag("NOME", data.get("banco_nome"))}{tag("CPFCNPJ", data.get("banco_cnpj"))}</PARTE>
      </PARTESNEGOCIO>
      <GARANTIAS>
        <GARANTIA>
          <TIPOGARANTIA>0427</TIPOGARANTIA>
          <TIPOBEM>02</TIPOBEM>
          {tag("VALOR", data.get("valor_financiamento"))}
          <PERCENTUALCOMPROMETIDO>100</PERCENTUALCOMPROMETIDO>
          <GRAU>1</GRAU>
        </GARANTIA>
      </GARANTIAS>
    </CONTRATO>
  </CONTRATOS>
</TITULOS>
'''
