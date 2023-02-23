import configparser
config = configparser.ConfigParser()
config.read("config.ini")
# window settings
WIDTH = int(config["WINDOW"]["width"])
HEIGHT = int(config["WINDOW"]["height"])
# game settings
GAME_FPS = int(config["GAME"]["fps"])
print(f"Width {WIDTH}, height {HEIGHT}")

ACC = float(config["PHYSICS"]["acceleration"])
FRICC = float(config["PHYSICS"]["friction"])