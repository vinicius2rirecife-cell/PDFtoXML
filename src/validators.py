from __future__ import annotations

def validate_data(data: dict, template_type: str) -> None:
    required_by_template = {
        "compra_simples": [
            "data_instrumento", "numero_contrato", "comprador_nome", "comprador_cpf",
            "vendedor_nome", "vendedor_cpf", "valor_negocio", "matricula",
        ],
        "compra_financiamento": [
            "data_instrumento", "numero_contrato", "comprador_nome", "comprador_cpf",
            "vendedor_nome", "vendedor_cpf", "valor_negocio", "valor_financiamento",
            "matricula", "banco_nome", "banco_cnpj",
        ],
        "alienacao_fiduciaria": [
            "data_instrumento", "numero_contrato", "comprador_nome", "comprador_cpf",
            "valor_financiamento", "matricula", "banco_nome", "banco_cnpj",
        ],
    }

    missing = [field for field in required_by_template.get(template_type, []) if not data.get(field)]
    if missing:
        raise ValueError(
            "Campos não encontrados no PDF ou não informados manualmente: " + ", ".join(missing)
        )

    for field in ("comprador_cpf", "vendedor_cpf"):
        value = data.get(field, "")
        if value and len(value) not in (11, 14):
            raise ValueError(f"Campo {field} parece inválido: {value}")

    banco_cnpj = data.get("banco_cnpj", "")
    if banco_cnpj and len(banco_cnpj) != 14:
        raise ValueError(f"CNPJ do credor parece inválido: {banco_cnpj}")
