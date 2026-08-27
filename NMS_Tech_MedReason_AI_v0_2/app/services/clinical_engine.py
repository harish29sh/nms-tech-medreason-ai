"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
import re
from .files import load_modules
MODULES=load_modules()

def _tokens(text:str):
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def choose_module(text:str):
    lower=text.lower(); tokens=_tokens(text); best=None; best_score=0
    for module in MODULES:
        score=0
        for alias in module["aliases"]:
            if alias in lower:
                score += 12 + len(alias.split())
            else:
                score += len(tokens & _tokens(alias))
        if score>best_score:
            best,best_score=module,score
    return (best,best_score) if best_score>0 else (None,0)

def rank_differentials(module,case_text:str):
    lower=case_text.lower(); weight={"high":4,"moderate":2,"lower":1}; ranked=[]
    for item in module["differentials"]:
        hits=[kw for kw in item["support_keywords"] if kw.lower() in lower]
        score=weight.get(item["base_priority"],1)+2*len(hits)
        ranked.append({"diagnosis":item["name"],"category":item["category"],"priority":item["base_priority"],"supporting_matches":hits,"score":score})
    return sorted(ranked,key=lambda x:x["score"],reverse=True)

def deterministic_analysis(case_text:str):
    module,confidence=choose_module(case_text)
    if not module:
        return {"module":None,"module_confidence":0,"syndrome":"Unclassified presentation","differential":[],"red_flags":[],"history_questions":[],"examination":[],"initial_evaluation":[],"reference_ids":["NMS-CORE-2026"]}
    return {"module":module["id"],"module_confidence":confidence,"specialty":module["specialty"],"syndrome":module["syndrome"],"differential":rank_differentials(module,case_text),"red_flags":module["red_flags"],"history_questions":module["key_history_questions"],"examination":module["focused_examination"],"initial_evaluation":module["initial_evaluation"],"reference_ids":module["reference_ids"]}

def module_context(module_id):
    for module in MODULES:
        if module["id"]==module_id:
            content="\n".join([f"Syndrome: {module['syndrome']}","Differentials: "+"; ".join(d["name"] for d in module["differentials"]),"Red flags: "+"; ".join(module["red_flags"]),"History: "+"; ".join(module["key_history_questions"]),"Examination: "+"; ".join(module["focused_examination"]),"Initial evaluation: "+"; ".join(module["initial_evaluation"])])
            return [{"id":f"fallback-{module_id}","title":module["syndrome"],"content":content,"source_ids":module["reference_ids"],"score":0.0}]
    return []
