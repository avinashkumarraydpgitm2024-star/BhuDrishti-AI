def explain_risk(data):
    reasons = []

    if data.rainfall >= 100:
        reasons.append({
            "factor": "rainfall",
            "severity": "critical",
            "message": "Extremely high rainfall detected."
        })
    elif data.rainfall >= 70:
        reasons.append({
            "factor": "rainfall",
            "severity": "high",
            "message": "Heavy rainfall may increase land instability."
        })

    if data.slope >= 50:
        reasons.append({
            "factor": "slope",
            "severity": "high",
            "message": "Steep terrain increases slope failure risk."
        })
    elif data.slope >= 35:
        reasons.append({
            "factor": "slope",
            "severity": "moderate",
            "message": "Moderately steep terrain may increase instability."
        })

    if data.soil_moisture >= 80:
        reasons.append({
            "factor": "soil_moisture",
            "severity": "critical",
            "message": "Very high soil moisture indicates possible soil saturation."
        })
    elif data.soil_moisture >= 60:
        reasons.append({
            "factor": "soil_moisture",
            "severity": "high",
            "message": "High soil moisture may reduce soil stability."
        })

    if data.vegetation <= 30:
        reasons.append({
            "factor": "vegetation",
            "severity": "high",
            "message": "Low vegetation cover reduces natural soil protection."
        })
    elif data.vegetation <= 50:
        reasons.append({
            "factor": "vegetation",
            "severity": "moderate",
            "message": "Reduced vegetation cover may increase erosion risk."
        })

    if data.previous_incidents >= 3:
        reasons.append({
            "factor": "previous_incidents",
            "severity": "high",
            "message": "Multiple previous incidents have been recorded."
        })

    if data.humidity >= 85:
        reasons.append({
            "factor": "humidity",
            "severity": "moderate",
            "message": "High humidity indicates elevated atmospheric moisture."
        })

    if not reasons:
        reasons.append({
            "factor": "general",
            "severity": "low",
            "message": "No major risk indicators detected."
        })

    return reasons
