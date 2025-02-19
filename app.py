import text
import pygame
import tkinter as tk
from tkinter import filedialog
import time


class App:
    def __init__(self):
        self.text_render = text.TextRender(None, 30, 600, 300)
        self.screen = pygame.display.set_mode((700, 500))
        self.running = False
        self.clock = pygame.time.Clock()
        self.text = text.Text(["Sample Text"])

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif(event.type == pygame.KEYDOWN and event.unicode != ""):
                self.text.type_character(event.unicode)
                if(self.text.finish()):
                    self.running = False

    def wait_press_key(self):
        r = True
        while r:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif(event.type == pygame.KEYDOWN):
                    r = False
        



    def render(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (50, 10, 600, 300), 2)
        self.screen.blit(self.text_render.render_text(self.text), (50, 10))
        
        pygame.display.flip()

    def run(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(title="Choose a text((.txt) file")
        self.text = self.text_render.load_text_from_file(file_path)

        self.running = True
        self.wait_press_key()
        start = time.time()
        while(self.running):
            self.process_input()
            self.render()
            self.clock.tick(60)

        end  = time.time()
        t = end - start

        totalLetters = 0#sum([len(l.text) for l in self.text.lines])
        totalTyped = 0
        totalCorrect = 0
        totalIncorrect = 0
        
        for l in self.text.lines:
            totalLetters += len(l.text)
            for i in range(len(l.text)):
                if(l.status[i] == text.TYPING_INCORRECT):
                    totalTyped += 1
                    totalIncorrect += 1
                elif (l.status[i] == text.TYPING_CORRECT):
                    totalTyped += 1
                    totalCorrect += 1
        
        print("time = {}, typed = {}, correct = {}, incorrect = {}".format(t, totalTyped, totalCorrect, totalIncorrect))
        accuracy = (totalCorrect / totalTyped)*100
        wpm = ((totalTyped/5)/t)*60
        print("accuracy = {}, WPM = {}".format(accuracy, wpm))

        s = "Time: %.02f, WPM: %.02f x ACCURARY:%.02f = %.02f"%(t, wpm, accuracy, wpm*accuracy/100)
        result = self.text_render.font.render(s, True, (0, 0, 255))
        self.screen.blit(result, (50, 450))
        pygame.display.flip()


