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

        label_t = TextMobject(" t ")
        label_t.move_to([6.5, 0.4 + y0, 0])
        label_t.set_color(RED)
        self.play(Write(label_t), run_time=1)
        self.wait(1)

        conv_text = TextMobject("Convolution:")
        conv_text.move_to([-5.3, 3, 0])
        self.play(Write(conv_text))
        self.wait(1)

        conv_formula = TextMobject("""
            {\\small $y(t)=\int\limits_{-\infty}^{\infty}x(\\tau)h(t-\\tau)d\\tau$}
        """)
        conv_formula.move_to([-4.1, 2.2, 0])
        self.play(Write(conv_formula))
        self.wait(1)


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

        xt_text = TextMobject("""
            $$x(t)=u(t+1)-u(t-1)$$
        """)
        xt_text.set_color(GREEN)
        xt_text.move_to([4, 3, 0])
        self.play(Write(xt_text))
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

        ht_text = TextMobject("""
            $$h(t)=u(t)$$
        """)
        ht_text.set_color(BLUE)
        ht_text.move_to([4, 2.3, 0])
        self.play(Write(ht_text))
        self.wait(1)

        # removing convolution text and putting the formula in a corner
        corner_conv_formula = TextMobject("""
                    {\\small $y(t)=\int\limits_{-\infty}^{\infty}x(\\tau)h(t-\\tau)d\\tau$}
                """)
        corner_conv_formula.move_to([-4.7, 3, 0])
        corner_conv_formula.scale(0.6)
        self.play(FadeOut(conv_text), Transform(conv_formula, corner_conv_formula))
        self.wait(1)

        #drawing convolution rect
        convolution_rect = Polygon([-6.7, 2.6, 0], [-2.7, 2.6, 0],
                              [-2.7, 3.4, 0], [-6.7, 3.4, 0])
        convolution_rect.set_color(WHITE)
        self.play(Write(convolution_rect))
        self.wait(1)


        # step 1: t -> tau
        t_to_tau = TextMobject("""$$Step \\ 1: \\; t \\rightarrow \\tau$$""")
        t_to_tau.move_to([-5.05, 2.2, 0])
        self.play(Write(t_to_tau))
        self.wait(1)

        xtau_text = TextMobject("""
            $$x(\\tau)=u(\\tau+1)-u(\\tau-1)$$
        """)
        xtau_text.set_color(GREEN)
        xtau_text.move_to([4, 3, 0])

        htau_text = TextMobject("""
            $$h(\\tau)$$
        """)
        htau_text.set_color(BLUE)
        htau_text.move_to([4, 2.3, 0])

        label_tau = TextMobject("""$$\\tau$$""")
        label_tau.move_to([6.5, 0.4 + y0, 0])
        label_tau.set_color(RED)

        self.play(
            Transform(xt_text, xtau_text),
            ReplacementTransform(ht_text, htau_text),
            Transform(label_t, label_tau)
        )
        self.wait(1)


        # step 2: h(tau) -> h(-tau)
        self.play(FadeOut(t_to_tau))
        htau_to_hmtau = TextMobject("""$Step \\ 2: \\; h(\\tau) \\rightarrow h(-\\tau)$""")
        htau_to_hmtau.move_to([-4.3, 2.2, 0])
        self.play(Write(htau_to_hmtau))
        self.wait(1)

        hmtau_text = TextMobject("""
            $$h(-\\tau)$$
        """)
        hmtau_text.set_color(BLUE)
        hmtau_text.move_to([4, 2.3, 0])

        # drawing u(-tau)
        umk = VGroup()
        um1 = Line([-12, 1 + y0, 0], [0, 1 + y0, 0])
        um1.set_color(BLUE)
        um2 = Line([0, 1 + y0, 0], [0, y0, 0])
        um2.set_color(BLUE)
        um3 = Line([0, y0, 0], [12, y0, 0])
        um3.set_color(BLUE)

        umk.add(um1, um2, um3)
        self.play(ReplacementTransform(u1, um3), ReplacementTransform(u3, um1), Write(um2),
            ReplacementTransform(htau_text, hmtau_text))
        self.remove(u2)
        self.wait(1)


        # step 3: moving window and multiply
        self.play(FadeOut(htau_to_hmtau))

        wind_and_multiply = TextMobject("Step 3 \\ : Moving Window")
        wind_and_multiply.move_to([-3.7, 2.2, 0])
        self.play(Write(wind_and_multiply))
        self.wait(1)


        # moving u(-k) to the left
        offset = -4
        self.play(umk.shift, [offset, 0, 0], run_time=1.5)
        self.wait(1)


        # drawing an extra number line for the result of convolution
        yz = -0.5
        number_line = NumberLine(y_min=-8, y_max=8, unit_size=1, numbers_with_elongated_ticks=[])
        number_line.set_stroke(width=1)
        number_line.move_to([0, yz, 0])
        self.play(Write(number_line))
        self.wait(1)


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
        y1 = Line([-4, yz, 0], [-1, yz, 0])
        y1.set_color(ORANGE)
        y2 = Line([-1, 0 + yz, 0], [1, 2 + yz, 0])
        y2.set_color(ORANGE)
        y3 = Line([1, 2 + yz, 0], [4, 2 + yz, 0])
        y3.set_color(ORANGE)

        y.add(y1, y2, y3)


        # moving window
        self.play(
            umk.shift, [3, 0, 0],
            t_value.set_value, -1,
            ShowCreation(y1),
            rate_func=linear,
            run_time=4
        )


        # handing the area
        one = self.get_graph(lambda x: 1, x_min=-1, x_max=1)
        area = self.color_area(one, -1, 1)
        self.get_area
        area.set_color(YELLOW)

        self.play(
            umk.shift, [2, 0, 0],
            t_value.set_value, 1,
            ShowCreation(area),
            ShowCreation(y2),
            rate_func=linear,
            run_time=4
        )

        self.play(
            umk.shift, [3, 0, 0],
            t_value.set_value, 3,
            ShowCreation(y3),
            rate_func=linear,
            run_time=4
        )

        self.wait(2)

        # removing stuff
        self.play(FadeOut(umk), FadeOut(group), FadeOut(label_tau),
            FadeOut(rt), FadeOut(area), FadeOut(xtau_text), FadeOut(self.x_axis))
        self.play(FadeOut(convolution_rect), FadeOut(corner_conv_formula), FadeOut(conv_formula), FadeOut(xt_text),
            FadeOut(hmtau_text), FadeOut(label_t), FadeOut(wind_and_multiply))

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

    def color_area(self, graph, t_min, t_max):
        numerator = max(t_max - t_min, 0.0001)
        dx = float(numerator) / 1000
        return self.get_riemann_rectangles(
            graph,
            x_min=t_min,
            x_max=t_max,
            dx=dx,
            stroke_width=0,
        ).set_fill(opacity=0.5)