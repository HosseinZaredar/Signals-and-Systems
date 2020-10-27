#!/usr/bin/env python

from manimlib.imports import *

class Conv(GraphScene):
    CONFIG = {
        "y_max" : 30,
        "y_min" : -10,
        "x_max" : 10,
        "x_min" : -10,
        "y_tick_frequency" : 1,
        "x_tick_frequency" : 1,
        "graph_origin" : [0, -2.5, 0],
        "y_axis_label": None,
        "x_axis_label": None,
        "x_axis_width": 20,
        "y_axis_height": 40,
    }
    
    def construct(self):
        self.setup_axes()

        # TODO play with rate_func 

        # y0
        y0 = -2.5


        # drawing rect = u(t + 2) - u(t - 2)
        rt = VGroup()
        r1 = Line([-8, y0, 0], [-1, y0, 0])
        r1.set_color(GREEN)
        r2 = Line([-1, y0, 0], [-1, 1 + y0, 0])
        r2.set_color(GREEN)
        r3 = Line([-1, 1 + y0, 0], [1, 1 + y0, 0])
        r3.set_color(GREEN)
        r4 = Line([1, 1 + y0, 0], [1, y0, 0])
        r4.set_color(GREEN)
        r5 = Line([1, y0, 0], [8, y0, 0])
        r5.set_color(GREEN)

        rt.add(r1, r2, r3, r4, r5)
        self.play(ShowCreation(r1, run_time=0.5))
        self.play(ShowCreation(r2, run_time=0.5))
        self.play(ShowCreation(r3, run_time=0.5))
        self.play(ShowCreation(r4, run_time=0.5))
        self.play(ShowCreation(r5, run_time=0.5))
        self.wait(1)


        # drawing u(t)
        ut = VGroup()
        u1 = Line([-12, y0, 0], [0, y0, 0])
        u1.set_color(BLUE)
        u2 = Line([0, y0, 0], [0, 1 + y0, 0])
        u2.set_color(BLUE)
        u3 = Line([0, 1 + y0, 0], [12, 1 + y0, 0])
        u3.set_color(BLUE)

        ut.add(u1, u2, u3)
        self.play(ShowCreation(u1, run_time=0.5))
        self.play(ShowCreation(u2, run_time=0.5))
        self.play(ShowCreation(u3, run_time=0.5))
        self.wait(1)


        # drawing u(-k)
        umk = VGroup()
        um1 = Line([-12, 1 + y0, 0], [0, 1 + y0, 0])
        um1.set_color(BLUE)
        um2 = Line([0, 1 + y0, 0], [0, y0, 0])
        um2.set_color(BLUE)
        um3 = Line([0, y0, 0], [12, y0, 0])
        um3.set_color(BLUE)

        umk.add(um1, um2, um3)
        self.play(ReplacementTransform(u1, um3), ReplacementTransform(u3, um1), Write(um2))
        self.remove(u2)
        self.wait(1)


        # moving u(-k) to the left
        offset = -3
        self.play(umk.shift, [offset, 0, 0], run_time=1.5)
        self.wait(1)


        # drawing an extra number line for the result of convolution
        number_line = NumberLine(x_min=-8, x_max=8, unit_size=1, numbers_with_elongated_ticks=[])
        self.play(Write(number_line))


        # ValueTracker for t
        t_value = ValueTracker(offset)
        t_text = DecimalNumber(t_value.get_value()).add_updater(lambda v: v.set_value(t_value.get_value()))
        x_label = TexMobject("t = ")
        group = VGroup(t_text, x_label)
        x_label.next_to(t_text, LEFT, buff=0.3, aligned_edge=x_label.get_bottom())

        self.add(group.move_to([0, -3.25, 0]))
        self.wait(1)


        # creating the result of convolution
        y = VGroup()
        y1 = Line([-3, 0, 0], [-1, 0, 0])
        y1.set_color(ORANGE)
        y2 = Line([-1, 0, 0], [1, 2, 0])
        y2.set_color(ORANGE)
        y3 = Line([1, 2, 0], [3, 2, 0])
        y3.set_color(ORANGE)

        y.add(y1, y2, y3)


        # moving window
        self.play(
            umk.shift, [2, 0, 0],
            t_value.set_value, -1,
            ShowCreation(y1),
            rate_func=linear,
            run_time=4
        )


        # TODO find a better way to do this
        # handing the area
        one = self.get_graph(lambda x: 1, x_min=-1, x_max=1)
        area = self.get_area(one, -1, 1)
        area.set_color(YELLOW) # TODO improve the color

        self.play(
            umk.shift, [2, 0, 0],
            t_value.set_value, 1,
            ShowCreation(area),
            ShowCreation(y2),
            rate_func=linear,
            run_time=4
        )

        self.play(
            umk.shift, [2, 0, 0],
            t_value.set_value, 3,
            ShowCreation(y3),
            rate_func=linear,
            run_time=4
        )

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
