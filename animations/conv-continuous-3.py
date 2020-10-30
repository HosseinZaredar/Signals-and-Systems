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

        # Introduction
        title = TextMobject("Continuous Convolution \#3")
        title.scale(2)
        creators = TextMobject("Made by \n Hossein Zaredar \& Matin Tavakoli")
        creators.scale(0.4)
        creators.move_to([5, -3.7, 0])
        self.play(Write(title), run_time=1.2)
        self.wait(2)
        self.play(Write(creators), run_time=0.7)
        self.wait(2)
        self.play(FadeOut(title))
        self.wait(2)

        self.setup_axes()

        # y0
        y0 = -2.5

        label_t = TextMobject(" t ")
        label_t.move_to([6.5, 0.4 + y0, 0])
        label_t.set_color(RED)
        self.play(Write(label_t), run_time=1)
        self.wait(1)

        conv_text = TextMobject("Continuous Convolution:")
        conv_text.move_to([-4, 3, 0])
        self.play(Write(conv_text))
        self.wait(0.2)

        conv_formula = TextMobject(
            "{\\small $y(t)=$}",
            "{\\small $\\ x(t)*h(t)=$}",
            "{\\small $\int\limits_{-\infty}^{\infty}x(\\tau)h(t-\\tau)d\\tau$}"
        )
        conv_formula.scale(0.85)
        conv_formula.move_to([-3.5, 2.2, 0])
        self.play(Write(conv_formula))
        self.wait(1)


        # drawing x(x) = sin(t)

        # dots 1
        dots_1 = TextMobject("...")
        dots_1.move_to([-5.3, y0 + 0.85, 0])
        dots_1.rotate(0.35)
        dots_1.scale(1.3)
        dots_1.set_color(GREEN)
        self.play(Write(dots_1))

        xt = self.get_graph(lambda x : np.sin(x), color = GREEN, x_min = -5,  x_max = 5)
        self.play(ShowCreation(xt, run_time=2))
        
        # dots 2
        dots_2 = TextMobject("...")
        dots_2.move_to([5.3, y0 - 0.85, 0])
        dots_2.rotate(0.35)
        dots_2.scale(1.3)
        dots_2.set_color(GREEN)
        self.play(Write(dots_2))

        self.wait(1)

        xt_text = TextMobject("""
            $$x(t)=sin(t)$$
        """)
        xt_text.set_color(GREEN)
        xt_text.move_to([3.5, 3, 0])
        self.play(Write(xt_text))
        self.wait(1)


        # drawing h(t) = delta(t)
        ht = Arrow([0, y0 - 0.25, 0], [0, 1.25 + y0, 0])
        ht.set_color(BLUE)
        self.play(ShowCreation(ht, run_time=0.5))
        self.wait(1)

        ht_text = TextMobject("""
            $$h(t)=\\delta (t)$$
        """)
        ht_text.set_color(BLUE)
        ht_text.move_to([3.5, 2.3, 0])
        self.play(Write(ht_text))
        self.wait(1)

        # removing convolution text and putting the formula in a corner
        corner_conv_formula = TextMobject(
            "{\\small $y(t)=$}",
            "{\\small $\int\limits_{-\infty}^{\infty}x(\\tau)h(t-\\tau)d\\tau$}"
        )

        corner_conv_formula.move_to([-3.5, 3, 0])
        corner_conv_formula.scale(0.8)
        self.play(
            FadeOut(conv_text),
            FadeOut(conv_formula[1]),
            ReplacementTransform(conv_formula[0], corner_conv_formula[0]),
            ReplacementTransform(conv_formula[2], corner_conv_formula[1])
        )
        self.wait(0.2)

        #drawing convolution rect
        convolution_rect = Polygon([-5.45, 2.55, 0], [-1.6, 2.55, 0],
                              [-1.6, 3.45, 0], [-5.45, 3.45, 0])
        convolution_rect.set_color(WHITE)
        convolution_rect.scale(1.1)
        self.play(Write(convolution_rect))
        self.wait(1)


        # step 1: t -> tau
        t_to_tau = TextMobject("""$$Step \\ 1: \\; t \\rightarrow \\tau$$""")
        t_to_tau.scale(0.9)
        t_to_tau.move_to([-3.5, 2.1, 0])
        self.play(Write(t_to_tau))
        self.wait(1)

        xtau_text = TextMobject("""
            $$x(\\tau)=sin(\\tau)$$
        """)
        xtau_text.set_color(GREEN)
        xtau_text.move_to([3.5, 3, 0])

        htau_text = TextMobject("""
            $$h(\\tau)=\\delta (\\tau)$$
        """)
        htau_text.set_color(BLUE)
        htau_text.move_to([3.5, 2.3, 0])

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
        htau_to_hmtau.scale(0.9)
        htau_to_hmtau.move_to([-3.5, 2.1, 0])
        self.play(Write(htau_to_hmtau))
        self.wait(1)

        hmtau_text = TextMobject("""
            $$h(-\\tau)=\\delta (-\\tau)$$
        """)
        hmtau_text.set_color(BLUE)
        hmtau_text.move_to([3.5, 2.3, 0])

        # drawing h(-tau) = u(-tau)
        hmtau = Arrow([0, y0 - 0.25, 0], [0, 1.25 + y0, 0])
        hmtau.set_color(BLUE)
        hmtau.flip()

        self.play(ReplacementTransform(ht, hmtau), ReplacementTransform(htau_text, hmtau_text))
        self.wait(1)


        # step 3: moving window and multiply
        self.play(FadeOut(htau_to_hmtau))

        wind_and_multiply = TextMobject("Step 3 \\ : Sliding Window")
        wind_and_multiply.scale(0.9)
        wind_and_multiply.move_to([-3.5, 2.1, 0])

        guide_1 = TextMobject("""
            for all t: take the integral of 
        """)
        guide_1.scale(0.75)
        guide_1.move_to([-3.8, 0.6, 0])

        guide_2 = TextMobject("""
            the multiplication of the signals,
        """)
        guide_2.scale(0.75)
        guide_2.move_to([-3.5, 0.25, 0])

        guide_3 = TextMobject("""
            from $-\\infty$ to $+\\infty$. 
        """)
        guide_3.scale(0.75)
        guide_3.move_to([-4.7, -0.1, 0])
        
        self.play(Write(wind_and_multiply))
        self.wait(0.5)
        self.play(Write(guide_1))
        self.play(Write(guide_2))
        self.play(Write(guide_3))
        self.wait(2)

        self.play(FadeOut(guide_1), FadeOut(guide_2), FadeOut(guide_3))

        # moving window group
        window = VGroup()
        window.add(hmtau)
        offset = -5

        # arrow
        arr = Arrow([0, y0 - 0.8, 0], [0, y0 + 0.2, 0])
        self.play(Write(arr))
        window.add(arr)

        # moving window to the left
        self.play(
            hmtau.shift, [offset, 0, 0],
            arr.shift, [offset, 0, 0],
            run_time=2
        )
        self.wait(1)


        # ValueTracker for t
        t_label = TexMobject("t=", )
        t_label.scale(0.8)
        t_label.move_to([offset - 0.8, -3.3, 0])

        def t_updater(obj):
            val = t_value.get_value()
            obj.set_value(val)
            obj.move_to([val + 0, -3.3, 0])

        t_value = ValueTracker(offset)
        t_text = DecimalNumber(offset)
        t_text.scale(0.8)
        t_text.add_updater(t_updater)
        t_text.move_to([offset + 0, -3.3, 0])
        

        self.play(Write(t_text), Write(t_label))
        self.wait(1)

        window.add(t_label)


        # drawing an extra number line for the result of convolution
        yz = -0.5
        number_line = NumberLine(y_min=-8, y_max=8, unit_size=1, numbers_with_elongated_ticks=[])
        number_line.set_stroke(width=1)
        number_line.move_to([0, yz, 0])
        self.play(Write(number_line))

        y_text = TextMobject("y(t)")
        y_text.set_color(ORANGE)
        y_text.scale(0.8)
        y_text.move_to([-6, -0.1, 0])
        self.play(Write(y_text))
        self.wait(1)


        # creating the result of convolution
        yt = self.get_graph(lambda x : np.sin(x) - y0 + yz, color = ORANGE, x_min = -5,  x_max = 5)

        # dots 3
        dots_3 = TextMobject("...")
        dots_3.move_to([-5.3, yz + 0.85, 0])
        dots_3.rotate(0.35)
        dots_3.scale(1.3)
        dots_3.set_color(ORANGE)
        self.play(Write(dots_3))

        # moving window
        self.play(
            window.shift, [10, 0, 0],
            t_value.set_value, 5,
            ShowCreation(yt),
            rate_func=linear,
            run_time=10
        )

        # dots 4
        dots_4 = TextMobject("...")
        dots_4.move_to([5.3, yz - 0.85, 0])
        dots_4.rotate(0.35)
        dots_4.scale(1.3)
        dots_4.set_color(ORANGE)
        self.play(Write(dots_4))

        self.wait(2)

        # removing stuff
        self.play(FadeOut(hmtau), FadeOut(arr), FadeOut(t_label), FadeOut(t_text), FadeOut(label_tau), FadeOut(label_t),
            FadeOut(xt), FadeOut(xtau_text), FadeOut(self.x_axis), FadeOut(dots_1), FadeOut(dots_2))
        self.play(FadeOut(convolution_rect), FadeOut(corner_conv_formula), FadeOut(xt_text),
            FadeOut(hmtau_text), FadeOut(wind_and_multiply))


        t_yt = TextMobject(" t ")
        t_yt.set_color(ORANGE)
        t_yt.move_to([6.5, 0.4 + yz, 0])
        self.play(Write(t_yt))

        self.wait(3)


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