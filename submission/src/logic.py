from dataclasses import dataclass
from typing import Dict, List, Optional
import time

@dataclass
class AnomalyEvent:
    id: str
    timestamp: float
    description: str
    severity: float  # 0.0 to 1.0
    location: str
    type: str  # e.g., "Overcrowding", "Suspicious Object"

@dataclass
class Alert:
    level: int  # 1, 2, 3
    color: str  # "green", "orange", "red"
    nle: str  # Natural Language Explanation
    audio_cue: bool
    strobe: bool

class TieredLogicEngine:
    def __init__(self):
        self.tiers = {
            1: {"threshold": 0.4, "color": "green", "label": "MONITORING"},
            2: {"threshold": 0.7, "color": "orange", "label": "CAUTION"},
            3: {"threshold": 1.0, "color": "red", "label": "CRITICAL"}
        }

    def process_anomaly(self, anomaly: AnomalyEvent) -> Alert:
        """
        Processes an anomaly event and returns the appropriate alert tier.
        Logic is based on severity thresholding.
        """
        severity = anomaly.severity
        tier = 1
        
        if severity > self.tiers[2]["threshold"]:
            tier = 3
        elif severity > self.tiers[1]["threshold"]:
            tier = 2
            
        return self._generate_alert(tier, anomaly)

    def _generate_alert(self, tier: int, anomaly: AnomalyEvent) -> Alert:
        if tier == 1:
            nle = f"System monitoring area '{anomaly.location}'. No significant anomalies detected. Current activity level is strictly routine."
            return Alert(level=1, color="green", nle=nle, audio_cue=False, strobe=False)
        
        elif tier == 2:
            nle = f"Attention: Unusual pattern detected at '{anomaly.location}'. Potential {anomaly.type.lower()} identified. Please verify camera feed."
            return Alert(level=2, color="orange", nle=nle, audio_cue=True, strobe=False)
            
        elif tier == 3:
            nle = f"CRITICAL ALERT: High-severity {anomaly.type.lower()} confirming at '{anomaly.location}'. Immediate human intervention required. Initiating containment protocols."
            return Alert(level=3, color="red", nle=nle, audio_cue=True, strobe=True)
            
        return Alert(level=0, color="grey", nle="System Error", audio_cue=False, strobe=False)
