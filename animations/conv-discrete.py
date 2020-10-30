#!/usr/bin/env python

from manimlib.imports import *


class Conv(MovingCameraScene):

    def construct(self):

        y0 = -0.5

        # drawing axes
        self.wait(0.5)
        x_axis = NumberLine(x_min=-16, x_max=16, unit_size=0.5, numbers_with_elongated_ticks=[])
        x_axis.set_stroke(width=1)
        x_axis.shift([0, y0, 0])
        x_axis.set_color(RED)
        y_axis = NumberLine(x_min=-10, x_max=10, unit_size=0.5, numbers_with_elongated_ticks=[])
        y_axis.set_stroke(width=1)
        y_axis.set_color(RED)
        y_axis.rotate(PI / 2)
        self.play(Write(x_axis), Write(y_axis))


        label_n = TextMobject(" n ")
        label_n.move_to([6.5, 0.4 + y0, 0])
        label_n.set_color(RED)
        self.play(Write(label_n), run_time=1)
        self.wait(1)

        conv_text = TextMobject("Convolution:")
        conv_text.move_to([-5.35, 3, 0])
        self.play(Write(conv_text))
        self.wait(1)

        conv_formula = TextMobject(
            "{\\small $y[n]=$}", 
            "{\\small $\\ x[n]*h[n]=$}",
            "{\\small $\sum\limits_{k=-\infty}^{+\infty}x[k]h[n-k]$}"
        )
        conv_formula.scale(0.85)
        conv_formula.move_to([-3.5, 2.2, 0])
        self.play(Write(conv_formula))
        self.wait(1)

        # drawing x:
        tx = np.array(range(-6, 6, 1))
        yx = 2 * np.sin(tx)

        gx1 = VGroup()

        # creating lines
        for i in range(len(tx)):
            lx1 = Line([tx[i] / 2, 0, 0], [tx[i] / 2, yx[i] / 2, 0])
            lx1.set_color(GREEN)
            gx1.add(lx1)

        # creating dots
        for i in range(len(tx)):
            dx1 = Dot([tx[i] / 2, yx[i] / 2, 0])
            dx1.set_color(GREEN)
            gx1.add(dx1)

        # drawing them
        gx1.shift([0, y0, 0])
        self.play(Write(gx1))

        xn_text = TextMobject("""
            $$x[n]$$
        """)
        xn_text.set_color(GREEN)
        xn_text.move_to([3.5, 3, 0])
        self.play(Write(xn_text))
        self.wait(1)

        # drawing h:

        th = np.array(range(-2, 2, 1))
        yh = 2 * np.cos(th)

        gh1 = VGroup()
        gh2 = VGroup()

        # creating lines
        for i in range(len(th)):
            lh1 = Line([th[i] / 2, 0, 0], [th[i] / 2, yh[i] / 2, 0])
            lh1.set_color(BLUE)
            gh1.add(lh1)

            lh2 = Line([-th[i] / 2, 0, 0], [-th[i] / 2, yh[i] / 2, 0])
            lh2.set_color(BLUE)
            gh2.add(lh2)

        # creating dots
        for i in range(len(th)):
            dh1 = Dot([th[i] / 2, yh[i] / 2, 0])
            dh1.set_color(BLUE)
            gh1.add(dh1)
            dh2 = Dot([-th[i] / 2, yh[i] / 2, 0])
            dh2.set_color(BLUE)
            gh2.add(dh2)

        # drawing h[n]
        gh1.shift([0, y0, 0])
        self.play(Write(gh1))
        self.wait(1)

        hn_text = TextMobject("""
            $$h[n]$$
        """)
        hn_text.set_color(BLUE)
        hn_text.move_to([3.5, 2.3, 0])
        self.play(Write(hn_text))
        self.wait(1)

        # removing convolution text and putting the formula in a corner
        corner_conv_formula = TextMobject(
            "{\\small $y[n]=$}", 
            "{\\small $\sum\limits_{k=-\infty}^{+\infty}x[k]h[n-k]$}"
        )
        corner_conv_formula.move_to([-3.5, 3, 0])
        corner_conv_formula.scale(0.8)
        self.play(
            FadeOut(conv_text),
            FadeOut(conv_formula[1]),
            ReplacementTransform(conv_formula[0], corner_conv_formula[0]),
            ReplacementTransform(conv_formula[2], corner_conv_formula[1])
        )
        self.wait(1)

        # drawing convolution rect
        convolution_rect = Polygon([-5.5, 2.55, 0], [-1.5, 2.55, 0],
                                   [-1.5, 3.4, 0], [-5.5, 3.4, 0])
        convolution_rect.set_color(WHITE)
        convolution_rect.scale(1.1)
        self.play(Write(convolution_rect))
        self.wait(1)

        # step 1: n -> k
        n_to_k = TextMobject("""$$Step \\ 1: \\; n \\rightarrow k$$""")
        n_to_k.scale(0.9)
        n_to_k.move_to([-3.5, 2.1, 0])
        self.play(Write(n_to_k))
        self.wait(1.5)

        xk_text = TextMobject("""
            $$x[k]$$
        """)
        xk_text.set_color(GREEN)
        xk_text.move_to([3.5, 3, 0])

        hk_text = TextMobject("""
            $$h[k]$$
        """)
        hk_text.set_color(BLUE)
        hk_text.move_to([3.5, 2.3, 0])

        label_k = TextMobject(" k ")
        label_k.move_to([6.5, 0.4 + y0, 0])
        label_k.set_color(RED)

        self.play(
            Transform(xn_text, xk_text),
            ReplacementTransform(hn_text, hk_text),
            ReplacementTransform(label_n, label_k),
            run_time=1.5
        )
        self.wait(1)

        # step 2: h[k] -> h[-k]
        self.play(FadeOut(n_to_k))

        hk_to_hmk = TextMobject("""$Step \\ 2: \\; h[k] \\rightarrow h[-k]$""")
        hk_to_hmk.scale(0.9)
        hk_to_hmk.move_to([-3.5, 2.1, 0])
        self.play(Write(hk_to_hmk))
        self.wait(1)

        hmk_text = TextMobject("""
            $$h[-k]$$
        """)
        hmk_text.set_color(BLUE)
        hmk_text.move_to([3.5, 2.3, 0])

        # drawing h[-k]
        gh2.shift([0, y0, 0])
        self.play(Transform(gh1, gh2), ReplacementTransform(hk_text, hmk_text))
        self.wait(1)

        # step 3: moving window and multiply
        self.play(FadeOut(hk_to_hmk))

        wind_and_multiply = TextMobject("Step 3 \\ : Sliding Window")
        wind_and_multiply.scale(0.9)
        wind_and_multiply.move_to([-3.5, 2.1, 0])
        self.play(Write(wind_and_multiply))
        self.wait(1)

        # writing h[n - k]
        h_nmk = TextMobject("{\\footnotesize$h[n -k]$}")
        h_nmk.set_color(BLUE)
        h_nmk.move_to([3.5, 2.3, 0])

        # moving h[-k] to left
        offset = (-2 + tx[0] + th[0]) / 2
        self.remove(gh1)
        self.play(gh2.shift, [offset, 0, 0], ReplacementTransform(hmk_text, h_nmk), run_time=2)
        self.wait(1)

        # drawing window
        tw_min = -th[len(th) - 1]
        tw_max = -th[0]
        yw_min = min(*yx, *yh)
        yw_max = max(*yx, *yh)

        window_rect = Polygon([tw_min / 2 - 1 / 4, yw_min / 2 - 1 / 4, 0], [tw_max / 2 + 1 / 4, yw_min / 2 - 1 / 4, 0],
                              [tw_max / 2 + 1 / 4, yw_max / 2 + 1 / 4, 1], [tw_min / 2 - 1 / 4, yw_max / 2 + 1 / 4, 0])
        window_rect.set_color(YELLOW)
        window_rect.shift([offset, y0, 0])
        self.play(Write(window_rect))
        self.wait(1)

        y_text = TextMobject("y[n]")
        y_text.set_color(YELLOW)
        y_text.scale(0.8)
        y_text.move_to([-6, -2.75, 0])
        self.play(Write(y_text))
        self.wait(1)

        # writing h[%d - k]
        h_dmk = TextMobject("{\\footnotesize$h[ %d -k]$}" % (2 * offset))
        h_dmk.set_color(BLUE)
        h_dmk.move_to([3.5, 2.3, 0])

        # n counter
        n_counter = TextMobject("{n = \\footnotesize$ %d $}" % (2 * offset))
        n_counter.move_to([offset + (tw_min + tw_max) / 4, yw_max / 2 + 1 / 2 + 0.05 + y0, 0])
        n_counter.set_color(YELLOW)
        n_counter.scale(0.9)
        self.play(Write(n_counter), ReplacementTransform(h_nmk, h_dmk))
        self.wait(1)

        # grouping the window and h[n - k]
        window = VGroup(gh2, window_rect)

        # adding extra 0 entries to x[k]
        extra_zeros = [0 for i in range(1 + tw_max - tw_min)]
        yx = np.array(extra_zeros + list(yx) + extra_zeros + [0])

        offset = (-2 + tx[0] + th[0]) / 2
        right_offset = (2 + tx[len(tx) - 1] + th[len(th) - 1]) / 2


        # result of convolution
        res = [0.0]

        # result texts
        res_texts = []

        # showing the first 0.00
        partial_mul = TextMobject('0.00')
        partial_mul.move_to([offset, -2.75, 0])
        partial_mul.scale(0.75)
        partial_mul.rotate(-PI / 2)
        partial_mul.set_color(YELLOW)
        self.play(Write(partial_mul))
        res_texts.append(partial_mul)

        for i in range(1, int(2 * (right_offset - offset)) + 1):
            next_h_nmk = TextMobject("{\\footnotesize$h[ %d -k]$}" % (2 * offset + i))
            next_h_nmk.set_color(BLUE)
            next_h_nmk.move_to([3.5, 2.3, 0])
            next_n_counter = TextMobject("{n = \\footnotesize$%d$}" % (2 * offset + i))
            next_n_counter.move_to([offset + (tw_min + tw_max) / 4 + 0.5 * i, yw_max / 2 + 1 / 2 + 0.05 + y0, 0])
            next_n_counter.set_color(YELLOW)
            next_n_counter.scale(0.9)
            self.play(
                window.shift, [0.5, 0, 0],
                Transform(h_dmk, next_h_nmk),
                Transform(n_counter, next_n_counter),
                run_time=0.5
            )
            self.wait(0.5)


            if 1 < i < 6:

                # zooming camera
                self.camera_frame.save_state()
                location = [gh2.get_x(), gh2.get_y() - 1/12, 0] 
                self.play(
                    self.camera_frame.set_width, window.get_width() * 2.75,
                    self.camera_frame.move_to, location
                )
                self.wait(1)

            # doing the partial convolution
            sum = 0
            th_start = 1  # th start index
            tx_start = 0  # tx start index

            # testing
            h_terms = VGroup()
            mul_symbols = VGroup()
            x_terms = VGroup()

            for j in range(len(th)):
                # calculate partial multiple
                partial_mul_value = yh[len(th) - j - 1] * yx[i + tw_min + j]
                sum += partial_mul_value

                if 1 < i < 6:
                    # write partial multiple
                    h_term = TextMobject('{:.2f}'.format(yh[len(th) - j - 1]))
                    mul_symbol = TextMobject('×')
                    x_term = TextMobject('{:.2f}'.format(yx[i + tw_min + j]))

                    h_term.move_to([offset + tw_min / 2 + i / 2 - 1 / 2 + 1 / 2 + j / 2, yw_min / 2 + 1 / 6 + 1 / 5, 0])
                    h_term.scale(0.25)
                    h_term.shift([0, y0, 0])
                    h_term.set_color(BLUE)

                    mul_symbol.move_to([offset + tw_min / 2 + i / 2 - 1 / 2 + 1 / 2 + j / 2, yw_min / 2 + 1 / 12 + 1 / 5, 0])
                    mul_symbol.shift([0, y0, 0])
                    mul_symbol.scale(0.25)

                    x_term.move_to([offset + tw_min / 2 + i / 2 - 1 / 2 + 1 / 2 + j / 2, yw_min / 2 + 1 / 5, 0])
                    x_term.shift([0, y0, 0])
                    x_term.scale(0.25)
                    x_term.set_color(GREEN)

                    self.play(Write(h_term), Write(mul_symbol), Write(x_term))
                    self.wait(0.25)
                    h_terms.add(h_term)
                    mul_symbols.add(mul_symbol)
                    x_terms.add(x_term)

                    th_term = th_start + 2 * offset + i - 1 + tw_min
                    tx_term = tx[tx_start]

                    if (th_term == tx_term):
                        th_start = th_start + 1
                        tx_start = tx_start + 1

                    elif (th_term < tx_term):
                        th_start = th_start + 1

                    else:
                        tx_start = tx_start + 1

                    self.wait(0.5)


            
            res.append(sum)

            if 1 < i < 6:

                plus_symbols = VGroup()
                for j in range(len(th) - 1):
                    plus_symbol = TextMobject('+')
                    plus_symbol.move_to([offset + tw_min/2 + i/2 + j/2 + 1/4, yw_min/2 + 1/12 + 1/5, 0])
                    plus_symbol.scale(0.35)
                    plus_symbols.add(plus_symbol)
                
                plus_symbols.shift([0, y0, 0])
                self.play(Write(plus_symbols))
                self.wait(0.5)

                calculations = VGroup(h_terms, mul_symbols, x_terms, plus_symbols)

                sum_term = TextMobject('{:.2f}'.format(sum))
                sum_term.move_to([offset + tw_min/2 + i/2 + float(len(th))/4 - 1/4, yw_min/2, 0])
                sum_term.shift([0, y0, 0])
                sum_term.scale(0.4)
                sum_term.set_color(YELLOW)


                self.play(ReplacementTransform(calculations, sum_term))
                self.wait(0.5)

                # Restore the state saved
                self.play(
                    Restore(self.camera_frame),
                    sum_term.scale, 15/8,
                )

                self.wait(0.5)

                partial_mul = TextMobject('{:.2f}'.format(sum))
                partial_mul.move_to([offset + i / 2, -2.75, 0])
                partial_mul.scale(0.75)
                partial_mul.rotate(-PI / 2)
                partial_mul.set_color(YELLOW)
                self.play(ReplacementTransform(sum_term, partial_mul))
                res_texts.append(partial_mul)


            else: 

                partial_mul = TextMobject('{:.2f}'.format(sum))
                partial_mul.move_to([offset + i / 2, -2.75, 0])
                partial_mul.scale(0.75)
                partial_mul.rotate(-PI / 2)
                partial_mul.set_color(YELLOW)
                self.play(FadeInFrom(partial_mul, UP))
                res_texts.append(partial_mul)

                self.wait(0.5)

        self.wait(1)

        # back to n!
        new_label_n = TextMobject(" n ")
        new_label_n.move_to([6.5, 0.4, 0])
        new_label_n.set_color(YELLOW)

        # removing stuff
        self.play()
        self.play(FadeOut(window), FadeOut(gx1), FadeOut(next_h_nmk), FadeOut(h_dmk),
        FadeOut(xk_text),FadeOut(xn_text), FadeOut(next_n_counter), FadeOut(n_counter))
        self.play(FadeOut(wind_and_multiply), FadeOut(corner_conv_formula), FadeOut(convolution_rect))


        self.play(
            y_text.shift, [0, 3.15, 0],
            x_axis.shift, [0, -y0, 0],
            ReplacementTransform(label_k, new_label_n)
        )

        # draw the result signal
        t_res = range(int(2 * offset), int(2 * right_offset) + 1)

        for i in range(len(t_res)):
            l_res = Line([t_res[i] / 2, 0, 0], [t_res[i] / 2, res[i] / 2, 0])
            l_res.set_color(YELLOW)
            self.play(Transform(res_texts[i], l_res))
            d_res = Dot([t_res[i] / 2, res[i] / 2, 0])
            d_res.set_color(YELLOW)
            self.play(Write(d_res, run_time=0.05))
        self.wait(3)

