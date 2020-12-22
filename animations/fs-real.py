from manimlib.imports import *


class FourierCirclesScene(ZoomedScene):
    CONFIG = {
        "n_vectors": 10,
        "big_radius": 2,
        "colors": [
            BLUE_D,
            BLUE_C,
            BLUE_E,
            GREY_BROWN,
        ],
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        },
        "circle_config": {
            "stroke_width": 1,
        },
        "base_frequency": 1,
        "slow_factor": 0.5,
        "center_point": ORIGIN,
        "parametric_function_step_size": 0.001,
        "drawn_path_color": YELLOW,
        "drawn_path_stroke_width": 2,
        "interpolate_config": [0, 1],
        # Zoom config
        "include_zoom_camera": False,
        "scale_zoom_camera_to_full_screen": False,
        "scale_zoom_camera_to_full_screen_at": 4,
        "zoom_factor": 0.3,
        "zoomed_display_height": 3,
        "zoomed_display_width": 4,
        "image_frame_stroke_width": 1,
        "zoomed_camera_config": {
            "default_frame_stroke_width": 3,
            "cairo_line_width_multiple": 0.05,
        },
        "zoom_position": lambda mob: mob.move_to(ORIGIN),
        "zoom_camera_to_full_screen_config": {
            "run_time": 3,
            "func": there_and_back_with_pause,
            "velocity_factor": 1
        },
        "wait_before_start": None
    }

    def setup(self):
        ZoomedScene.setup(self)
        self.slow_factor_tracker = ValueTracker(
            self.slow_factor
        )
        self.vector_clock = ValueTracker(0)
        self.add(self.vector_clock)
        self.prev = None


    def add_vector_clock(self):
        self.vector_clock.add_updater(
            lambda m, dt: m.increment_value(
                self.get_slow_factor() * dt
            )
        )

    def get_slow_factor(self):
        return self.slow_factor_tracker.get_value()

    def get_vector_time(self):
        return self.vector_clock.get_value()

    def get_freqs(self):
        n = self.n_vectors
        all_freqs = list(range(n // 2, -n // 2, -1))
        all_freqs.sort(key=abs)
        return all_freqs

    def get_coefficients(self):
        return [complex(0) for _ in range(self.n_vectors)]

    def get_color_iterator(self):
        return it.cycle(self.colors)

    def get_rotating_vectors(self, freqs=None, coefficients=None):
        vectors = VGroup()
        self.center_tracker = VectorizedPoint(self.center_point)

        if freqs is None:
            freqs = self.get_freqs()
        if coefficients is None:
            coefficients = self.get_coefficients()

        last_vector = None
        i = 0
        for freq, coefficient in zip(freqs, coefficients):
            if last_vector:
                center_func = last_vector.get_end
            else:
                center_func = self.center_tracker.get_location

            is_last = (i == len(freqs) - 1)
            vector = self.get_rotating_vector(
                coefficient=coefficient,
                freq=freq,
                center_func=center_func,
                is_last=is_last
            )

            vectors.add(vector)
            last_vector = vector
            i += 1

        return vectors

    def get_rotating_vector(self, coefficient, freq, center_func, is_last):
        vector = Vector(RIGHT, **self.vector_config)
        vector.scale(abs(coefficient))
        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=ORIGIN)
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func
        if is_last:
            vector.add_updater(self.last_vector_updater)
        else:
            vector.add_updater(self.update_vector)

        return vector

    def last_vector_updater(self, vector, dt):
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag + PI / 2

        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        point = Dot([1, 1, 0], radius=0.02)
        point.set_color(WHITE)
        vt = self.vector_clock.get_value()
        point.move_to([-6 + 6 *  (vt - 1), vector.get_end()[1], 0])
        self.add(point)

        if vt >=1:
            line = DashedLine(
                [-5.95 + 6 *  (vt - 1), vector.get_end()[1], 0],
                [self.center_point[0], vector.get_end()[1], 0]
            )
            line.set_color(ORANGE)
            if self.prev is not None:
                self.remove(self.prev)
            self.add(line)
            self.prev = line                            

        return vector

    def update_vector(self, vector, dt):
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag + PI / 2

        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())

        return vector

    def get_circles(self, vectors):
        return VGroup(*[
            self.get_circle(
                vector,
                color=color
            )
            for vector, color in zip(
                vectors,
                self.get_color_iterator()
            )
        ])

    def get_circle(self, vector, color=BLUE):
        circle = Circle(color=color, **self.circle_config)
        circle.center_func = vector.get_start
        circle.radius_func = vector.get_length
        circle.add_updater(self.update_circle)
        return circle

    def update_circle(self, circle):
        circle.set_width(2 * circle.radius_func())
        circle.move_to(circle.center_func())
        return circle

    def get_vector_sum_path(self, vectors, color=YELLOW):
        coefs = [v.coefficient for v in vectors]
        freqs = [v.freq for v in vectors]
        center = self.center_point

        path = ParametricFunction(
            lambda t: center + reduce(op.add, [
                complex_to_R3(
                    coef * np.exp(TAU * 1j * freq * t)
                )
                for coef, freq in zip(coefs, freqs)
            ]),
            t_min=0,
            t_max=1,
            color=color,
            step_size=self.parametric_function_step_size,
        )
        return path

    def get_drawn_path_alpha(self):
        return self.get_vector_time()

    def get_drawn_path(self, vectors, stroke_width=None, **kwargs):
        if stroke_width is None:
            stroke_width = self.drawn_path_stroke_width
        path = self.get_vector_sum_path(vectors, **kwargs)
        broken_path = CurvesAsSubmobjects(path)
        broken_path.curr_time = 0
        start, end = self.interpolate_config

        def update_path(path, dt):
            alpha = self.get_drawn_path_alpha()
            n_curves = len(path)
            for a, sp in zip(np.linspace(0, 1, n_curves), path):
                b = (alpha - a)
                if b < 0:
                    width = 0
                else:
                    width = stroke_width * interpolate(start, end, (1 - (b % 1)))
                sp.set_stroke(width=width)
            path.curr_time += dt
            return path

        broken_path.set_color(self.drawn_path_color)
        broken_path.add_updater(update_path)
        return broken_path

    def get_y_component_wave(self,
                             vectors,
                             left_x=1,
                             color=PINK,
                             n_copies=2,
                             right_shift_rate=5):
        path = self.get_vector_sum_path(vectors)
        wave = ParametricFunction(
            lambda t: op.add(
                right_shift_rate * t * LEFT,
                path.function(t)[1] * UP
            ),
            t_min=path.t_min,
            t_max=path.t_max,
            color=color,
        )
        wave_copies = VGroup(*[
            wave.copy()
            for x in range(n_copies)
        ])
        wave_copies.arrange(RIGHT, buff=0)
        top_point = wave_copies.get_top()
        wave.creation = ShowCreation(
            wave,
            run_time=(1 / self.get_slow_factor()),
            rate_func=linear,
        )
        cycle_animation(wave.creation)
        wave.add_updater(lambda m: m.shift(
            (m.get_left()[0] - left_x) * LEFT
        ))

        def update_wave_copies(wcs):
            index = int(
                wave.creation.total_time * self.get_slow_factor()
            )
            wcs[:index].match_style(wave)
            wcs[index:].set_stroke(width=0)
            wcs.next_to(wave, RIGHT, buff=0)
            wcs.align_to(top_point, UP)

        wave_copies.add_updater(update_wave_copies)

        return VGroup(wave, wave_copies)

    def get_wave_y_line(self, vectors, wave):
        return DashedLine(
            vectors[-1].get_end(),
            wave[0].get_end(),
            stroke_width=1,
            dash_length=DEFAULT_DASH_LENGTH * 0.5,
        )

    def get_coefficients_of_path(self, path, n_samples=100000, freqs=None):
        if freqs is None:
            freqs = self.get_freqs()
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([
            self.function(t)
            for t in ts
        ])
        complex_samples = [(s + 1j * 0) for s in samples] 

        return [
            np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt for freq in freqs
        ]

    def zoom_config(self):
        # This is not in the original version of the code.
        self.activate_zooming(animate=False)
        self.zoom_position(self.zoomed_display)
        self.zoomed_camera.frame.add_updater(lambda mob: mob.move_to(self.vectors[-1].get_end()))

    def scale_zoom_camera_to_full_screen_config(self):
        # This is not in the original version of the code.
        def fix_update(mob, dt, velocity_factor, dt_calculate):
            if dt == 0 and mob.counter == 0:
                rate = velocity_factor * dt_calculate
                mob.counter += 1
            else:
                rate = dt * velocity_factor
            if dt > 0:
                mob.counter = 0
            return rate

        fps = 1 / self.camera.frame_rate
        mob = self.zoomed_display
        mob.counter = 0
        velocity_factor = self.zoom_camera_to_full_screen_config["velocity_factor"]
        mob.start_time = 0
        run_time = self.zoom_camera_to_full_screen_config["run_time"]
        run_time *= 2
        mob_height = mob.get_height()
        mob_width = mob.get_width()
        mob_center = mob.get_center()
        ctx = self.zoomed_camera.cairo_line_width_multiple

        def update_camera(mob, dt):
            line = Line(
                mob_center,
                self.camera_frame.get_center()
            )
            mob.start_time += fix_update(mob, dt, velocity_factor, fps)
            if mob.start_time <= run_time:
                alpha = mob.start_time / run_time
                alpha_func = self.zoom_camera_to_full_screen_config["func"](alpha)
                coord = line.point_from_proportion(alpha_func)
                mob.set_height(
                    interpolate(
                        mob_height,
                        self.camera_frame.get_height(),
                        alpha_func
                    ),
                    stretch=True
                )
                mob.set_width(
                    interpolate(
                        mob_width,
                        self.camera_frame.get_width(),
                        alpha_func
                    ),
                    stretch=True
                )
                self.zoomed_camera.cairo_line_width_multiple = interpolate(
                    ctx,
                    self.camera.cairo_line_width_multiple,
                    alpha_func
                )
                mob.move_to(coord)
            return mob

        self.zoomed_display.add_updater(update_camera)


