#!/usr/bin/env python3
"""Valida noticias/*.md contra o FORMATO.md do Orceu Radar. Uso: validar_noticia.py arq1.md [arq2.md ...] [--hoje AAAA-MM-DD]"""
import re, sys, datetime, pathlib
import yaml

CATS = {"gestao-e-obras", "mercado-e-economia", "inovacao-e-ia"}
CTAS = {"copiloto", "treinamentos", "comunidade", "hub"}
UFS = set("AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split())
REQ = ["title", "meta_title", "subtitle", "resumo", "slug", "categoria", "date", "tempo_leitura", "fonte", "fonte_url", "cta_produto"]
FINAL = "### O que isso representa para o setor"

JANELA = 7  # dias (Arthur ampliou de 48h para 7 dias em 14/10/2026)

def validate(path, hoje):
    errs, warns = [], []
    p = pathlib.Path(path)
    t = p.read_text(encoding="utf-8")
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", t, re.S)
    if not m:
        return ["sem frontmatter delimitado por ---"], warns
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        return [f"YAML inválido: {e}"], warns
    body = m.group(2)
    for k in REQ:
        v = meta.get(k)
        if v is None or (isinstance(v, str) and not v.strip()):
            errs.append(f"campo obrigatório ausente ou vazio: {k}")
    if errs:
        return errs, warns
    for k in ("title","meta_title","subtitle","resumo","slug","categoria","date","fonte","fonte_url","cta_produto"):
        if not isinstance(meta[k], str):
            errs.append(f"{k} deve ser texto entre aspas")
    if errs:
        return errs, warns
    if len(meta["meta_title"]) > 70: errs.append(f"meta_title com {len(meta['meta_title'])} caracteres (máx 70)")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", meta["slug"]): errs.append("slug deve ter só minúsculas, números e hífens")
    if meta["slug"] != p.stem: errs.append(f"slug ({meta['slug']}) diferente do nome do arquivo ({p.stem})")
    if re.search(r"\d{4}-\d{2}-\d{2}", p.stem): errs.append("nome do arquivo não deve ter data")
    if meta["categoria"] not in CATS: errs.append(f"categoria inválida: {meta['categoria']}")
    try:
        d = datetime.date.fromisoformat(meta["date"])
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["date"]) is None: raise ValueError
        if hoje and (hoje - d).days > JANELA: errs.append(f"date {meta['date']} fora da janela de {JANELA} dias")
        if hoje and d > hoje: errs.append(f"date {meta['date']} no futuro")
    except Exception:
        errs.append("date deve ser AAAA-MM-DD válido")
    tl = meta["tempo_leitura"]
    if not (isinstance(tl, int) and not isinstance(tl, bool) and 1 <= tl <= 60): errs.append("tempo_leitura deve ser inteiro de 1 a 60")
    if not re.match(r"https?://[^\s]+\.[^\s]+", meta["fonte_url"]): errs.append("fonte_url inválido")
    if meta["cta_produto"] not in CTAS: errs.append(f"cta_produto inválido: {meta['cta_produto']}")
    est = meta.get("estado", "")
    if est not in ("", None) and est not in UFS: errs.append(f"estado inválido: {est}")
    img = meta.get("imagem", "")
    if img not in ("", None):
        if not str(img).startswith("https://"): errs.append("imagem deve ser URL https ou vazio")
        if not str(meta.get("imagem_credito", "") or "").strip(): errs.append("imagem_credito obrigatório quando há imagem")
    tags = meta.get("tags")
    if tags is not None and not (isinstance(tags, list) and all(isinstance(x, str) for x in tags)): errs.append("tags deve ser lista de textos")
    if FINAL not in body:
        errs.append(f'falta a seção final "{FINAL}"')
    else:
        after = body.split(FINAL, 1)[1].strip()
        if len(after) < 40: errs.append("seção final sem texto")
        if re.search(r"^#{1,6} ", after, re.M): warns.append("há títulos depois da seção final (ela deve ser a última)")
    if "—" in t or "–" in t: errs.append("travessão encontrado (regra da marca)")
    if re.search(r"\bnão é\b[^.\n]{0,80}\bé\b", t, re.I): errs.append('padrão "não é X, é Y" (regra da marca)')
    if re.search(r"\bsoftware\b", t, re.I): errs.append('usar "tecnologia", não "software" (regra da marca)')
    return errs, warns

if __name__ == "__main__":
    args = sys.argv[1:]
    hoje = None
    if "--hoje" in args:
        i = args.index("--hoje"); hoje = datetime.date.fromisoformat(args[i+1]); del args[i:i+2]
    bad = 0
    for f in args:
        e, w = validate(f, hoje)
        print(("OK   " if not e else "ERRO ") + f)
        for x in e: print("   -", x)
        for x in w: print("   ~", x)
        bad += bool(e)
    sys.exit(1 if bad else 0)
