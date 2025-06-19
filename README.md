# KiCad AI Circuit Generator

An AI-powered chat interface for generating KiCad circuit files through natural language descriptions.

## Features

- Natural language circuit description input
- Generates complete KiCad projects with:
  - Schematics (.kicad_sch)
  - Netlists (.net)
  - PCB files (.kicad_pcb)
  - Project files (.kicad_pro)
- Real-time chat interface
- Example circuit templates
- Automatic KiCad environment setup
- **RC Filter Circuit Generation** (NEW!)
  - Low-pass and high-pass filters
  - Configurable cutoff frequencies
  - Automatic component value calculation

## Prerequisites

- Python 3.8 or higher
- KiCad 6.0 or higher
- Git (for downloading symbol libraries)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kicad-ai-generator.git
cd kicad-ai-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

1. Start the chat interface:
```bash
streamlit run interface/chat_ui.py
```

2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Type your circuit description in natural language, for example:
   - "Create a voltage divider that converts 5V to 3.3V"
   - "Generate an RC low-pass filter with 1kHz cutoff frequency"
   - "Design a simple LED circuit with current limiting resistor"

4. The generated KiCad files will be saved in the `kicad_output` directory

### RC Filter Generation

The project now includes a dedicated RC filter generation function:

```python
from generate_circuit import create_rc_filter

# Create a low-pass filter with 1kHz cutoff
create_rc_filter(cutoff_freq=1000, filter_type='low_pass')

# Create a high-pass filter with 500Hz cutoff
create_rc_filter(cutoff_freq=500, filter_type='high_pass')

# Use custom component values
create_rc_filter(cutoff_freq=2000, filter_type='low_pass', r_value=4700, c_value=0.01e-6)
```

#### RC Filter Parameters:
- `cutoff_freq` (float): Cutoff frequency in Hz (default: 1000 Hz)
- `filter_type` (str): 'low_pass' or 'high_pass' (default: 'low_pass')
- `r_value` (float): Resistor value in ohms (default: 10k)
- `c_value` (float): Capacitor value in farads (if None, calculated from cutoff freq)

### Testing

Run the test script to generate multiple RC filter examples:

```bash
python test_rc_filter.py
```

This will create:
- RC low-pass filter (1kHz cutoff)
- RC high-pass filter (500Hz cutoff)
- Custom low-pass filter (2kHz, 4.7kΩ resistor)
- Custom high-pass filter (100Hz, 0.01μF capacitor)
- Audio low-pass filter (20kHz cutoff)

## Project Structure

```
kicad-ai-generator/
├── core/
│   ├── circuit_generator.py
│   └── llm_engine.py
├── interface/
│   └── chat_ui.py
├── utils/
│   └── kicad_setup.py
├── generate_circuit.py      # Main circuit generation functions
├── test_rc_filter.py       # RC filter test script
├── requirements.txt
└── README.md
```

## Circuit Types Supported

1. **Voltage Dividers**: Convert input voltage to desired output voltage
2. **RC Filters**: 
   - Low-pass filters (attenuate high frequencies)
   - High-pass filters (attenuate low frequencies)
   - Configurable cutoff frequencies
   - Automatic component value calculation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 