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
        label_n = TextMobject(" n ")
        label_n.move_to([6.5, 0.4, 0])
        label_n.set_color(RED)
        self.play(Write(label_n), run_time=1)
        self.wait(1)

        conv_text = TextMobject("Convolution:")
        conv_text.move_to([-5.3, 3.5, 0])
        self.play(Write(conv_text))
        self.wait(1)

        conv_formula = TextMobject("""
            {\\small $x[n]*h[n]=\sum\limits_{k=-\infty}^{+\infty}x[k]h[n-k]$}
        """)
        conv_formula.move_to([-3.5, 2.7, 0])
        self.play(Write(conv_formula))
        self.wait(1)


        # drawing x:
        tx = np.array(range(-7, 7, 1))
        yx = 3 * np.sin(tx)

        gx1 = VGroup()

        # creating lines
        for i in range(len(tx)):
            lx1 = Line([tx[i]/2, 0, 0], [tx[i]/2, yx[i]/2, 0])
            lx1.set_color(GREEN)
            gx1.add(lx1)

        # creating dots
        for i in range(len(tx)):
            dx1 = Dot([tx[i]/2, yx[i]/2, 0])
            dx1.set_color(GREEN)
            gx1.add(dx1)

        
        # drawing them
        self.play(Write(gx1))


        xn_text = TextMobject("""
            $$x[n]$$
        """)
        xn_text.set_color(GREEN)
        xn_text.move_to([4, 3, 0])
        self.play(Write(xn_text))

        self.wait(1)


        # drawing h:

        th = np.array(range(-2, 2, 1))
        yh = 2 * np.cos(th)
        
        gh1 = VGroup()
        gh2 = VGroup()

        # creating lines
        for i in range(len(th)):
            lh1 = Line([th[i]/2, 0, 0], [th[i]/2, yh[i]/2, 0])
            lh1.set_color(BLUE)
            gh1.add(lh1)

            lh2 = Line([-th[i]/2, 0, 0], [-th[i]/2, yh[i]/2, 0])
            lh2.set_color(BLUE)
            gh2.add(lh2)

        # creating dots
        for i in range(len(th)):
            dh1 = Dot([th[i]/2, yh[i]/2, 0])
            dh1.set_color(BLUE)
            gh1.add(dh1)
            dh2 = Dot([-th[i]/2, yh[i]/2, 0])
            dh2.set_color(BLUE)
            gh2.add(dh2)


        # drawing h[n]
        self.play(Write(gh1))
        self.wait(1)

        hn_text = TextMobject("""
            $$h[n]$$
        """)
        hn_text.set_color(BLUE)
        hn_text.move_to([4, 2.3, 0])
        self.play(Write(hn_text))
        self.wait(1)

        # removing convolution text and formula
        self.play(FadeOut(conv_text), FadeOut(conv_formula))

        # step 1: n -> k
        n_to_k = TextMobject("""$$Step \\; 1: \\; n \\rightarrow k$$""")
        n_to_k.move_to([-5, 3, 0])
        self.play(Write(n_to_k))

        xk_text = TextMobject("""
            $$x[k]$$
        """)
        xk_text.set_color(GREEN)
        xk_text.move_to([4, 3, 0])

        hk_text = TextMobject("""
            $$h[k]$$
        """)
        hk_text.set_color(BLUE)
        hk_text.move_to([4, 2.3, 0])
        
        label_k = TextMobject(" k ")
        label_k.move_to([6.5, 0.4, 0])
        label_k.set_color(RED)

        self.play(
            Transform(xn_text, xk_text),
            ReplacementTransform(hn_text, hk_text),
            Transform(label_n, label_k)
        )

        self.wait(1)


        # step 2: h[k] -> h[-k]
        self.play(FadeOut(n_to_k))

        hk_to_hmk = TextMobject("""$Step \\; 2: \\; h[k] \\rightarrow h[-k]$""")
        hk_to_hmk.move_to([-4, 3, 0])
        self.play(Write(hk_to_hmk))

        self.wait(1)

        hmk_text = TextMobject("""
            $$h[-k]$$
        """)
        hmk_text.set_color(BLUE)
        hmk_text.move_to([4, 2.3, 0])

        # drawing h[-k]
        self.play(Transform(gh1, gh2), ReplacementTransform(hk_text, hmk_text))
        self.wait(1)


        # step 3: moving window and multiply 
        self.play(FadeOut(hk_to_hmk))

        wind_and_multiply = TextMobject("Step 3: Moving Window")
        wind_and_multiply.move_to([-4, 3, 0])
        self.play(Write(wind_and_multiply))
        
        self.wait(1)


        # moving h[-k] to left
        self.remove(gh1)
        self.play(gh2.shift, [-6, 0, 0], run_time=1.5)
        self.wait(1)

        # drawing window
        tw_min = -th[len(th) - 1]
        tw_max = -th[0]
        yw_min = min(*yx)
        yw_max = max(*yx)

        rect = Polygon([tw_min/2-1/4, yw_min/2-1/4, 0], [tw_max/2+1/4, yw_min/2-1/4, 0],
                [tw_max/2+1/4, yw_max/2+1/4, 1], [tw_min/2-1/4, yw_max/2+1/4, 0])
        rect.set_color(WHITE)
        rect.shift([-6, 0, 0])
        self.play(Write(rect))

        self.wait(1)

        # writing h[n - k]
        h_nmk = TextMobject("{\\footnotesize$h[ %d -k]$}" % (tw_min - 11))
        h_nmk.set_color(BLUE)
        h_nmk.move_to([-6 + (tw_min + tw_max)/4, yw_max/2+1/2 + 0.05, 0])
        self.play(ReplacementTransform(hmk_text, h_nmk))

        self.wait(1)

        # moving the window and h[n - k]
        window = VGroup(gh2, rect, h_nmk)

        for i in range(22):
            next_h_nmk = TextMobject("{\\footnotesize$h[ %d -k]$}" % (tw_min - 11 + i + 1))
            next_h_nmk.set_color(BLUE)
            next_h_nmk.move_to([-6 + (tw_min + tw_max)/4 + 0.5 * i + 0.5, yw_max/2+1/2 + 0.05, 0])
            self.play(window.shift, [0.5, 0, 0], Transform(h_nmk, next_h_nmk), run_time=0.5)
            self.wait(1)

        
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