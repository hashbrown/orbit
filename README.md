# Orbit Simulation

A Python application that simulates and visualizes objects orbiting Earth with realistic orbital mechanics.

## Setup Instructions

1. Install `uv` if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone this repository:
```bash
git clone <repository-url>
cd orbit
```

3. Create a virtual environment and install dependencies using `uv`:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
uv pip install -r requirements.txt
```

4. Run the application:
```bash
python src/main.py
```

## Features

- Real-time simulation of orbital mechanics
- Interactive control of orbital parameters
- Visualization of Earth and orbiting objects
- Support for various orbital scenarios

## Project Structure

The project follows a modular structure:
- `src/physics/`: Orbital mechanics calculations
- `src/visualization/`: Rendering and display
- `src/ui/`: User interface components

## Development

Please refer to `spec.md` for detailed technical specifications and development guidelines.

## License

MIT License 