class AbstractFourierOfTexSymbol(FourierCirclesScene):
    CONFIG = {
        "n_vectors": 50,
        "slow_factor": 0.05,
        "n_cycles": None,
        "run_time": 10,
        "tex": r"\rm M",
        "start_drawn": True,
        "path_custom_position": lambda mob: mob,
        "max_circle_stroke_width": 1,
        "tex_class": TexMobject,
        "tex_config": {
            "fill_opacity": 0,
            "stroke_width": 1,
            "stroke_color": BLACK
        },
        "include_zoom_camera": False,
        "scale_zoom_camera_to_full_screen": False,
        "scale_zoom_camera_to_full_screen_at": 1,
        "zoom_position": lambda mob: mob.scale(0.8).move_to(ORIGIN).to_edge(RIGHT)
    }

    def construct(self):

        # # x and y axis

        x_axis = Arrow(
            [-7, 0, 0], [1.5, 0, 0],
            stroke_width=2,
            tip_length=0.15,
            max_stroke_width_to_length_ratio=10,
        )
        x_axis.set_color(RED)

        y_axis = Arrow(
            [-6, -3.7, 0], [-6, 3.7, 0],
            stroke_width=2,
            tip_length=0.15,
            max_stroke_width_to_length_ratio=10,
        )
        y_axis.set_color(RED)

        self.add(x_axis, y_axis)


        # This is not in the original version of the code.
        self.add_vectors_circles_path()
        if self.wait_before_start != None:
            self.wait(self.wait_before_start)
        self.add_vector_clock()
        self.add(self.vector_clock)
        if self.include_zoom_camera:
            self.zoom_config()
        if self.scale_zoom_camera_to_full_screen:
            self.run_time -= self.scale_zoom_camera_to_full_screen_at
            self.wait(self.scale_zoom_camera_to_full_screen_at)
            self.scale_zoom_camera_to_full_screen_config()
        if self.n_cycles != None:
            if not self.scale_zoom_camera_to_full_screen:
                for n in range(self.n_cycles):
                    self.run_one_cycle()
            else:
                cycle = 1 / self.slow_factor
                total_time = cycle * self.n_cycles
                total_time -= self.scale_zoom_camera_to_full_screen_at
                self.wait(total_time)
        elif self.run_time != None:
            self.wait(self.run_time)


    def add_vectors_circles_path(self):

        path = self.get_path()
        coefs = self.get_coefficients_of_path(path)
        vectors = self.get_rotating_vectors(coefficients=coefs)
        circles = self.get_circles(vectors)

        self.set_decreasing_stroke_widths(circles)
        drawn_path = self.get_drawn_path(vectors)

        if self.start_drawn:
            self.vector_clock.increment_value(1)

        # rotating
        vectors.rotate_about_origin(PI / 2)
        circles.rotate_about_origin(PI / 2)
        path.rotate_about_origin(PI / 2)
        drawn_path.shift([-self.center_point[0], -self.center_point[1], 0])
        drawn_path.rotate_about_origin(PI / 2)
        drawn_path.shift([self.center_point[0], self.center_point[1], 0])

        self.add(vectors)
        self.add(circles)
        self.add(drawn_path)

        self.vectors = vectors
        self.circles = circles
        self.path = path
        self.drawn_path = drawn_path

        # x and y axis
        # x_axis = Arrow(
        #     [-7, 0, 0], [1.5, 0, 0],
        #     stroke_width=2,
        #     tip_length=0.15,
        #     max_stroke_width_to_length_ratio=10,
        # )
        # x_axis.set_color(RED)

        # y_axis = Arrow(
        #     [-6, -3.7, 0], [-6, 3.7, 0],
        #     stroke_width=2,
        #     tip_length=0.15,
        #     max_stroke_width_to_length_ratio=10,
        # )
        # y_axis.set_color(RED)

        # self.play(GrowArrow(x_axis), GrowArrow(y_axis))

        # self.wait(0.5)


    def run_one_cycle(self):
        time = 1 / self.slow_factor
        self.wait(time)

    def set_decreasing_stroke_widths(self, circles):
        mcsw = self.max_circle_stroke_width
        for k, circle in zip(it.count(1), circles):
            circle.set_stroke(width=max(
                mcsw / k,
                mcsw,
            ))
        return circles

    def get_path(self):
        tex_mob = self.tex_class(self.tex, **self.tex_config)
        tex_mob.set_height(6)
        path = tex_mob.family_members_with_points()[0]
        return path


