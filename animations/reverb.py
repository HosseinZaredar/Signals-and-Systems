from manim import *
from scipy.signal import chirp

class SineMove(GraphScene, MovingCameraScene):

    CONFIG = {
        "y_max" : 20,
        "y_min" : -20,
        "x_max" : 19,
        "x_min" : -1,
        "y_tick_frequency" : 1,
        "x_tick_frequency" : 1,
        "graph_origin" : [-6, 0, 0],
        "y_axis_label": None,
        "x_axis_label": None,
        "x_axis_width": 20,
        "y_axis_height": 40,
    }

    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):

        self.play(self.camera_frame.scale, 1.2)
        self.camera_frame.save_state()
        
        self.setup_axes()
        graph = self.get_graph(lambda t : chirp(t, f0=0.2, f1=20, t1=40, method='quadratic'), x_min=0, x_max=13.5)
        dot_at_start_graph = Dot().move_to(graph.points[0])
        dot_at_end_grap = Dot().move_to(graph.points[-1])
        self.add(graph, dot_at_end_grap, dot_at_start_graph)
        self.play(self.camera_frame.scale, 0.6, self.camera_frame.move_to, dot_at_start_graph)
        self.play(self.camera_frame.move_to, dot_at_end_grap, run_time=6)
        self.play(Restore(self.camera_frame))
        self.wait()


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

class ReverbGraph(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_max" : 20,
        "y_min" : 0,
        "y_max" : 20,
        "y_tick_frequency" : 1,
        "x_tick_frequency" : 1,
        "x_labeled_nums" : np.arange(0, 20, 1),
        "x_axis_label": r"t",
        "y_axis_label": None
    }

    def reverb(self, x):
        noise = random.choice([-6, 5, 0, 0, 0, 0])/x * np.random.normal(0, 1, 1)
        return np.abs(17 - x + noise)

    def construct(self):
        self.setup_axes()
        curve1 = self.get_graph(lambda x: 18, x_min=2, x_max=4)
        curve2 = self.get_graph(lambda x: 15, x_min=5, x_max=7)
        curve3 = self.get_graph(lambda x: 15 - (x-7)**2, x_min=7.001, x_max=8)
        curve4 = self.get_graph(self.reverb, x_min=9, x_max=17)
        line1 = self.get_vertical_line_to_graph(2, curve1, DashedLine, color=YELLOW)
        line2 = self.get_vertical_line_to_graph(4, curve1, DashedLine, color=YELLOW)
        line3 = self.get_vertical_line_to_graph(5, curve2, DashedLine, color=YELLOW)
        line4 = self.get_vertical_line_to_graph(8, curve3, DashedLine, color=YELLOW)
        line5 = self.get_vertical_line_to_graph(9, curve4, DashedLine, color=YELLOW)
        area1 = self.get_area(curve1, 2, 4, area_color=BLUE)
        area2 = self.get_area(curve2, 5, 7, area_color=GRAY)
        area3 = self.get_area(curve3, 7, 8, area_color=GRAY)
        area4 = self.get_area(curve4, 9, 17, area_color=GREEN, dx_scaling=0.01)
        loudness = PangoText("Loudness")
        loudness.next_to(self.y_axis, LEFT)
        loudness.shift(2.5 * UP)
        original_sound = PangoText("Original Sound")ی
        original_sound.next_to(area1, UP)
        original_sound.scale(0.5)
        early_reflections = PangoText("Early Reflections")
        early_reflections.next_to(area2, UP)
        early_reflections.shift(0.5 * RIGHT)
        early_reflections.scale(0.5)
        reverberation = PangoText("Reverberation")
        reverberation.next_to(area4, UP)
        reverberation.scale(0.5)
        self.add(
            curve1, curve2, curve3, curve4,
            line1, line2, line3, line4, line5,
            loudness, original_sound, early_reflections, reverberation
        )
        self.play(Write(area1))
        self.play(Write(VGroup(area2, area3)))
        self.play(Write(area4))
        self.wait()
    