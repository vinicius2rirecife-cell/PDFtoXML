from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pdfplumber

def _extract_text(pdf_path: Path) -> str:
    texts: list[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            texts.append(page_text)
    text = "\n".join(texts)
    if not text.strip():
        raise ValueError(
            "Não foi possível extrair texto do PDF. "
            "Se o PDF for escaneado como imagem, será preciso adicionar OCR."
        )
    return text

def _first_match(patterns: list[str], text: str, flags: int = re.IGNORECASE) -> str:
    for pattern in patterns:
        m = re.search(pattern, text, flags)
        if m:
            return m.group(1).strip()
    return ""

def _normalize_number(value: str) -> str:
    if not value:
        return ""
    cleaned = value.replace(".", "").replace("R$", "").replace(" ", "").strip()
    cleaned = cleaned.replace(",", ".")
    return cleaned

def extract_from_pdf(pdf_path: Path) -> dict[str, Any]:
    text = _extract_text(pdf_path)

    data_instrumento = _first_match([
        r"data do instrumento[:\s]+(\d{2}/\d{2}/\d{4})",
        r"em\s+(\d{2}/\d{2}/\d{4})",
        r"(\d{2}/\d{2}/\d{4})",
    ], text)

    numero_contrato = _first_match([
        r"n[úu]mero do contrato[:\s]+([0-9.\-/]+)",
        r"contrato[:\s]+([0-9.\-/]+)",
    ], text)

    local = _first_match([
        r"local[:\s]+([A-ZÇÁÉÍÓÚÂÊÔÃÕa-zçáéíóúâêôãõ/\- ]+)",
    ], text)

    valor_negocio = _normalize_number(_first_match([
        r"valor (?:do )?(?:neg[oó]cio|im[oó]vel|venda e compra)[:\s]+R?\$?\s*([\d\.,]+)",
        r"preço[:\s]+R?\$?\s*([\d\.,]+)",
    ], text))

    valor_financiamento = _normalize_number(_first_match([
        r"valor (?:do )?financiamento[:\s]+R?\$?\s*([\d\.,]+)",
    ], text))

    recursos_proprios = ""
    if valor_negocio and valor_financiamento:
        try:
            recursos_proprios = f"{float(valor_negocio) - float(valor_financiamento):.2f}"
        except ValueError:
            recursos_proprios = ""

    matricula = _first_match([
        r"matr[íi]cula[:\sº°n]*([0-9.\-]+)",
        r"matr[íi]cula n[º°]?\s*([0-9.\-]+)",
    ], text)

    endereco_imovel = _first_match([
        r"endere[çc]o do im[oó]vel[:\s]+(.+)",
    ], text)

    comprador_nome = _first_match([
        r"comprador[a]?:\s*(.+)",
        r"adquirente[:\s]+(.+)",
    ], text)

    comprador_cpf = _first_match([
        r"comprador[a]?:.*?cpf[:\s]+([\d.\-]+)",
        r"adquirente.*?cpf[:\s]+([\d.\-]+)",
        r"cpf[:\s]+([\d.\-]{11,18})",
    ], text)

    vendedor_nome = _first_match([
        r"vendedor[a]?(?:es)?:\s*(.+)",
        r"transmitente[:\s]+(.+)",
    ], text)

    vendedor_cpf = _first_match([
        r"vendedor[a]?(?:es)?:.*?cpf[:\s]+([\d.\-]+)",
        r"transmitente.*?cpf[:\s]+([\d.\-]+)",
    ], text)

    banco_nome = _first_match([
        r"(caixa econ[oô]mica federal)",
        r"(banco do brasil)",
        r"(bradesco)",
        r"(ita[uú])",
        r"(santander)",
    ], text)

    banco_cnpj = _first_match([
        r"cnpj do credor[:\s]+([\d./\-]+)",
        r"credor.*?cnpj[:\s]+([\d./\-]+)",
    ], text)

    prazo_amortizacao = _first_match([
        r"prazo(?: de)? amortiza[çc][ãa]o[:\s]+(\d+)",
        r"prazo[:\s]+(\d+)\s*meses",
    ], text)

    juros_anual_nominal = _normalize_number(_first_match([
        r"juros anual nominal[:\s]+([\d\.,]+)",
        r"taxa nominal[:\s]+([\d\.,]+)",
    ], text))

    juros_anual_efetivo = _normalize_number(_first_match([
        r"juros anual efetivo[:\s]+([\d\.,]+)",
        r"taxa efetiva[:\s]+([\d\.,]+)",
    ], text))

    data_primeira_parcela = _first_match([
        r"primeira parcela[:\s]+(\d{2}/\d{2}/\d{4})",
        r"data da primeira parcela[:\s]+(\d{2}/\d{2}/\d{4})",
    ], text)

    valor_primeira_parcela = _normalize_number(_first_match([
        r"valor da primeira parcela[:\s]+R?\$?\s*([\d\.,]+)",
        r"encargo mensal.*?R?\$?\s*([\d\.,]+)",
    ], text))

    if banco_nome.lower() == "caixa econômica federal" and not banco_cnpj:
        banco_cnpj = "00360305000104"

    return {
        "raw_text": text,
        "data_instrumento": data_instrumento,
        "numero_contrato": numero_contrato,
        "local": local or "RECIFE/PE",
        "valor_negocio": valor_negocio,
        "valor_financiamento": valor_financiamento,
        "recursos_proprios": recursos_proprios,
        "matricula": matricula,
        "endereco_imovel": endereco_imovel,
        "comprador_nome": comprador_nome,
        "comprador_cpf": re.sub(r"\D", "", comprador_cpf),
        "vendedor_nome": vendedor_nome,
        "vendedor_cpf": re.sub(r"\D", "", vendedor_cpf),
        "banco_nome": banco_nome.upper(),
        "banco_cnpj": re.sub(r"\D", "", banco_cnpj),
        "prazo_amortizacao": prazo_amortizacao,
        "juros_anual_nominal": juros_anual_nominal,
        "juros_anual_efetivo": juros_anual_efetivo,
        "data_primeira_parcela": data_primeira_parcela,
        "valor_primeira_parcela": valor_primeira_parcela,
    }
