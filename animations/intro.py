#!/usr/bin/env python

from manimlib.imports import *

class Intro(Scene):

    def construct(self):

        # Introduction
        title_l1 = TextMobject("CT Fourier Series")
        title_l2 = TextMobject("Real Signals (Epicycles) \\#1")
        title_l1.scale(1.8)
        title_l2.scale(1.25)
        title_l1.shift([0, 0.5, 0])
        title_l2.shift([0, -0.37, 0])
        line = Line([-4.6, 0, 0], [4.6, 0, 0])
        line.set_stroke(WHITE, 1.1, 1)
        creators = TextMobject("Made by Hossein Zaredar \& Matin Tavakoli")
        creators.scale(0.4)
        creators.move_to([5, -3.7, 0])
        self.add(title_l1)
        self.add(title_l2)
        self.add(line)
        self.wait(2)
        self.play(Write(creators), run_time=0.7)
        self.wait(2)
        self.play(FadeOut(title_l1), FadeOut(title_l2), FadeOut(line), FadeOut(creators))
        self.wait(1.5)

        