# Using TexMobject or TextMobject
class FourierOfTexSymbol(AbstractFourierOfTexSymbol):
    CONFIG = {
        # if start_draw = True the path start to draw
        "start_drawn": True,
        # Tex config
        "tex_class": TexMobject,
        "tex": r"\Sigma",
        "tex_config": {
            "fill_opacity": 0,
            "stroke_width": 1,
            "stroke_color": BLACK
        },
        # Draw config
        "drawn_path_color": YELLOW,
        "interpolate_config": [0, 1],
        "n_vectors": 50,
        "big_radius": 2,
        "drawn_path_stroke_width": 2,
        "slow_factor": 0.2,
        "n_cycles": None,
        "run_time": 10,
        # colors of circles
        "colors": [
            BLUE_D,
            BLUE_C,
            BLUE_E,
            GREY_BROWN,
        ],
        # circles config
        "circle_config": {
            "stroke_width": 1,
        },
        # vector config
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        },
        "base_frequency": 1,
        # definition of subpaths
        "parametric_function_step_size": 0.001,
    }


class Dash(FourierOfTexSymbol):
    CONFIG = {
        "n_vectors": 101,
        "slow_factor": 0.1,
        "run_time": 10,
        "tex_class": TexMobject,
        # "wait_before_start": 1.2,
        

        "function": lambda x: 2.5 * (x <= 0.5) + -2.5 * (x > 0.5),
        "center_point": [3.5, 0, 0],

        # "function": lambda x: 2 * np.sin(2 * PI * x) + np.cos(4 * PI * x),
        # "center_point": [4, 0, 0],

        # "function": lambda x: 5 * x * (x <= 0.5) + (5 - 5 * x) * (x > 0.5),
        # "center_point": [4, -2, 0],
    }
