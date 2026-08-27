"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
from fastapi import APIRouter
from .schemas import AnalyzeRequest
from .services.case_text import patient_to_text
from .services.clinical_engine import deterministic_analysis
from .services.safety import detect_emergency_flags, emergency_preamble, strip_unverified_doses
from .services.rag import retrieve
from .services.citations import sources_for_ids, validate_citations
from .services.ollama import chat
from .services.imaging import imaging_safety_note
from .config import settings

router=APIRouter()

SYSTEM_PROMPT="""
You are NMS Tech MedReason AI, a clinician-facing clinical reasoning prototype.
Hard rules:
- Never claim diagnostic certainty from incomplete information.
- Never invent patient facts.
- Never invent citations, guideline titles, URLs, authors, pages or editions.
- Cite only the source IDs explicitly supplied in the prompt.
- Differentiate life-threatening diagnoses from common and lower-priority causes.
- Prefer asking for missing discriminating history/examination/results.
- Do not reproduce copyrighted textbook passages.
- Do not provide a patient-specific medication dose. Dose lines will be removed.
- Imaging/contrast recommendations must be conditional and tied to the clinical question.
- Local protocols, specialist/radiologist judgment and clinician assessment take priority.
"""

@router.get("/health")
def health():
    return {"status":"ok","app":settings.app_name,"version":settings.app_version}

@router.get("/modules")
def modules():
    from .services.files import load_modules
    return [{"id":m["id"],"specialty":m["specialty"],"syndrome":m["syndrome"]} for m in load_modules()]

@router.post("/analyze")
async def analyze(req:AnalyzeRequest):
    case_text=patient_to_text(req.patient)
    analysis=deterministic_analysis(case_text+"\nQuestion: "+req.question)
    emergency_flags=detect_emergency_flags(case_text)
    chunks=await retrieve(case_text+"\n"+req.question,analysis.get("module"),settings.rag_top_k)

    source_ids=list(analysis.get("reference_ids",[]))
    for chunk in chunks: source_ids.extend(chunk.get("source_ids",[]))
    source_ids=list(dict.fromkeys(source_ids))
    sources=sources_for_ids(source_ids)

    context="\n\n".join(f"CHUNK {c['id']}\n{c['content']}\nSOURCE IDS: {', '.join(c.get('source_ids',[]))}" for c in chunks)
    differential="\n".join(f"- {d['diagnosis']} | category={d['category']} | priority={d['priority']} | matching features={', '.join(d['supporting_matches']) or 'none explicitly matched'}" for d in analysis.get("differential",[])[:10])
    source_block="\n".join(f"[{s['id']}] {s['title']} — {s['organization']} — {s['url']}" for s in sources)

    prompt=f"""
PATIENT / CASE INFORMATION
{case_text}

USER QUESTION
{req.question}

DETERMINISTIC CLINICAL CLASSIFICATION
Syndrome: {analysis.get('syndrome')}
Specialty: {analysis.get('specialty','unclassified')}

PRIORITIZED DIFFERENTIAL CANDIDATES
{differential or '- No deterministic module matched; explicitly state the limitation.'}

MODULE RED FLAGS
{'; '.join(analysis.get('red_flags',[]))}

TARGETED HISTORY QUESTIONS
{'; '.join(analysis.get('history_questions',[]))}

FOCUSED EXAMINATION
{'; '.join(analysis.get('examination',[]))}

INITIAL EVALUATION FRAMEWORK
{'; '.join(analysis.get('initial_evaluation',[]))}

RAG CONTEXT
{context or 'No RAG context retrieved.'}

ALLOWED REFERENCES
{source_block}

OUTPUT FORMAT
1. Clinical problem representation
2. Immediate red flags / must-not-miss issues
3. Prioritized differential diagnosis, with supporting and opposing/missing features
4. Targeted history still needed
5. Focused examination
6. Investigations: immediate/bedside; blood/urine; microbiology/culture/PCR where indicated; pathology/biopsy/cytology only when indicated; imaging X-ray/USG/CT/MRI/MRA/MRV only if justified, with conditional contrast considerations
7. How new results would change the differential
8. High-level management/escalation considerations WITHOUT medication doses
9. Evidence/reference links using ONLY allowed [SOURCE-ID] citations
10. Uncertainty and limitations
"""
    try:
        answer=await chat(SYSTEM_PROMPT,prompt); llm_status="local-ollama"
    except Exception as exc:
        llm_status="unavailable"
        answer=("Local LLM is unavailable, so only deterministic clinical output is shown. Start Ollama and ensure the configured Qwen3 model is pulled.\n\n"
                f"Syndrome: {analysis.get('syndrome')}\n"
                f"Differential: {', '.join(d['diagnosis'] for d in analysis.get('differential',[])[:8])}\n"
                f"Suggested evaluation: {'; '.join(analysis.get('initial_evaluation',[]))}\nTechnical detail: {exc}")

    answer=emergency_preamble(emergency_flags)+answer
    answer,dose_removed=strip_unverified_doses(answer)
    answer,invalid_citations=validate_citations(answer,source_ids)
    imaging_note=imaging_safety_note(case_text+"\n"+req.question)

    return {"llm_status":llm_status,"syndrome":analysis.get("syndrome"),"specialty":analysis.get("specialty"),"module_id":analysis.get("module"),"module_confidence":analysis.get("module_confidence"),"emergency_flags":emergency_flags,"differential":analysis.get("differential",[])[:10],"history_questions":analysis.get("history_questions",[]),"focused_examination":analysis.get("examination",[]),"initial_evaluation":analysis.get("initial_evaluation",[]),"rag_chunks":[{"id":c["id"],"title":c["title"],"source_ids":c.get("source_ids",[])} for c in chunks],"answer":answer,"imaging_safety_note":imaging_note,"dose_content_removed":dose_removed,"invalid_citations_removed":invalid_citations,"references":sources,"disclaimer":"Prototype only. Not validated for autonomous diagnosis or treatment. Verify against current local/specialty guidance and clinician judgment."}
