from simulation.simulation_consts import *
import pygame
from datetime import datetime
import numpy as np
from moviepy.editor import ImageSequenceClip
from random import randint
import log
import database.db_access as db
from simulation.bot import Bot
from simulation.bullet import Bullet
import json
from RestrictedPython import compile_restricted, safe_builtins

class Simulation:

    def __init__(self):
        log.d("Initializing pygame...")
        pygame.init()
        log.d("Pygame initialized")
        
        log.d("Creating the screen...")
        self.__screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        log.d("Screen created")

        log.d("Initializing simulation object variables...")
        self.__clock = pygame.time.Clock()
        self.__current_tick = 0
        self.__frames = []
        self.__id_counter = 0
        self.__entities = {
            "bots": {},
            "bullets": {}
        }
        log.d("Simulation object variables initialized")
    
    def get_id(self):
        self.__id_counter += 1
        return self.__id_counter
    
    def run(self):

        log.d("Preparing to run the simulation...")
        list_of_bots = db.get_bots_to_execute()
        for bot in list_of_bots:
            config = json.loads(bot["config"])
            sim_id = self.get_id()
            self.__entities["bots"][sim_id] = Bot(sim_id, 
                                                  bot["id"], 
                                                  bot["username"], 
                                                  randint(100, 900), 
                                                  randint(100, 900), 
                                                  bot["code"], 
                                                  config["health"], 
                                                  config["shield"], 
                                                  config["attack"])
        log.d("Simulation prepared")

        log.d("Running the simulation loop...")
        running = True
        while self.__current_tick < DURATION and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.__perform_actions()
            self.__update_frame()
            pygame.display.flip()

            self.__save_frame()

            self.__current_tick += 1
            self.__clock.tick(FPS)

        pygame.quit()
        log.d("Simulation loop finished")
    
    def __generate_actions(self, bot):
        def move(dx, dy):
            bot.move(dx, dy)
        
        def shot(dx, dy):
            sim_id = self.get_id()
            self.__entities["bullets"][sim_id] = Bullet(sim_id, 
                                                        bot.x(), 
                                                        bot.y(), 
                                                        dx, 
                                                        dy, 
                                                        BULLET_DAMAGE)

        return move, shot

    def __perform_actions(self):
        for bot in self.__entities["bots"].values():
            move, shot = self.__generate_actions(bot) #for the context enviroment
            context = {
                "__builtins__": safe_builtins,
                "move": move,
                "shot": shot
            }
            try:
                bot_code = compile_restricted(bot.code(), '<string>', 'exec')
                exec(bot_code, context, {}) #execute the bot code
            except Exception as e:
                log.e(f"Error while executing the bot code with db_id = {bot.get_db_id()} and name = {bot.get_name()}: {e}")
                self.__entities["bots"].pop(bot.get_sim_id())
                continue
        
        for bullet in self.__entities["bullets"].values():
            bullet.move()
    
    def __update_frame(self):
        self.__screen.fill(BACKGROUND_COLOR)
        for bot in self.__entities["bots"].values():
            pygame.draw.circle(self.__screen, BOT_COLOR, bot.pos(), BOT_RADIUS)
        for bullet in self.__entities["bullets"].values():
            pygame.draw.circle(self.__screen, BULLET_COLOR, bullet.pos(), BULLET_RADIUS)
    
    def __save_frame(self):
        frame = pygame.surfarray.array3d(self.__screen)
        
        frame = np.rot90(frame, k=-1)
        frame = np.fliplr(frame)

        self.__frames.append(frame)
    
    def save_replay(self):

        log.d("Saving the mp4 file...")
        video_clip = ImageSequenceClip(self.__frames, fps=FPS)
        video_clip.write_videofile(SIM_MP4_NAME, fps=FPS)
        log.d("Mp4 file saved")

        log.d("Saving the simulation info file...")
        with open(SIM_INFO_NAME, "w") as f:
            f.write(f"Last simulation: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        log.d("Simulation info file saved")