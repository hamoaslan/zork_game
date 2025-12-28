import tkinter as tk
from PIL import Image, ImageTk
from math import cos, sin, atan, degrees, radians
from game_functions import submitText


class Compass(tk.Frame):
    def __init__(self, parent_root, master, size=200, width=3):
        super().__init__()

        self.master = master
        self.root = parent_root

        # size of the graphic and width of the needle
        self._size = size, size
        self._width = width

        # Values for graphic, diffs from logic angle, because of missing vector graphic
        self._EAST = 0
        self._NE = 46
        self._NORTH = 90
        self._NW = 133
        self._WEST = 180
        self._SW = 228
        self._SOUTH = 270
        self._SE = 311

        self._direction_dic = {
            '0': self.go_east,
            '1': self.go_ne,
            '2': self.go_north,
            '3': self.go_nw,
            '4': self.go_west,
            '5': self.go_sw,
            '6': self.go_south,
            '7': self.go_se,
            '8': self.go_east
        }

        self._directioncmd_dic = {
            'n': self.go_north,
            'north': self.go_north,
            'w': self.go_west,
            'west': self.go_west,
            's': self.go_south,
            'south': self.go_south,
            'e': self.go_east,
            'east': self.go_east,
            'ne': self.go_ne,
            'northeast': self.go_ne,
            'nw': self.go_nw,
            'northwest': self.go_nw,
            'se': self.go_se,
            'southeast': self.go_se,
            'sw': self.go_sw,
            'southwest': self.go_sw
        }

        self._compass_image = self.load_image()
        self.cv = self._create_canvas()
        self._current_state = tk.IntVar(value=91)
        self._draw()

        # start the animation to move the needle to 90 degrees
        self._update_needle(self._NORTH, self._current_state.get())
        self.cv.pack(side=tk.BOTTOM)

        self.cv.bind('<Button 1>', self.motion_dect)

    # --interaction functions-- #
    def go_north(self, w=False) -> None:
        if not w:
            self.master.compass_interact("north")
        self._update_needle(self._NORTH, self._current_state.get())
        self._current_state.set(self._NORTH)
        return None

    def go_east(self, w=False) -> None:
        if not w:
            self.master.compass_interact("east")
        self._update_needle(self._EAST, self._current_state.get())
        self._current_state.set(self._EAST)
        return None

    def go_south(self, w=False) -> None:
        if not w:
            self.master.compass_interact("south")
        self._update_needle(self._SOUTH, self._current_state.get())
        self._current_state.set(self._SOUTH)
        return None

    def go_west(self, w=False) -> None:
        if not w:
            self.master.compass_interact("west")
        self._update_needle(self._WEST, self._current_state.get())
        self._current_state.set(self._WEST)
        return None

    def go_ne(self, w=False) -> None:
        if not w:
            self.master.compass_interact("northeast")
        self._update_needle(self._NE, self._current_state.get())
        self._current_state.set(self._NE)
        return None

    def go_se(self, w=False) -> None:
        if not w:
            self.master.compass_interact("southeast")
        self._update_needle(self._SE, self._current_state.get())
        self._current_state.set(self._SE)
        return None

    def go_sw(self, w=False) -> None:
        if not w:
            self.master.compass_interact("southwest")
        self._update_needle(self._SW, self._current_state.get())
        self._current_state.set(self._SW)
        return None

    def go_nw(self, w=False) -> None:
        if not w:
            self.master.compass_interact("northwest")
        self._update_needle(self._NW, self._current_state.get())
        self._current_state.set(self._NW)
        return None

    # --end of interacting functions-- #

    def motion_dect(self, event) -> None:

        x_center = self._compass_image.width() // 2
        y_center = self._compass_image.height() // 2
        x, y = event.x, event.y
        y = self._compass_image.height() - y  # mirrors the y-axis to upwards

        # skips the divide by 0 case
        dx = (x - x_center)
        if dx == 0:
            dx = 1

        dy_dx = - (y - y_center) / dx
        angle_radians = atan(dy_dx)
        angle_degrees = degrees(angle_radians) * -1

        # print(x, y)

        # gets the angle and calls funktion from dict above
        if y >= x_center:
            if x >= x_center:
                pass
            else:
                angle_degrees += 180
        elif x >= x_center:
            angle_degrees = 360 + angle_degrees * 1
        else:
            angle_degrees = 180 + angle_degrees * 1

        angle_degrees = round(angle_degrees)

        self._direction_dic[str(round(angle_degrees / 45))]()

    # load compass image via PIL
    def load_image(self):
        image_path = "./images/compass.png"
        original_image = Image.open(image_path)
        original_image = original_image.resize(self._size)
        compass_image = ImageTk.PhotoImage(original_image)
        return compass_image

    # function to update the compass needle direction with animation
    def _update_needle(self, target_angle, current_angle) -> None:
        # condition to stop recursion
        if current_angle == target_angle or current_angle == target_angle + 360 or current_angle % 360 == target_angle:
            return None

        # determine the direction of rotation
        angle_diff = (current_angle - target_angle) % 360

        if angle_diff > 360 / 2:
            new_angle = current_angle + 1
        else:
            new_angle = current_angle - 1
        # print(current_angle, target_angle, angle_diff)

        # update the needle on canvas
        self._draw_needle(new_angle)

        self.root.after(2, self._update_needle, target_angle, new_angle)

        return None

    def _draw_needle(self, angle) -> None:
        self.cv.delete("needle")
        x_center = self._compass_image.width() // 2
        y_center = self._compass_image.height() // 2
        length = min(x_center, y_center) - 18  # length of the needle

        # calculate the end point of the needle
        x_end = x_center + length * cos(radians(angle))
        y_end = y_center - length * sin(radians(angle))

        # draw the needle
        self.cv.create_line(x_center, y_center, x_end, y_end, fill="red", width=self._width, tags="needle")
        return None

    # creates a Canvas to display the compass image
    def _create_canvas(self):
        cv = tk.Canvas(self.root, width=self._compass_image.width(), height=self._compass_image.height())
        return cv

    def _draw(self):
        # displays the compass image on the canvas
        self.cv.create_image(0, 0, image=self._compass_image, anchor=tk.NW)


if __name__ == "__main__":
    root = tk.Tk()
    compass = Compass(root)
    root.mainloop()
