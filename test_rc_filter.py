#!/usr/bin/env python3
"""
Test script for RC filter circuit generation
"""

from generate_circuit import setup_kicad_env, create_rc_filter, log

def test_rc_filters():
    """Test various RC filter configurations"""
    
    # Set up KiCad environment
    setup_kicad_env()
    
    # Test 1: Basic low-pass filter (1kHz cutoff)
    log("\n=== Test 1: RC Low-Pass Filter (1kHz cutoff) ===")
    create_rc_filter(cutoff_freq=1000, filter_type='low_pass')
    
    # Test 2: High-pass filter (500Hz cutoff)
    log("\n=== Test 2: RC High-Pass Filter (500Hz cutoff) ===")
    create_rc_filter(cutoff_freq=500, filter_type='high_pass')
    
    # Test 3: Low-pass filter with custom resistor value
    log("\n=== Test 3: RC Low-Pass Filter (custom 4.7kΩ resistor) ===")
    create_rc_filter(cutoff_freq=2000, filter_type='low_pass', r_value=4700)
    
    # Test 4: High-pass filter with custom capacitor value
    log("\n=== Test 4: RC High-Pass Filter (custom 0.01μF capacitor) ===")
    create_rc_filter(cutoff_freq=100, filter_type='high_pass', r_value=10000, c_value=0.01e-6)
    
    # Test 5: Audio frequency low-pass filter (20kHz cutoff)
    log("\n=== Test 5: Audio Low-Pass Filter (20kHz cutoff) ===")
    create_rc_filter(cutoff_freq=20000, filter_type='low_pass')
    
    log("\n=== All RC filter tests completed! ===")
    log("Check the 'kicad_output/rc_filter' directory for generated files.")

if __name__ == "__main__":
    test_rc_filters() 