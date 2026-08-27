from app.services.clinical_engine import deterministic_analysis

def test_ams_module():
    x=deterministic_analysis("65-year-old with altered sensorium, fever and diabetes")
    assert x["module"]=="AMS"
    names=[d["diagnosis"] for d in x["differential"]]
    assert "Metabolic encephalopathy" in names
    assert "CNS infection / meningoencephalitis" in names

def test_chest_pain_module():
    assert deterministic_analysis("sudden chest pain with sweating in a diabetic")["module"]=="CHEST_PAIN"
