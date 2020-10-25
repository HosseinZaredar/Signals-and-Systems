#!/usr/bin/env python

from manimlib.imports import *

class Conv(GraphScene):
    CONFIG = {
        "y_max" : 9,
        "y_min" : -9,
        "x_max" : 18,
        "x_min" : -18,
        "y_tick_frequency" : 1,
        "x_tick_frequency" : 1,
        "graph_origin" : ORIGIN,
        "y_axis_label": None,
        "x_axis_label": None,
        "x_axis_width": 18,
        "y_axis_height": 9,
    }
    
    def construct(self):
        self.setup_axes()
        
        graph = self.get_graph(lambda x : 1/5 * np.exp(x), color = GREEN, x_min = -14, x_max = 5)
        self.play(ShowCreation(graph), run_time = 2)

        self.wait(2)


    def setup_axes(self):
        GraphScene.setup_axes(self)

        # width of edges
        self.x_axis.set_stroke(width=1)
        self.y_axis.set_stroke(width=1)

        # color of edges
        self.x_axis.set_color(RED)
        self.y_axis.set_color(RED)
        self.play(
            *[Write(objeto)
            for objeto in [self.y_axis, self.x_axis]],
            run_time=2
        )