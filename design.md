# Earth-Moon-ISS Orbital Simulation

## 1. Project Overview
The project successfully implements a real-time simulation of the Earth-Moon-ISS system using actual orbital parameters and Newtonian physics. The simulation visualizes the orbits with proper scaling and provides interactive controls.

### Key Features
- Accurate orbital mechanics using Velocity Verlet integration
- Real-time visualization with Pygame
- Interactive controls for simulation speed and visibility
- Proper scaling to show both Moon and ISS orbits
- Distance indicators and trajectory paths
- Real-time information display (altitude, velocity)

## 2. Project Structure
```
orbit/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main simulation loop and initialization
│   ├── physics/
│   │   ├── __init__.py
│   │   ├── constants.py     # Physical and display constants
│   │   └── orbital_mechanics.py  # Orbital body class and physics
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── renderer.py      # Pygame-based visualization
│   └── ui/
│       ├── __init__.py
│       └── control_panel.py # UI controls and buttons
├── tests/                   # Test directory
├── run.py                   # Entry point script
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## 3. Implementation Details

### 3.1 Physics Engine (`orbital_mechanics.py`)
- **OrbitalBody Class**: Represents objects in orbit around Earth
  - Uses Velocity Verlet integration for stable orbits
  - Calculates gravitational forces using Newton's law
  - Maintains trajectory history for visualization
  - Supports activation/deactivation for visibility control

### 3.2 Constants (`constants.py`)
```python
# Physical Constants
EARTH_RADIUS = 6_371_000  # meters
EARTH_MASS = 5.972e24     # kg
MOON_MASS = 7.34767309e22 # kg
MOON_ORBITAL_RADIUS = 384_400_000  # meters
MOON_RADIUS = 1_737_100   # meters
ISS_MASS = 419_725        # kg
ISS_ALTITUDE = 408_000    # meters
G = 6.67430e-11          # m³/kg⋅s²

# Display Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
MOON_SCALE_FACTOR = DESIRED_MOON_PIXELS / MOON_ORBITAL_RADIUS
SCALE_FACTOR = MOON_SCALE_FACTOR * 2  # ISS scale

# Time Constants
SIMULATION_DURATION = 86400  # 24 hours
REAL_TIME_DURATION = 60     # 1 minute
TIME_SCALE = SIMULATION_DURATION / REAL_TIME_DURATION
```

### 3.3 Visualization (`renderer.py`)
- **Scaling Solution**: 
  - Moon orbit uses 95% of screen radius
  - ISS uses 2x Moon's scale for better visibility
  - Earth sized appropriately for both scales
- **Features**:
  - Body labels and connecting lines
  - Distance indicators
  - Trajectory paths
  - Real-time information display
  - Orbital path indicators

### 3.4 UI Controls (`control_panel.py`)
- **Button Class**: Handles button creation and events
- **Control Panel Features**:
  - Play/Pause toggle
  - Speed control (24h in 4min, 2min, 1min, or 30sec)
  - Reset simulation
  - Toggle Moon visibility
  - Toggle ISS visibility
  - Real-time information display

### 3.5 Main Simulation (`main.py`)
- **Initialization**:
  - Creates Moon and ISS with correct orbital parameters
  - Sets up visualization and UI components
- **Main Loop**:
  - Handles events and UI updates
  - Updates physics with proper time scaling
  - Manages visibility states
  - Coordinates rendering

## 4. Technical Specifications

### 4.1 Performance Optimizations
- Time step of 0.1 seconds for stability
- Trajectory history limited to 1000 points
- Frame rate capped at 60 FPS
- Efficient event handling

### 4.2 Scaling Details
- Moon orbit: 95% of screen radius
- ISS orbit: 2x Moon's scale
- Earth: Sized proportionally
- Distance indicators: Shown in kilometers

### 4.3 Time Scaling
- Default: 24 hours in 1 minute (1440x)
- Options: 
  - 24h in 4min (360x)
  - 24h in 2min (720x)
  - 24h in 1min (1440x)
  - 24h in 30sec (2880x)

## 5. Dependencies
```
pygame==2.5.2
numpy==1.24.3
scipy==1.12.0
```

## 6. Running the Simulation
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python run.py`

## 7. Future Improvements
- Add more celestial bodies (planets, satellites)
- Implement elliptical orbits
- Add orbital plane visualization
- Support for multiple central bodies
- Add more interactive controls
- Implement zoom functionality
- Add time reversal capability
- Support for saving/loading simulation states 