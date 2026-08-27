from app.services.safety import detect_emergency_flags,strip_unverified_doses

def test_emergency_detection():
    assert detect_emergency_flags("patient in shock with respiratory distress")

def test_dose_guard():
    answer,removed=strip_unverified_doses("Give medicine 500 mg twice daily")
    assert removed is True and "500 mg" not in answer
