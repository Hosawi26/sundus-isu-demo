import random
import time
from .logic import AnomalyEvent

class AnomalyGenerator:
    def __init__(self):
        # Data from Anomaly Database.pdf
        self.scenarios = [
            {"id": "C-01", "type": "Unauthorized Access", "description": "Unauthorized person entering a lab in the Durham Center after hours.", "location": "Durham Center Lab", "base_severity": 0.3},
            {"id": "C-02", "type": "Unattended Object", "description": "Unattended backpack left near the Memorial Union entrance for >10 mins.", "location": "Memorial Union Entrance", "base_severity": 0.6},
            {"id": "C-05", "type": "Security Breach", "description": "Person observed propping open a fire door in a residence hall.", "location": "Residence Hall", "base_severity": 0.3},
            {"id": "C-06", "type": "Suspicious Activity", "description": "Person attempting to climb the facade of Beardshear Hall.", "location": "Beardshear Hall", "base_severity": 0.65},
            {"id": "C-09", "type": "Suspicious Activity", "description": "Individual ducking and hiding near a vehicle in a parking lot.", "location": "Parking Lot", "base_severity": 0.45},
            {"id": "H-01", "type": "Physical Altercation", "description": "Physical altercation breaking out at a Jack Trice Stadium tailgate.", "location": "Jack Trice Stadium", "base_severity": 0.8},
            {"id": "H-02", "type": "Medical Emergency", "description": "Individual collapsing suddenly in the Parks Library common area.", "location": "Parks Library", "base_severity": 0.85},
            {"id": "H-03", "type": "Weapon Detection", "description": "Person brandishing a firearm in a classroom setting.", "location": "Classroom", "base_severity": 1.0},
            {"id": "H-04", "type": "Environmental Hazard", "description": "Visual indicators of a flash flood (Squaw Creek area).", "location": "Squaw Creek", "base_severity": 0.9},
            {"id": "C-03", "type": "Vehicle Incident", "description": "Low-speed fender bender in the Lied Recreation Center lot.", "location": "Lied Rec Center", "base_severity": 0.25},
        ]
        
    def generate_event(self) -> AnomalyEvent:
        """
        Simulates an anomaly event from the database.
        """
        scenario = random.choice(self.scenarios)
        # Low fluctuation to keep it near the 'severity' defined in PDF
        fluctuation = random.uniform(-0.05, 0.05)
        severity = max(0.0, min(1.0, scenario["base_severity"] + fluctuation))
        
        event = AnomalyEvent(
            id=scenario["id"],
            timestamp=time.time(),
            description=scenario["description"],
            severity=severity,
            location=scenario["location"],
            type=scenario["type"]
        )
        return event

    def get_specific_scenario(self, scenario_id: str) -> Optional[AnomalyEvent]:
        """
        Retrieves a specific scenario by ID (e.g., 'H-03').
        """
        for sc in self.scenarios:
            if sc["id"] == scenario_id:
                return AnomalyEvent(
                    id=sc["id"],
                    timestamp=time.time(),
                    description=sc["description"],
                    severity=sc["base_severity"],
                    location=sc["location"],
                    type=sc["type"]
                )
        return None
        """
        Forces a scenario that matches a specific tier for testing.
        """
        if target_tier == 1:
            base = 0.2
        elif target_tier == 2:
            base = 0.55
        else:
            base = 0.9
            
        return AnomalyEvent(
            id=f"test_{target_tier}_{int(time.time())}",
            timestamp=time.time(),
            description="Forced Test Event",
            severity=base,
            location="Test Grid",
            type="Test Protocol"
        )
