MAP_WIDTH, MAP_HEIGHT = 500, 500 # pixels, actual playing zone
MAP_PADDING = 50 # padding at each side of the map
BULLET_RADIUS = 4 # pixels
BOT_RADIUS = 4 * BULLET_RADIUS # pixels
BOT_SPEED = 3 # pixels per frame
BULLET_SPEED = BOT_SPEED * 4 # pixels per frame
FPS = 20 # frames per second
DURATION = 10 * FPS # ticks (converts 60 seconds to ticks)
INTER_SIMULATION_TIME = 300 # seconds (5 minutes)
SIM_MP4_NAME = "replays/simulation.mp4"
SIM_INFO_NAME = "replays/simulation_info.txt"

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40) 
BOT_COLOR = BLUE
BACKGROUND_COLOR = BLACK
BULLET_COLOR = RED

BULLET_DAMAGE = 10 # change this in the future
BOT_SHOOT_COOLDOWN = 10 # ticks
BOT_MOVE_COOLDOWN = 1 
BOT_MELEE_COOLDOWN = 20 
BOT_DASH_COOLDOWN = 100
BOT_SUPER_SHOT_COOLDOWN = 100
BOT_SUPER_MELEE_COOLDOWN = 100
