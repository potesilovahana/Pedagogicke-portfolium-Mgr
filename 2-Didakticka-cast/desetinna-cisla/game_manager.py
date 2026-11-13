"""Hlavní řízení aplikace."""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
import pygame
from constants import BACKGROUND, DATA_DIR, SOUNDS_DIR, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from exercise_loader import Exercise, ExerciseLoader
from settings import Settings
from statistics import LessonStats
from ui import UI

class GameManager:
    MODE_FILES={"add":"scitani.txt","subtract":"odcitani.txt","mixed":"kombinovane.txt"}
    def __init__(self,settings:Settings)->None:
        self.settings=settings; flags=pygame.FULLSCREEN if settings.fullscreen else pygame.RESIZABLE
        self.screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),flags); pygame.display.set_caption(WINDOW_TITLE)
        self.clock=pygame.time.Clock(); self.ui=UI(); self.loader=ExerciseLoader(); self.state="menu"; self.message=""
        self.lesson:list[Exercise]=[]; self.lesson_index=0; self.stats=LessonStats(); self.last_stats=LessonStats()
        self.answer_input=""; self.feedback:str|None=None; self.feedback_correct=False; self.feedback_time=0.0; self.theory_scroll=0
        self.sounds:dict[str,pygame.mixer.Sound]={}; self.load_sounds()
    def load_sounds(self)->None:
        if not pygame.mixer.get_init(): return
        for name in ("success","error","finish"):
            try:
                path=SOUNDS_DIR/f"{name}.wav"
                if path.is_file(): self.sounds[name]=pygame.mixer.Sound(str(path))
            except (pygame.error,OSError): pass
    def play_sound(self,name:str)->None:
        try:
            if name in self.sounds: self.sounds[name].set_volume(self.settings.volume); self.sounds[name].play()
        except pygame.error: pass
    def start_lesson(self,mode:str)->None:
        try: self.lesson=self.loader.make_lesson(self.loader.load(self.MODE_FILES[mode],DATA_DIR),self.settings.lesson_length)
        except (KeyError,ValueError) as exc: self.message=str(exc); self.state="message"; return
        self.stats=LessonStats(); self.lesson_index=0; self.answer_input=""; self.feedback=None; self.state="game"
    def submit_answer(self)->None:
        if self.feedback is not None or not self.answer_input.strip(): return
        try: entered=Decimal(self.answer_input.strip().replace(",","."))
        except InvalidOperation: self.feedback="Zadej prosím platné číslo."; self.feedback_correct=False; self.feedback_time=pygame.time.get_ticks()/1000; return
        self.feedback_correct=entered==self.lesson[self.lesson_index].answer; self.stats.record(self.feedback_correct)
        if self.feedback_correct: self.feedback="Správně! Výborná práce!"; self.play_sound("success")
        else: self.feedback=f"To nevadí. Správná odpověď je {self.lesson[self.lesson_index].answer_text}."; self.play_sound("error")
        self.feedback_time=pygame.time.get_ticks()/1000
    def advance(self)->None:
        if self.feedback is None:return
        self.lesson_index+=1; self.answer_input=""; self.feedback=None
        if self.lesson_index>=len(self.lesson): self.last_stats=self.stats; self.play_sound("finish"); self.state="summary"
    def handle_click(self,pos:tuple[int,int])->None:
        action=self.ui.hit(pos)
        if action in self.MODE_FILES:self.start_lesson(action)
        elif action=="quit":pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif action=="settings":self.state="settings"
        elif action=="stats":self.state="stats"
        elif action=="theory":self.theory_scroll=0; self.state="theory"
        elif action=="home":self.state="menu"
        elif action=="continue":self.advance()
        elif action=="again":self.start_lesson("mixed")
        elif action=="volume":
            vals=(0.0,0.3,0.6,1.0); i=min(range(4),key=lambda j:abs(vals[j]-self.settings.volume)); self.settings.volume=vals[(i+1)%4]; self.settings.save()
        elif action=="fullscreen":
            self.settings.fullscreen=not self.settings.fullscreen; flags=pygame.FULLSCREEN if self.settings.fullscreen else pygame.RESIZABLE
            self.screen=pygame.display.set_mode((0,0) if self.settings.fullscreen else (WINDOW_WIDTH,WINDOW_HEIGHT),flags); self.settings.save()
        elif action=="font":
            vals=(20,24,28,32); i=vals.index(self.settings.font_size) if self.settings.font_size in vals else 1; self.settings.font_size=vals[(i+1)%4]; self.settings.save()
        elif action=="length":
            vals=(10,20,30,50); i=vals.index(self.settings.lesson_length); self.settings.lesson_length=vals[(i+1)%4]; self.settings.save()
    def handle_event(self,event:pygame.event.Event)->bool:
        if event.type==pygame.QUIT:return False
        if event.type==pygame.VIDEORESIZE and not self.settings.fullscreen:self.screen=pygame.display.set_mode((max(960,event.w),max(600,event.h)),pygame.RESIZABLE)
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:self.handle_click(event.pos)
        if self.state=="game" and event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:self.state="menu"
            elif self.feedback is not None and event.key in (pygame.K_RETURN,pygame.K_KP_ENTER):self.advance()
            elif self.feedback is None:
                if event.key in (pygame.K_RETURN,pygame.K_KP_ENTER):self.submit_answer()
                elif event.key==pygame.K_BACKSPACE:self.answer_input=self.answer_input[:-1]
                elif event.unicode and event.unicode in "0123456789,.-":self.answer_input+=event.unicode
        elif self.state=="theory":
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:self.state="menu"
            elif event.type==pygame.MOUSEWHEEL:self.theory_scroll=min(120,max(0,self.theory_scroll-event.y*25))
            elif event.type==pygame.KEYDOWN and event.key in (pygame.K_UP,pygame.K_DOWN):self.theory_scroll=min(120,max(0,self.theory_scroll+(25 if event.key==pygame.K_DOWN else -25)))
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE and self.state!="menu":self.state="menu"
        return True
    def render(self)->None:
        self.screen.fill(BACKGROUND); self.ui.begin_frame(); size=self.settings.font_size
        if self.state=="menu":self.ui.draw_menu(self.screen,size)
        elif self.state=="game" and self.lesson:self.ui.draw_game(self.screen,self.lesson[self.lesson_index],self.answer_input,self.stats,len(self.lesson),size,self.feedback,self.feedback_correct,pygame.time.get_ticks()/1000-self.feedback_time)
        elif self.state=="settings":self.ui.draw_settings(self.screen,self.settings,size)
        elif self.state=="stats":self.ui.draw_statistics(self.screen,self.last_stats,size)
        elif self.state=="theory":self.ui.draw_theory(self.screen,size,self.theory_scroll)
        elif self.state=="summary":self.ui.draw_summary(self.screen,self.last_stats,len(self.lesson),size)
        elif self.state=="message":self.ui.draw_message(self.screen,self.message,size)
        pygame.display.flip()
    def run(self)->None:
        running=True
        while running:
            for event in pygame.event.get():
                if not self.handle_event(event):running=False; break
            self.render(); self.clock.tick(60)
