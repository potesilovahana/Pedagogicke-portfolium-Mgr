"""Kreslení obrazovek aplikace."""
from __future__ import annotations
import math
import pygame
from constants import BLUE, BLUE_DARK, BORDER, GREEN, INK, LAVENDER, MINT, MUTED, PINK, RED, WHITE, YELLOW
from exercise_loader import Exercise
from settings import Settings
from statistics import LessonStats
from theory import IMPORTANT_RULE, THEORY_PARAGRAPHS, WORKED_EXAMPLES

class UI:
    def __init__(self) -> None:
        self.buttons: dict[str, pygame.Rect] = {}
        self.fonts: dict[tuple[int, bool], pygame.font.Font] = {}

    def begin_frame(self) -> None:
        self.buttons.clear()

    def font(self, size: int, bold: bool = False) -> pygame.font.Font:
        key = (size, bold)
        if key not in self.fonts: self.fonts[key] = pygame.font.SysFont("arial", size, bold=bold)
        return self.fonts[key]

    def text(self, surface: pygame.Surface, value: str, pos: tuple[int, int], size: int, color=INK, center: bool = False, bold: bool = False) -> pygame.Rect:
        image = self.font(size, bold).render(value, True, color)
        rect = image.get_rect()
        if center: rect.center = pos
        else: rect.topleft = pos
        surface.blit(image, rect)
        return rect

    def wrap(self, surface: pygame.Surface, value: str, x: int, y: int, width: int, size: int) -> int:
        font = self.font(size)
        lines: list[str] = []
        line = ""
        for word in value.split():
            candidate = f"{line} {word}".strip()
            if line and font.size(candidate)[0] > width:
                lines.append(line); line = word
            else: line = candidate
        if line: lines.append(line)
        for item in lines:
            self.text(surface, item, (x, y), size)
            y += font.get_linesize() + 4
        return y

    def button(self, surface: pygame.Surface, key: str, label: str, rect: pygame.Rect, color=BLUE, size: int = 26) -> None:
        self.buttons[key] = rect
        pygame.draw.rect(surface, color, rect, border_radius=16)
        pygame.draw.rect(surface, WHITE, rect, 2, border_radius=16)
        self.text(surface, label, rect.center, size, center=True, bold=True)

    def hit(self, pos: tuple[int, int]) -> str | None:
        return next((key for key, rect in self.buttons.items() if rect.collidepoint(pos)), None)

    @staticmethod
    def cx(surface: pygame.Surface) -> int:
        return surface.get_width() // 2

    def draw_menu(self, s: pygame.Surface, size: int) -> None:
        cx = self.cx(s)
        self.text(s, "Desetinná čísla", (cx, 75), size+22, center=True, bold=True)
        self.text(s, "Matematické dobrodružství", (cx, 125), size, MUTED, center=True)
        choices = (("add", "Sčítání", BLUE), ("subtract", "Odčítání", PINK), ("mixed", "Sčítání + odčítání", LAVENDER), ("theory", "Teorie", YELLOW))
        for i, (key, label, color) in enumerate(choices):
            self.button(s, key, label, pygame.Rect(cx-210, 165+i*77, 420, 66), color, size)
        y = min(s.get_height()-65, 165+4*77+5)
        for key, label, x, color in (("stats","Statistiky",cx-320,YELLOW),("settings","Nastavení",cx-100,LAVENDER),("quit","Konec",cx+120,PINK)):
            self.button(s, key, label, pygame.Rect(x,y,200,54), color, max(18,size-4))

    def draw_stats(self, s: pygame.Surface, stats: LessonStats, target: int, size: int) -> None:
        msg = f"Vyřešeno {stats.solved}/{target}   Správně {stats.correct}   Chybně {stats.incorrect}   Úspěšnost {stats.accuracy:.0f} %   Série {stats.current_streak}"
        self.text(s, msg, (self.cx(s), 24), max(16,size-8), MUTED, center=True)

    def draw_game(self, s: pygame.Surface, ex: Exercise, answer: str, stats: LessonStats, target: int, size: int, feedback: str | None, correct: bool, elapsed: float) -> None:
        self.draw_stats(s, stats, target, size)
        cx, cy = self.cx(s), s.get_height()//2
        panel = pygame.Rect(cx-440,cy-210,880,400)
        pygame.draw.rect(s,WHITE,panel,border_radius=26); pygame.draw.rect(s,BORDER,panel,3,border_radius=26)
        self.text(s,"Kolik to je?",(cx,cy-150),size,MUTED,center=True)
        self.text(s,ex.question,(cx,cy-75),size+20,INK,center=True,bold=True)
        entry=pygame.Rect(cx-210,cy-5,420,70); color=GREEN if feedback and correct else RED if feedback else BLUE_DARK
        pygame.draw.rect(s,WHITE,entry,border_radius=14); pygame.draw.rect(s,color,entry,4,border_radius=14)
        self.text(s,answer or "Zadej výsledek…",entry.center,size+4,INK if answer else MUTED,center=True)
        if feedback:
            self.text(s,feedback,(cx,cy+90),size,GREEN if correct else RED,center=True,bold=True)
            self.button(s,"continue","Pokračovat  ↵",pygame.Rect(cx-130,cy+125,260,54),YELLOW,max(18,size-4))
        else: self.text(s,"Zadej číslo a stiskni ENTER. Lze použít čárku i tečku.",(cx,cy+100),max(16,size-7),MUTED,center=True)
        if correct:
            for i in range(5):
                angle=elapsed*3.2+i*math.tau/5; radius=110+(elapsed*40)%60
                pygame.draw.circle(s,YELLOW,(int(cx+math.cos(angle)*radius),int(cy-75+math.sin(angle)*radius*.6)),8)
        self.button(s,"home","Menu",pygame.Rect(25,s.get_height()-65,145,45),LAVENDER,18)

    def draw_settings(self,s:pygame.Surface,settings:Settings,size:int)->None:
        cx=self.cx(s); self.text(s,"Nastavení",(cx,75),size+18,center=True,bold=True)
        rows=(("volume","Hlasitost zvuků",f"{round(settings.volume*100)} %"),("fullscreen","Režim obrazovky","Celá obrazovka" if settings.fullscreen else "Okno"),("font","Velikost písma",str(settings.font_size)),("length","Počet příkladů",str(settings.lesson_length)))
        for i,(key,label,value) in enumerate(rows):
            y=145+i*90; self.text(s,label,(cx-300,y+16),size)
            self.button(s,key,value,pygame.Rect(cx+120,y,270,58),(BLUE,LAVENDER,YELLOW,PINK)[i],max(18,size-3))
        self.button(s,"home","Zpět do menu",pygame.Rect(cx-145,s.get_height()-75,290,54),MINT)

    def draw_statistics(self,s:pygame.Surface,stats:LessonStats,size:int)->None:
        cx=self.cx(s); self.text(s,"Statistiky poslední lekce",(cx,100),size+10,center=True,bold=True)
        vals=(f"Vyřešené příklady: {stats.solved}",f"Správné odpovědi: {stats.correct}",f"Chybné odpovědi: {stats.incorrect}",f"Úspěšnost: {stats.accuracy:.0f} %",f"Nejdelší série: {stats.best_streak}")
        for i,v in enumerate(vals): self.text(s,v,(cx,210+i*55),size,center=True)
        self.button(s,"home","Zpět do menu",pygame.Rect(cx-145,s.get_height()-85,290,54),MINT)

    def draw_theory(self,s:pygame.Surface,size:int,scroll:int)->None:
        cx=self.cx(s); self.text(s,"Teorie",(cx,35),size+14,center=True,bold=True); y=75-scroll
        for p in THEORY_PARAGRAPHS: y=self.wrap(s,p,75,y,s.get_width()-150,max(16,size-8))+3
        rule=pygame.Rect(75,y,s.get_width()-150,48); pygame.draw.rect(s,YELLOW,rule,border_radius=12)
        self.text(s,IMPORTANT_RULE,rule.center,max(18,size-3),center=True,bold=True); y+=57
        self.text(s,"Řešené příklady",(75,y),max(18,size-3),bold=True); y+=32
        w=min(210,(s.get_width()-170)//5); gap=10; x0=(s.get_width()-(5*w+4*gap))//2
        for i,e in enumerate(WORKED_EXAMPLES):
            x=x0+i*(w+gap); card=pygame.Rect(x,y,w,132); pygame.draw.rect(s,WHITE,card,border_radius=12); pygame.draw.rect(s,BORDER,card,2,border_radius=12)
            for j,line in enumerate((e.first,f"{e.operator} {e.second}","──────",e.result)): self.text(s,line,(x+14,y+9+j*27),max(16,size-10),BLUE_DARK if "," in line else INK,bold=j==3)
        self.text(s,"Tip: Chybějící desetinné místo můžeš doplnit nulou.",(cx,min(s.get_height()-40,y+145),),max(16,size-9),MUTED,center=True)
        self.button(s,"home","Zpět do menu",pygame.Rect(20,s.get_height()-58,180,42),MINT,18)

    def draw_summary(self,s:pygame.Surface,stats:LessonStats,target:int,size:int)->None:
        cx=self.cx(s); p=stats.accuracy
        grade="Výborně!" if p==100 else "Skvělá práce!" if p>=90 else "Velmi dobře!" if p>=75 else "Dobře, ještě trénuj." if p>=50 else "Ještě procvičuj."
        self.text(s,"Lekce dokončena!",(cx,95),size+18,center=True,bold=True); self.text(s,grade,(cx,185),size+12,GREEN if p>=75 else BLUE_DARK,center=True,bold=True)
        for i,v in enumerate((f"Úspěšnost: {p:.0f} %",f"Správně: {stats.correct} z {target}",f"Chybně: {stats.incorrect}",f"Nejdelší série: {stats.best_streak}")): self.text(s,v,(cx,275+i*45),size,center=True)
        self.button(s,"again","Další lekce",pygame.Rect(cx-245,s.get_height()-88,220,56),BLUE)
        self.button(s,"home","Hlavní menu",pygame.Rect(cx+25,s.get_height()-88,220,56),MINT)

    def draw_message(self,s:pygame.Surface,message:str,size:int)->None:
        cx,cy=self.cx(s),s.get_height()//2; panel=pygame.Rect(90,cy-140,s.get_width()-180,280)
        pygame.draw.rect(s,WHITE,panel,border_radius=22); pygame.draw.rect(s,BORDER,panel,3,border_radius=22)
        self.wrap(s,message,130,cy-50,s.get_width()-260,size)
        self.button(s,"home","Zpět do menu",pygame.Rect(cx-145,cy+55,290,54),MINT)
