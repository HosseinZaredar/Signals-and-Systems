from manimlib.imports import *


class PlotFourierSeries4(GraphScene):
    CONFIG = {
        "x_min": -3,
        "x_max": 3,
        "y_min": -1.5,
        "y_max": 1.5,
        "graph_origin": ORIGIN,
        "function_color": RED,
        "axes_color": RED,
        "x_axis_label": "$t$",
        "y_axis_label": "$x(t)$",
        "x_labeled_nums": range(-3, 4, 1),
        "colors": [
            PURPLE_B, BLUE, YELLOW, TEAL,
            PURPLE_B, BLUE, YELLOW, TEAL,
            PURPLE_B, BLUE, YELLOW, TEAL,
            PURPLE_B, BLUE, YELLOW, TEAL,
            PURPLE_B, BLUE, YELLOW, TEAL,
            PURPLE_B, BLUE, YELLOW, TEAL,
            PURPLE_B, BLUE, YELLOW, TEAL,
            PURPLE_B, BLUE, YELLOW, TEAL,
            PURPLE_B, BLUE, YELLOW, TEAL,
            PURPLE_B, BLUE, YELLOW, TEAL]
    }

    def construct(self):

        # Introduction
        title_l1 = TextMobject("CT Fourier Series")
        title_l2 = TextMobject("Complex Signals (Sinusoids) \\#1")
        title_l1.scale(1.8)
        title_l2.scale(1.25)
        title_l1.shift([0, 0.5, 0])
        title_l2.shift([0, -0.37, 0])
        line = Line([-4.6, 0, 0], [4.6, 0, 0])
        line.set_stroke(WHITE, 1.1, 1)
        creators = TextMobject("Made by Matin Tavakoli \& Hossein Zaredar")
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

        self.setup_axes(animate=True)

        start = -1
        end = 1
        step = 0.001
        k = 30

        plot4 = self.get_graph(self.func_to_graph_plot4)
        plot4.set_color(GREEN)
        self.play(ShowCreation(plot4), run_time=1.2)
        self.wait(1)
        x, f = self.create_func4(start, end, step)
        A0, A, B = self.find_func_coeffs(x, f, step, k)
        self.dc = A0 / 2

        self.cos_amp = 0
        self.cos_freq = 0
        self.cos_freqs = []
        self.sin_freqs = []

        self.cos_amps = A
        self.sin_amps = B

        old_counter = TextMobject("k = " + str(0))
        old_counter.set_color(BLUE)
        old_counter.move_to([3, 3, 0])

        self.play(plot1.set_opacity, 0.5, plot1.set_fill, GREEN, False)
        self.wait(0.7)

        dc_func_graph = self.get_graph(self.func_to_graph_line, YELLOW)
        self.play(ShowCreation(dc_func_graph), FadeIn(old_counter))
        self.wait(1)

        prev_sum_func_graph = dc_func_graph

        for i in range(k):

            if i < 7:
                speed = 0.9
            elif i < 12:
                speed = 0.7
            elif i < 20:
                speed = 0.5
            else:
                speed = 0.15

            counter = TextMobject("k = " + str(i + 1))
            counter.set_color(BLUE)
            counter.move_to([3, 3, 0])

            self.cos_amp = self.cos_amps[i]
            self.sin_amp = self.sin_amps[i]
            self.cos_freq = i + 1
            self.cos_freqs.append(i + 1)
            self.sin_freq = i + 1
            self.sin_freqs.append(i + 1)
            cos_func_graph = self.get_graph(self.func_to_graph_cos, self.colors[i])
            sin_func_graph = self.get_graph(self.func_to_graph_sin, self.colors[i])
            sum_func_graph = self.get_graph(self.func_to_graph_sum, self.colors[i])
            partial_sum_func_graph = self.get_graph(self.func_to_graph_partial_sum, self.colors[i])

            self.play(ReplacementTransform(old_counter, counter), run_time=speed)
            self.play(ShowCreation(cos_func_graph), run_time=speed)
            self.play(ShowCreation(sin_func_graph), run_time=speed)
            self.wait(0.5 * speed)
            self.play(ReplacementTransform(sin_func_graph, partial_sum_func_graph),
                      FadeOut(prev_sum_func_graph),
                      run_time=speed)
            self.wait(0.5 * speed)
            self.play(ReplacementTransform(cos_func_graph, sum_func_graph), FadeOut(partial_sum_func_graph),
                      run_time=speed)
            self.wait(1 * speed)
            prev_sum_func_graph = sum_func_graph
            old_counter = counter

        self.wait(1)

    def func_to_graph_line(self, x):
        return self.dc

    def func_to_graph_cos(self, x):
        return self.cos_amp * np.cos(self.cos_freq * x)

    def func_to_graph_sin(self, x):
        return self.sin_amp * np.sin(self.sin_freq * x)

    def func_to_graph_partial_sum(self, x):
        res = self.dc
        for i in range(len(self.cos_freqs)):
            if i != len(self.cos_freqs) - 1:
                res = res + self.cos_amps[i] * np.cos(self.cos_freqs[i] * x) + self.sin_amps[i] * np.sin(
                    self.sin_freqs[i] * x)
            else:
                res = res + self.sin_amps[i] * np.sin(self.sin_freqs[i] * x)
        return res

    def func_to_graph_sum(self, x):
        res = self.dc
        for i in range(len(self.cos_freqs)):
            res = res + self.cos_amps[i] * np.cos(self.cos_freqs[i] * x) + self.sin_amps[i] * np.sin(
                self.sin_freqs[i] * x)
        return res

    def func_to_graph_plot1(self, x):
        if x <= -2.01:
            return 0
        elif x <= -1.01:
            return x + 2
        elif x <= 0.99:
            return -x
        elif x <= 1.99:
            return x - 2
        else:
            return 0

    def func_to_graph_plot2(self, x):
        if x < 0:
            return 1
        elif x == 0:
            return 0
        elif x < 3:
            return -1
        else:
            return 1

    def func_to_graph_plot3(self, x):
        if x <= -1:
            return 0
        elif x <= 1:
            return 1
        else:
            return 0

    def func_to_graph_plot4(self, x):
        if x <= -2:
            return 1
        elif x <= -1:
            return -1.5
        elif x <= 0:
            return -1
        elif x <= 1:
            return -0.5
        elif x <= 2:
            return 0
        else:
            return 0.5

    def create_func1(self, start, end, step):
        x = np.pi * np.arange(start + step, end + step, step)
        n = len(x)
        partition = int(np.floor(n / 6))
        f = np.zeros_like(x)
        f[partition:2 * partition] = (6 / n) * np.arange(1, partition + 1)
        f[2 * partition:3 * partition] = np.ones(partition) - (6 / n) * np.arange(1, partition + 1)
        f[3 * partition:4 * partition] = -(6 / n) * np.arange(1, partition + 1)
        f[4 * partition:5 * partition] = -(np.ones(partition) - (6 / n) * np.arange(1, partition + 1))
        return x, f

    def create_func2(self, start, end, step):
        x = np.pi * np.arange(start + step, end + step, step)
        n = len(x)
        partition = int(np.floor(n / 6))
        f = np.ones_like(x)
        f[3 * partition:6 * partition] = -np.ones_like(partition)
        return x, f

    def create_func3(self, start, end, step):
        x = np.pi * np.arange(start + step, end + step, step)
        n = len(x)
        partition = int(np.floor(n / 6))
        f = np.ones_like(x)
        f[0:2 * partition] = 0
        f[4 * partition:] = 0
        return x, f

    def create_func4(self, start, end, step):
        x = np.pi * np.arange(start + step, end + step, step)
        n = len(x)
        partition = int(np.floor(n / 6))
        f = np.ones_like(x)
        f[0 * partition:1 * partition] = 1 * np.ones_like(partition)
        f[1 * partition:2 * partition] = -1.5 * np.ones_like(partition)
        f[2 * partition:3 * partition] = -1 * np.ones_like(partition)
        f[3 * partition:4 * partition] = -0.5 * np.ones_like(partition)
        f[4 * partition:5 * partition] = 0
        f[5 * partition:6 * partition] = 0.5 * np.ones_like(partition)
        return x, f

    def find_func_coeffs(self, x, f, step, k):
        A0 = np.sum(f * np.ones_like(x)) * step
        A = np.zeros(k)
        B = np.zeros(k)
        for i in range(k):
            A[i] = np.sum(f * np.cos((i + 1) * x)) * step
            B[i] = np.sum(f * np.sin((i + 1) * x)) * step

        return A0, A, B
