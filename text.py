import pygame

TYPING_PENDING = 0
TYPING_CORRECT = 1
TYPING_INCORRECT = 2

pygame.init()

class Line:
    def __init__(self, text:str):
        self.text = text
        self.status = [TYPING_PENDING for i in range(len(self.text))]
        self.pointer = 0

    def type_character(self, character):
        if(self.finish()):
            return
        if(self.text[self.pointer] == character):
            self.status[self.pointer] = TYPING_CORRECT
        else:
            self.status[self.pointer] = TYPING_INCORRECT
        self.pointer += 1
    
    def finish(self)->bool:
        return self.pointer == len(self.text)

    def restart(self):
        for i in range(len(self.text)):
            self.status[i] = TYPING_PENDING
        self.pointer = 0

class Text:
    def __init__(self, lines:list[str]):
        self.lines = [Line(l) for l in lines]
        self.pointer = 0

    def type_character(self, character):
        if(self.finish()):
            return 
        
        if(self.lines[self.pointer].finish()):
            self.pointer += 1
            self.type_character(character)
        else:
            self.lines[self.pointer].type_character(character)
        

    def finish(self)->bool:
        return (self.pointer == len(self.lines)-1 and self.lines[self.pointer].finish())
    
    def restart(self):
        for i in range(self.lines):
            self.lines[i].restart()
        self.pointer = 0


class TextRender:
    def __init__(self, font:str|None, size:int, width:int, height:int, \
                color_pending = (128, 128, 128), \
                color_correct = (0, 0, 255), \
                color_incorrect = (255, 0, 0)):
        self.font = pygame.font.Font(font, size)
        self.width = width
        self.height = height
        self.color_pending = color_pending
        self.color_correct = color_correct
        self.color_incorrect = color_incorrect

    def load_text_from_file(self, file_path)->Text:
        worlds = []
        with open(file_path, 'r') as file:
            all_line = file.readlines()
            for l in all_line:
                for w in l.split():
                    worlds.append(w)
        lines = []
        l = ""
        length = 0
        for w in worlds:
            w_length = self.font.render(w + " ", True, (0, 0, 0)).get_size()[0]
            if(length + w_length + 10  < self.width):
                l += w+" "
                length += w_length

            else:
                lines.append(l)
                l = w +' '
                length = w_length
        lines.append(l[0:-1:1])
        return Text(lines)

    
    def render_char(self, c:str, color:pygame.Color|tuple[int, int,int])->pygame.Surface:
        return self.font.render(c, True, color)
        
    
    def render_line(self, l:Line)->pygame.Surface:
        # return self.font.render(l.text, True, (255, 255, 255))
        h = self.font.render("|LJGH!^", True, (0, 0, 0)).get_size()[1]
        transparent_surface = pygame.Surface((self.width, h), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        color = None

        x = 0
        for i in range(len(l.text)):
            if l.status[i] == TYPING_PENDING:
                color = self.color_pending
            elif l.status[i] == TYPING_INCORRECT:
                color = self.color_incorrect
            else:
                color = self.color_correct
            rendered = self.font.render(l.text[i], True, color)
            transparent_surface.blit(rendered, (x, 0))
            x += rendered.get_size()[0]
        return transparent_surface

    def render_text(self, text:Text)->pygame.surface:
        # transparent Surface
        transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))

        y = 5
        for p in range(text.pointer, len(text.lines)):
            rendered = self.render_line(text.lines[p])
            if y + rendered.get_size()[1] + 5 > self.height:
                break
            transparent_surface.blit(rendered, (5, y))
            y += rendered.get_size()[1] + 5
            

        return transparent_surface
    
# trd = TextRender(None, 50, 900, 300)
# t = trd.load_text_from_file('TextSample/text1.txt')
# for l in t.lines:
#     print(l.text)

# screen = pygame.display.set_mode((1000, 500))

# running = True
# while running:
#     for event in pygame.event.get():
#         if(event.type == pygame.KEYDOWN):
#             if(event.unicode != ""):
#                 t.type_character(event.unicode)
#                 if(t.finish()):
#                     running = False
#     screen.fill((0, 0, 0))
#     pygame.draw.rect(screen, (255, 255, 255), (50, 50, 900, 300))
#     screen.blit(trd.render_text(t), (50, 50))
#     pygame.display.flip()

