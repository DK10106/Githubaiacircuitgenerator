from skidl import *
import os
import urllib.request
from datetime import datetime

def log(msg):
    """Log messages with timestamp"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def setup_kicad_env():
    """Setup KiCad environment and download required libraries"""
    log("Setting up KiCad environment...")
    
    # Create libraries directory
    libraries_dir = os.path.join(os.getcwd(), 'libraries')
    os.makedirs(libraries_dir, exist_ok=True)
    
    # Download required KiCad libraries
    required_libs = {
        'Device.kicad_sym': 'https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/Device.kicad_sym',
        'power.kicad_sym': 'https://gitlab.com/kicad/libraries/kicad-symbols/-/raw/master/power.kicad_sym'
    }
    
    for lib_name, lib_url in required_libs.items():
        lib_path = os.path.join(libraries_dir, lib_name)
        if not os.path.exists(lib_path):
            log(f"Downloading {lib_name}...")
            urllib.request.urlretrieve(lib_url, lib_path)
            log(f"✓ Downloaded {lib_name}")
    
    # Set up library search paths
    lib_search_paths_kicad = lib_search_paths_skidl = [os.path.abspath(libraries_dir)]
    
    # Set environment variables
    os.environ['KICAD_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
    os.environ['KICAD6_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
    os.environ['KICAD7_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
    os.environ['KICAD8_SYMBOL_DIR'] = os.path.abspath(libraries_dir)
    
    # Set default tool
    set_default_tool(KICAD)
    log("✓ KiCad environment setup complete")

def create_voltage_divider(vin=5.0, vout=3.3):
    """Create a voltage divider circuit"""
    # Reset the circuit to ensure clean generation
    default_circuit.reset()
    
    # Calculate resistor values (using 10k for R1)
    r1_value = 10000  # 10k
    r2_value = int(r1_value * (vout / (vin - vout)))
    
    # Create output directory
    output_dir = os.path.join(os.getcwd(), 'kicad_output', 'voltage_divider')
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up circuit
    circuit_name = f'voltage_divider_{int(vin)}v_{int(vout*10)}v'
    default_circuit.name = circuit_name
    default_circuit.description = f"Voltage divider {vin}V to {vout}V"
    
    # Create nets
    vcc = Net('VCC')
    gnd = Net('GND')
    out = Net('OUT')
    
    # Create components with footprints
    r1 = Part("Device", "R", value=f"{r1_value}", footprint="Resistor_SMD:R_0805_2012Metric")
    r2 = Part("Device", "R", value=f"{r2_value}", footprint="Resistor_SMD:R_0805_2012Metric")
    
    # Make connections
    vcc += r1[1]
    r1[2] += out
    out += r2[1]
    r2[2] += gnd
    
    # Generate KiCad files
    netlist_file = os.path.join(output_dir, f"{circuit_name}.net")
    log(f"Generating netlist: {netlist_file}")
    generate_netlist(file_=netlist_file)
    
    # Create KiCad project file
    project_file = os.path.join(output_dir, f"{circuit_name}.kicad_pro")
    with open(project_file, 'w') as f:
        f.write('''{
  "board": {
    "design_settings": {
      "defaults": {
        "board_outline_line_width": 0.1,
        "copper_line_width": 0.2,
        "copper_text_size_h": 1.5,
        "copper_text_size_v": 1.5,
        "copper_text_thickness": 0.3,
        "copper_text_upright": false,
        "courtyard_line_width": 0.05,
        "dimension_precision": 4,
        "dimension_units": 3,
        "dimensions": {
          "arrow_length": 1270000,
          "extension_offset": 500000,
          "keep_text_aligned": true,
          "suppress_zeroes": false,
          "text_position": 0,
          "units_format": 1
        }
      }
    }
  },
  "meta": {
    "filename": "circuit.kicad_pro",
    "version": 1
  },
  "net_settings": {
    "classes": [
      {
        "bus_width": 12.0,
        "clearance": 0.2,
        "diff_pair_gap": 0.25,
        "diff_pair_via_gap": 0.25,
        "diff_pair_width": 0.2,
        "line_style": 0,
        "microvia_diameter": 0.3,
        "microvia_drill": 0.1,
        "name": "Default",
        "pcb_color": "rgba(0, 0, 0, 0.000)",
        "schematic_color": "rgba(0, 0, 0, 0.000)",
        "track_width": 0.25,
        "via_diameter": 0.8,
        "via_drill": 0.4,
        "wire_width": 6.0
      }
    ],
    "meta": {
      "version": 2
    }
  },
  "schematic": {
    "drawing": {
      "default_line_thickness": 6.0,
      "default_text_size": 50.0,
      "field_names": [],
      "intersheets_ref_own_page": false,
      "intersheets_ref_prefix": "",
      "intersheets_ref_short": false,
      "intersheets_ref_show": false,
      "intersheets_ref_suffix": "",
      "junction_size_choice": 3,
      "label_size_ratio": 0.25,
      "pin_symbol_size": 0.0,
      "text_offset_ratio": 0.08
    }
  }
}''')
    
    # Create schematic file with component placement
    schematic_file = os.path.join(output_dir, f"{circuit_name}.kicad_sch")
    with open(schematic_file, 'w') as f:
        f.write(f'''(kicad_sch (version 20211123) (generator skidl)
  (paper "A4")
  (title_block
    (title "{circuit_name}")
    (date "{datetime.now().strftime('%Y-%m-%d')}")
    (rev "v1.0")
    (company "Generated by KiCad AI Assistant")
  )
  (lib_symbols
    (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "R" (id 0) (at 2.032 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "R" (id 1) (at 0 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "" (id 2) (at -1.778 0 90)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "~" (id 3) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_keywords" "R res resistor" (id 4) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_description" "Resistor" (id 5) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_fp_filters" "R_*" (id 6) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "R_0_1"
        (rectangle (start -1.016 -2.54) (end 1.016 2.54)
          (stroke (width 0.254) (type default) (color 0 0 0 0))
          (fill (type none))
        )
      )
      (symbol "R_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 0 -3.81 90) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
      )
    )
  )
  (wire (pts (xy 127 88.9) (xy 127 96.52)) (stroke (width 0) (type default) (color 0 0 0 0)))
  (wire (pts (xy 127 109.22) (xy 127 116.84)) (stroke (width 0) (type default) (color 0 0 0 0)))
  (wire (pts (xy 127 129.54) (xy 127 137.16)) (stroke (width 0) (type default) (color 0 0 0 0)))
  (symbol (lib_id "Device:R") (at 127 100.33 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid "1234a")
    (property "Reference" "R1" (id 0) (at 129.54 99.06 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{r1_value}" (id 1) (at 129.54 101.6 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "Resistor_SMD:R_0805_2012Metric" (id 2) (at 125.222 100.33 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid "1234b"))
    (pin "2" (uuid "1234c"))
  )
  (symbol (lib_id "Device:R") (at 127 125.73 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid "5678a")
    (property "Reference" "R2" (id 0) (at 129.54 124.46 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{r2_value}" (id 1) (at 129.54 127 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "Resistor_SMD:R_0805_2012Metric" (id 2) (at 125.222 125.73 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid "5678b"))
    (pin "2" (uuid "5678c"))
  )
  (label "VCC" (at 127 88.9 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
  )
  (label "OUT" (at 127 109.22 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
  )
  (label "GND" (at 127 137.16 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
  )
)''')
    
    # Create PCB file
    pcb_file = os.path.join(output_dir, f"{circuit_name}.kicad_pcb")
    with open(pcb_file, 'w') as f:
        f.write(f'''(kicad_pcb (version 20211014) (generator pcbnew)
  (general
    (thickness 1.6)
  )
  (paper "A4")
  (title_block
    (title "{circuit_name}")
    (date "{datetime.now().strftime('%Y-%m-%d')}")
    (rev "v1.0")
    (company "Generated by KiCad AI Assistant")
  )
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    (33 "F.Adhes" user "F.Adhesive")
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (42 "Eco1.User" user "User.Eco1")
    (43 "Eco2.User" user "User.Eco2")
    (44 "Edge.Cuts" user)
    (45 "Margin" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user)
    (49 "F.Fab" user)
  )
)''')
    
    log(f"✓ Generated KiCad files in: {output_dir}")
    log(f"✓ Files created:")
    log(f"  - {os.path.basename(netlist_file)}")
    log(f"  - {os.path.basename(project_file)}")
    log(f"  - {os.path.basename(schematic_file)}")
    log(f"  - {os.path.basename(pcb_file)}")
    
    return netlist_file, project_file, schematic_file

def create_rc_filter(cutoff_freq=1000, filter_type='low_pass', r_value=10000, c_value=None):
    """Create an RC filter circuit
    
    Args:
        cutoff_freq (float): Cutoff frequency in Hz (default: 1000 Hz)
        filter_type (str): 'low_pass' or 'high_pass' (default: 'low_pass')
        r_value (float): Resistor value in ohms (default: 10k)
        c_value (float): Capacitor value in farads (if None, calculated from cutoff freq)
    """
    # Reset the circuit to ensure clean generation
    default_circuit.reset()
    
    # Calculate capacitor value if not provided
    if c_value is None:
        # f = 1/(2*pi*R*C) -> C = 1/(2*pi*R*f)
        c_value = 1 / (2 * 3.14159 * r_value * cutoff_freq)
        # Convert to microfarads for display
        c_value_uf = c_value * 1e6
    else:
        c_value_uf = c_value * 1e6
    
    # Create output directory
    output_dir = os.path.join(os.getcwd(), 'kicad_output', 'rc_filter')
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up circuit
    circuit_name = f'rc_{filter_type}_{int(cutoff_freq)}hz'
    default_circuit.name = circuit_name
    default_circuit.description = f"RC {filter_type.replace('_', ' ')} filter, {cutoff_freq} Hz cutoff"
    
    # Create nets
    vcc = Net('VCC')
    gnd = Net('GND')
    in_signal = Net('IN')
    out_signal = Net('OUT')
    
    # Create components with footprints
    r1 = Part("Device", "R", value=f"{r_value}", footprint="Resistor_SMD:R_0805_2012Metric")
    c1 = Part("Device", "C", value=f"{c_value_uf:.2f}uF", footprint="Capacitor_SMD:C_0805_2012Metric")
    
    # Make connections based on filter type
    if filter_type == 'low_pass':
        # Low-pass: IN -> R -> OUT, OUT -> C -> GND
        in_signal += r1[1]
        r1[2] += out_signal
        out_signal += c1[1]
        c1[2] += gnd
    elif filter_type == 'high_pass':
        # High-pass: IN -> C -> OUT, OUT -> R -> GND
        in_signal += c1[1]
        c1[2] += out_signal
        out_signal += r1[1]
        r1[2] += gnd
    else:
        raise ValueError("filter_type must be 'low_pass' or 'high_pass'")
    
    # Generate KiCad files
    netlist_file = os.path.join(output_dir, f"{circuit_name}.net")
    log(f"Generating netlist: {netlist_file}")
    generate_netlist(file_=netlist_file)
    
    # Create KiCad project file
    project_file = os.path.join(output_dir, f"{circuit_name}.kicad_pro")
    with open(project_file, 'w') as f:
        f.write('''{
  "board": {
    "design_settings": {
      "defaults": {
        "board_outline_line_width": 0.1,
        "copper_line_width": 0.2,
        "copper_text_size_h": 1.5,
        "copper_text_size_v": 1.5,
        "copper_text_thickness": 0.3,
        "copper_text_upright": false,
        "courtyard_line_width": 0.05,
        "dimension_precision": 4,
        "dimension_units": 3,
        "dimensions": {
          "arrow_length": 1270000,
          "extension_offset": 500000,
          "keep_text_aligned": true,
          "suppress_zeroes": false,
          "text_position": 0,
          "units_format": 1
        }
      }
    }
  },
  "meta": {
    "filename": "circuit.kicad_pro",
    "version": 1
  },
  "net_settings": {
    "classes": [
      {
        "bus_width": 12.0,
        "clearance": 0.2,
        "diff_pair_gap": 0.25,
        "diff_pair_via_gap": 0.25,
        "diff_pair_width": 0.2,
        "line_style": 0,
        "microvia_diameter": 0.3,
        "microvia_drill": 0.1,
        "name": "Default",
        "pcb_color": "rgba(0, 0, 0, 0.000)",
        "schematic_color": "rgba(0, 0, 0, 0.000)",
        "track_width": 0.25,
        "via_diameter": 0.8,
        "via_drill": 0.4,
        "wire_width": 6.0
      }
    ],
    "meta": {
      "version": 2
    }
  },
  "schematic": {
    "drawing": {
      "default_line_thickness": 6.0,
      "default_text_size": 50.0,
      "field_names": [],
      "intersheets_ref_own_page": false,
      "intersheets_ref_prefix": "",
      "intersheets_ref_short": false,
      "intersheets_ref_show": false,
      "intersheets_ref_suffix": "",
      "junction_size_choice": 3,
      "label_size_ratio": 0.25,
      "pin_symbol_size": 0.0,
      "text_offset_ratio": 0.08
    }
  }
}''')
    
    # Create schematic file with component placement
    schematic_file = os.path.join(output_dir, f"{circuit_name}.kicad_sch")
    with open(schematic_file, 'w') as f:
        f.write(f'''(kicad_sch (version 20211123) (generator skidl)
  (paper "A4")
  (title_block
    (title "{circuit_name}")
    (date "{datetime.now().strftime('%Y-%m-%d')}")
    (rev "v1.0")
    (company "Generated by KiCad AI Assistant")
  )
  (lib_symbols
    (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "R" (id 0) (at 2.032 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "R" (id 1) (at 0 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "" (id 2) (at -1.778 0 90)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "~" (id 3) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_keywords" "R res resistor" (id 4) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_description" "Resistor" (id 5) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_fp_filters" "R_*" (id 6) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "R_0_1"
        (rectangle (start -1.016 -2.54) (end 1.016 2.54)
          (stroke (width 0.254) (type default) (color 0 0 0 0))
          (fill (type none))
        )
      )
      (symbol "R_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 0 -3.81 90) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
      )
    )
    (symbol "Device:C" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "C" (id 0) (at 2.032 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "C" (id 1) (at 0 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "" (id 2) (at -1.778 0 90)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "~" (id 3) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_keywords" "C cap capacitor" (id 4) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_description" "Capacitor" (id 5) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_fp_filters" "C_*" (id 6) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "C_0_1"
        (rectangle (start -1.016 -2.54) (end 1.016 2.54)
          (stroke (width 0.254) (type default) (color 0 0 0 0))
          (fill (type none))
        )
      )
      (symbol "C_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 0 -3.81 90) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
      )
    )
  )
  (wire (pts (xy 127 88.9) (xy 127 96.52)) (stroke (width 0) (type default) (color 0 0 0 0)))
  (wire (pts (xy 127 109.22) (xy 127 116.84)) (stroke (width 0) (type default) (color 0 0 0 0)))
  (wire (pts (xy 127 129.54) (xy 127 137.16)) (stroke (width 0) (type default) (color 0 0 0 0)))
  (symbol (lib_id "Device:R") (at 127 100.33 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid "1234a")
    (property "Reference" "R1" (id 0) (at 129.54 99.06 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{r_value}" (id 1) (at 129.54 101.6 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "Resistor_SMD:R_0805_2012Metric" (id 2) (at 125.222 100.33 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid "1234b"))
    (pin "2" (uuid "1234c"))
  )
  (symbol (lib_id "Device:C") (at 127 125.73 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid "5678a")
    (property "Reference" "C1" (id 0) (at 129.54 124.46 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{c_value_uf:.2f}uF" (id 1) (at 129.54 127 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "Capacitor_SMD:C_0805_2012Metric" (id 2) (at 125.222 125.73 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid "5678b"))
    (pin "2" (uuid "5678c"))
  )
  (label "IN" (at 127 88.9 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
  )
  (label "OUT" (at 127 109.22 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
  )
  (label "GND" (at 127 137.16 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
  )
)''')
    
    # Create PCB file
    pcb_file = os.path.join(output_dir, f"{circuit_name}.kicad_pcb")
    with open(pcb_file, 'w') as f:
        f.write(f'''(kicad_pcb (version 20211014) (generator pcbnew)
  (general
    (thickness 1.6)
  )
  (paper "A4")
  (title_block
    (title "{circuit_name}")
    (date "{datetime.now().strftime('%Y-%m-%d')}")
    (rev "v1.0")
    (company "Generated by KiCad AI Assistant")
  )
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    (33 "F.Adhes" user "F.Adhesive")
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (42 "Eco1.User" user "User.Eco1")
    (43 "Eco2.User" user "User.Eco2")
    (44 "Edge.Cuts" user)
    (45 "Margin" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user)
    (49 "F.Fab" user)
  )
)''')
    
    log(f"✓ Generated RC {filter_type} filter circuit")
    log(f"✓ Cutoff frequency: {cutoff_freq} Hz")
    log(f"✓ Resistor: {r_value} Ω")
    log(f"✓ Capacitor: {c_value_uf:.2f} μF")
    log(f"✓ Generated KiCad files in: {output_dir}")
    log(f"✓ Files created:")
    log(f"  - {os.path.basename(netlist_file)}")
    log(f"  - {os.path.basename(project_file)}")
    log(f"  - {os.path.basename(schematic_file)}")
    log(f"  - {os.path.basename(pcb_file)}")
    
    return netlist_file, project_file, schematic_file

if __name__ == "__main__":
    # Set up KiCad environment
    setup_kicad_env()
    
    # Create a voltage divider (5V to 3.3V)
    log("\n=== Creating Voltage Divider Circuit ===")
    netlist, project, schematic = create_voltage_divider(5.0, 3.3)
    
    # Create an RC low-pass filter (1kHz cutoff)
    log("\n=== Creating RC Low-Pass Filter Circuit ===")
    rc_netlist, rc_project, rc_schematic = create_rc_filter(cutoff_freq=1000, filter_type='low_pass')
    
    # Create an RC high-pass filter (500Hz cutoff)
    log("\n=== Creating RC High-Pass Filter Circuit ===")
    rc_hp_netlist, rc_hp_project, rc_hp_schematic = create_rc_filter(cutoff_freq=500, filter_type='high_pass')
    
    log("\nTo use these files in KiCad:")
    log("1. Open KiCad")
    log("2. Click 'File' -> 'Open Project'")
    log("3. Navigate to the respective output directories:")
    log(f"   - Voltage divider: {os.path.dirname(project)}")
    log(f"   - RC low-pass filter: {os.path.dirname(rc_project)}")
    log(f"   - RC high-pass filter: {os.path.dirname(rc_hp_project)}")
    log("4. Open the .kicad_pro files")
    log("5. The schematic and netlist will be loaded automatically") 