"""Physical constants for orbital mechanics calculations."""

# Earth constants
EARTH_RADIUS = 6_371_000  # meters
EARTH_MASS = 5.972e24     # kg

# Moon constants
MOON_MASS = 7.34767309e22  # kg
MOON_ORBITAL_RADIUS = 384_400_000  # meters (average distance from Earth's center)
MOON_RADIUS = 1_737_100  # meters

# ISS constants
ISS_MASS = 419_725  # kg
ISS_ALTITUDE = 408_000  # meters (average altitude above Earth's surface)
ISS_ORBITAL_RADIUS = EARTH_RADIUS + ISS_ALTITUDE  # meters

# Universal constants
G = 6.67430e-11          # gravitational constant (m³/kg⋅s²)

# Display constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Calculate required scale to fit Moon on screen
# We want the Moon's orbit to take up 95% of the smaller screen dimension
SCREEN_RADIUS = min(SCREEN_WIDTH, SCREEN_HEIGHT) / 2  # Radius in pixels
DESIRED_MOON_PIXELS = SCREEN_RADIUS * 0.95  # Moon should reach 95% of the way to screen edge
MOON_SCALE_FACTOR = DESIRED_MOON_PIXELS / MOON_ORBITAL_RADIUS  # This gives us the scale needed

# Now set ISS scale to be similar but slightly larger for better visibility
SCALE_FACTOR = MOON_SCALE_FACTOR * 2  # ISS scale twice as large as Moon scale for better visibility

# Simulation constants
TIME_STEP = 0.1  # reduced for stability with high time_scale

# Time constants
SIMULATION_DURATION = 86400  # 24 hours in seconds
REAL_TIME_DURATION = 60     # 1 minute in seconds
TIME_SCALE = SIMULATION_DURATION / REAL_TIME_DURATION  # 1440x speed

# Debug print to verify calculations
print(f"Screen dimensions: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
print(f"Moon orbit radius: {MOON_ORBITAL_RADIUS:,} meters")
print(f"Moon pixels from center: {MOON_ORBITAL_RADIUS * MOON_SCALE_FACTOR:.1f}")
print(f"Screen radius available: {SCREEN_RADIUS:.1f}")
print(f"Moon scale factor: {MOON_SCALE_FACTOR:.2e}")
print(f"ISS scale factor: {SCALE_FACTOR:.2e}") 