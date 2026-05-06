import re
import unicodedata


def normalize(text: str):

    text = text.lower()

    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# OFENSAS
# =========================

INSULT_ROOTS = [
    "burr", "idiot", "imbecil", "retard", "estupid",
    "lixo", "inutil", "merd", "porcar",
    "babac", "otari", "fdp",
    "fuck", "shit", "bitch", "asshol"
]

# =========================
# VIOLÊNCIA / ARMAS
# =========================

WEAPON_ROOTS = [
    "bomba",
    "explosiv",
    "dinamit",
    "granad",
    "arma",
    "pistol",
    "rifl",
    "ak47",
    "molotov",
    "detonador",
    "polvora",
    "napalm"
]

# =========================
# ATIVIDADE ILEGAL
# =========================

ILLEGAL_ROOTS = [
    "hackear",
    "invadir",
    "clonar",
    "cartao",
    "fraude",
    "lavagem",
    "droga",
    "trafico"
]

# =========================
# AUTO-DANO
# =========================

SELF_HARM_ROOTS = [
    "suicid",
    "me matar",
    "morrer",
    "acabar com minha vida"
]


# =========================
# CONSULTAS MÉDICAS
# =========================

MEDICAL_ROOTS = [
    "emagrecer",
    "dieta",
    "remedio",
    "medic",
    "doenca",
    "tratamento",
    "diagnostic"
]


# =========================
# PERGUNTAS PESSOAIS
# =========================

PERSONAL_PATTERNS = [
    r"minha\s+nota",
    r"minha\s+vida",
    r"minha\s+familia",
    r"posso\s+mentir"
]


# =========================
# GUARDRAIL
# =========================

def check_guardrails(text: str):

    norm = normalize(text)


    for root in INSULT_ROOTS:
        if root in norm:
            return False, (
                "⚠️ Linguagem ofensiva detectada."
            )


    for root in MEDICAL_ROOTS:
        if root in norm:
            return False, (
                "⚠️ Este sistema educacional não fornece orientação médica."
            )


    for pattern in PERSONAL_PATTERNS:
        if re.search(pattern, norm):
            return False, (
                "⚠️ Esta plataforma é destinada apenas a dúvidas educacionais."
            )
    

    for root in WEAPON_ROOTS:
        if root in norm:
            return False, (
            "⚠️ Este sistema educacional não pode ajudar com armas ou violência."
        )


    for root in ILLEGAL_ROOTS:
        if root in norm:
            return False, (
            "⚠️ Esta plataforma não fornece ajuda para atividades ilegais."
        )


    for root in SELF_HARM_ROOTS:
        if root in norm:
         return False, (
            "⚠️ Se você estiver passando por um momento difícil, procure ajuda profissional ou alguém de confiança."
        )

    return True, ""