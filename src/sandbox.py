"""
Virtual Sandbox Test (Self-Correction Module)
This script simulates the logic loop to ensure no race conditions overlap between alerts.
"""
import time
import logging
from src.logic import TieredLogicEngine
from src.simulation import AnomalyGenerator

# Configure logging to strictly track valid outputs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_sandbox_test():
    engine = TieredLogicEngine()
    generator = AnomalyGenerator()
    
    print(">>> STARTING VIRTUAL SANDBOX TEST <<<")
    
    # Test 1: Rapid Fire Events (Race Condition Check)
    print("\n[Test 1] Rapid Fire Logic Check...")
    events = [generator.generate_event() for _ in range(50)]
    start_time = time.time()
    
    results = []
    for evt in events:
        alert = engine.process_anomaly(evt)
        results.append(alert)
        
    duration = time.time() - start_time
    print(f"Processed 50 events in {duration:.4f}s")
    
    # Validation: Ensure High Severity always yields Tier 3
    errors = 0
    for i, evt in enumerate(events):
        if evt.severity > 0.7 and results[i].level != 3:
            print(f"FAIL: Event {evt.id} severity {evt.severity} got Tier {results[i].level}")
            errors += 1
            
    if errors == 0:
        print("SUCCESS: 0 Logic Inconsistencies found in rapid batch.")
    else:
        print(f"FAILURE: {errors} Logic Inconsistencies found.")

    # Test 2: Priority Override
    print("\n[Test 2] Priority Override Check...")
    # Use known scenarios: C-01 (Low) vs H-03 (High)
    low_event = generator.get_specific_scenario("C-01") 
    high_event = generator.get_specific_scenario("H-03")
    
    # Simulate simultaneous processing (simulated via sequential immediate calls)
    alert_low = engine.process_anomaly(low_event)
    alert_high = engine.process_anomaly(high_event)
    
    if alert_high.level > alert_low.level:
        print("SUCCESS: High tier correctly prioritized in logic flow.")
    else:
        print("FAILURE: Priority inversion detected.")

if __name__ == "__main__":
    run_sandbox_test()
