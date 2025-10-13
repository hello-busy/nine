#!/usr/bin/env python3
"""
Giara persona skill for Muse: a merged, capability-rich assistant that knows how to evaluate equations,
handle learner commands (observe/train/predict/status), and respond like a grounded chatbot.
All operations are local, deterministic, and safe.
"""
from typing import List, Tuple
import re
from scripts.muse import equations
from scripts.muse.skills import learner_skill
from scripts.muse import muse_utils
from scripts.muse.skill_router import get_response as router_response

# Lightweight intent patterns
_RE_EQUATION = re.compile(r"\b(calc|calculate|solve|equation|eval|evaluate|sin\(|cos\(|tan\(|sqrt\()", re.I)
_RE_LEARN = re.compile(r"\b(observe|train|predict|status)\b", re.I)
_RE_GIARA = re.compile(r"\bgiara\b", re.I)

VOICE_TEMPLATE = "Giara — an offline, logical assistant:\n{body}"

def _safe_eval_equation(text: str):
    # extract expression after keywords if present
    # common forms: "calc 2+2", "evaluate sin(3.14)", or just an expression
    # remove leading trigger words
    t = re.sub(r'^(calc|calculate|solve|evaluate|eval)\s*', '', text, flags=re.I).strip()
    # if the message contains words, try to find the subexpression within backticks or parentheses
    # fallback: use whole text
    expr = t
    try:
        val = equations.evaluate(expr)
        return f"= {{val}}"
    except Exception as e:
        return f"(equation error) {{e}}"

def respond(user_text: str, memories: List[Tuple[str, str]], context: dict) -> str:
    ut = user_text.strip()
    # 1) explicit Giara invocation or persona-tagging
    if _RE_GIARA.search(ut) and not _RE_LEARN.search(ut) and not _RE_EQUATION.search(ut):
        # remove the token and treat rest as normal prompt
        cleaned = _RE_GIARA.sub('', ut).strip()
        if not cleaned:
            cleaned = "Hello — I'm Giara. How can I help?"
        # let router/gpt_like generate a polished reply but tag as Giara
        body = router_response(cleaned, memories, context)
        return VOICE_TEMPLATE.format(body=body)

    # 2) equations/number crunching
    if _RE_EQUATION.search(ut):
        eq_resp = _safe_eval_equation(ut)
        return VOICE_TEMPLATE.format(body=f"I evaluated your expression: {{eq_resp}}")

    # 3) learner commands: delegate to learner_skill
    if _RE_LEARN.search(ut):
        # pass db context if available
        local_ctx = dict(context or {})
        if 'db_path' not in local_ctx:
            from pathlib import Path
            local_ctx['db_path'] = str(Path.home() / '.muse_db.sqlite3')
        lr = learner_skill.respond(ut, memories, local_ctx)
        return VOICE_TEMPLATE.format(body=lr)

    # 4) fallback — prefer GPT-like structured response but include memories
    # call the router (which will pick a persona if needed)
    body = router_response(ut, memories, context)
    return VOICE_TEMPLATE.format(body=body)