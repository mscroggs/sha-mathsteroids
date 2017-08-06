import ugfx
import time
from math import sin,cos,floor,pi
try:
    import deepsleep
except ImportError:
    pass

SCREEN_Y = 126
SCREEN_X = 295
SPEED = 10
ROTATION = pi/8
FRAMERATE = 0.2


class DONE(BaseException):
    pass

class Game:
    def __init__(self):


        self.surface = 0

        self.options = ["4D flat torus","flat Klein bottle"]

        self.x = 30
        self.y = 30
        self.r = 0

        ugfx.init()
        ugfx.input_init()

        self.select_surface()

        self.main_loop()


    def main_loop(self):
        ugfx.input_attach(ugfx.JOY_LEFT, self.take)
        ugfx.input_attach(ugfx.JOY_RIGHT, self.add)
        ugfx.input_attach(ugfx.BTN_START, self.exit)
        ugfx.input_attach(ugfx.BTN_A, self.exit)
        ugfx.input_attach(ugfx.BTN_B, self.exit)

        while True:
            self.x += SPEED*cos(self.r)
            self.y += SPEED*sin(self.r)

            self.wrap()

            self.draw_ship()
            time.sleep(FRAMERATE)


    def exit(self, press):
        if press:
            deepsleep.reboot()

    def draw_line(self, x1, y1, x2, y2):
        x1_ = self.x+(x1-self.x)*cos(self.r) - (y1-self.y)*sin(self.r)
        y1_ = self.y+(y1-self.y)*cos(self.r) + (x1-self.x)*sin(self.r)
        x2_ = self.x+(x2-self.x)*cos(self.r) - (y2-self.y)*sin(self.r)
        y2_ = self.y+(y2-self.y)*cos(self.r) + (x2-self.x)*sin(self.r)

        line = Line(x1_, y1_, x2_, y2_)

        while line.goes_out():
            line.split()

        line.draw()

    def draw_ship(self):
        ugfx.clear(ugfx.WHITE)

        ugfx.string(10, SCREEN_Y-15, "You are playing on a "+self.options[self.surface],
                        "RobotoRegular12", ugfx.BLACK)

        self.draw_line(self.x+4, self.y, self.x-6, self.y-5)
        self.draw_line(self.x+4, self.y, self.x-6, self.y+5)
        self.draw_line(self.x-3, self.y, self.x-6, self.y-5)
        self.draw_line(self.x-3, self.y, self.x-6, self.y+5)

        ugfx.flush()


    def add(self, press):
        if press:
            self.r += ROTATION

    def take(self, press):
        if press:
            self.r -= ROTATION

    def return_(self, press):
        if press:
            self.do_return = True

    def next(self, press):
        if press:
            self.surface += 1
            self.surface %= len(self.options)
            self.show_choice()

    def prev(self, press):
        if press:
            self.surface -= 1
            self.surface %= len(self.options)
            self.show_choice()

    def pass_(self, press):
        pass

    def show_choice(self):
        ugfx.clear(ugfx.WHITE)
        ugfx.string(10, 10, self.options[self.surface], "PermanentMarker22", ugfx.BLACK)
        ugfx.string(10, 40, "Press up/down to choose a surface.", "Roboto_Regular12", ugfx.BLACK)
        ugfx.string(10, 55, "Press A/B/START to begin.", "Roboto_Regular12", ugfx.BLACK)
        ugfx.flush()

    def select_surface(self):
        ugfx.input_attach(ugfx.JOY_UP, self.next)
        ugfx.input_attach(ugfx.JOY_DOWN, self.prev)
        ugfx.input_attach(ugfx.BTN_START, self.return_)
        ugfx.input_attach(ugfx.BTN_A, self.return_)
        ugfx.input_attach(ugfx.BTN_B, self.return_)
        self.show_choice()
        self.do_return = False
        while not self.do_return:
            pass
        ugfx.input_attach(ugfx.JOY_UP, self.pass_)
        ugfx.input_attach(ugfx.JOY_DOWN, self.pass_)
        ugfx.input_attach(ugfx.BTN_START, self.pass_)
        ugfx.input_attach(ugfx.BTN_A, self.pass_)
        ugfx.input_attach(ugfx.BTN_B, self.pass_)

    def wrap(self):
        if self.surface == 0: # 4D flat torus
            if self.y < 0:
                self.y += SCREEN_Y
            if self.y > SCREEN_Y:
                self.y -= SCREEN_Y
            if self.x < 0:
                self.x += SCREEN_X
            if self.x > SCREEN_X:
                self.x -= SCREEN_X

        if self.surface == 1: # ?D flat Klein bottle
            if self.y < 0:
                self.y += SCREEN_Y
                self.x = SCREEN_X - self.x
                self.r = pi - self.r
            if self.y > SCREEN_Y:
                self.y -= SCREEN_Y
                self.x = SCREEN_X - self.x
                self.r = pi - self.r
            if self.x < 0:
                self.x += SCREEN_X
            if self.x > SCREEN_X:
                self.x -= SCREEN_X



class Line:
    def __init__(self, x1, y1, x2, y2):
        self.segments = [LineSegment(x1,y1, x2,y2)]
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def split(self):
        for i,segment in enumerate(self.segments):
            if segment.goes_out():
                s1,s2 = segment.split()
                self.segments = self.segments[:i] + [s1,s2] + self.segments[i+1:]
                return

    def goes_out(self):
        for segment in self.segments:
            if segment.goes_out():
                return True
        return False

    def draw(self):
        for segment in self.segments:
            segment.draw()


class LineSegment:
    def __init__(self, x1, y1, x2, y2):
        if x1 < 0 and x2 < 0:
            x1 += SCREEN_X
            x2 += SCREEN_X
        if x1 > SCREEN_X and x2 > SCREEN_X:
            x1 -= SCREEN_X
            x2 -= SCREEN_X
        if y1 < 0 and y2 < 0:
            y1 += SCREEN_Y
            y2 += SCREEN_Y
        if y1 > SCREEN_Y and y2 > SCREEN_Y:
            y1 -= SCREEN_Y
            y2 -= SCREEN_Y


        self.start = (x1,y1)
        self.end = (x2,y2)



    def draw(self):
        ugfx.line(int(floor(self.start[0])),
                  int(floor(self.start[1])),
                  int(floor(self.end[0])),
                  int(floor(self.end[1])),ugfx.BLACK)

    def min_x(self):
        return min(self.start[0],self.end[0])

    def max_x(self):
        return max(self.start[0],self.end[0])

    def min_y(self):
        return min(self.start[1],self.end[1])

    def max_y(self):
        return max(self.start[1],self.end[1])

    def split(self):
        for a,b in [(self.start,self.end),(self.end,self.start)]:
            if a[0] < 0:
                y = a[1] + (b[1]-a[1])*a[0]/(a[0]-b[0])
                return (LineSegment(a[0]+SCREEN_X,a[1],SCREEN_X,y),
                        LineSegment(0,y,b[0],b[1]))
            if a[0] > SCREEN_X:
                y = a[1] + (b[1]-a[1])*(a[0]-SCREEN_X)/(a[0]-b[0])
                return (LineSegment(a[0]-SCREEN_X,a[1],0,y),
                        LineSegment(SCREEN_X,y,b[0],b[1]))

            if a[1] < 0:
                x = a[0] + (b[0]-a[0])*a[1]/(a[1]-b[1])
                return (LineSegment(a[0],a[1]+SCREEN_Y,x,SCREEN_Y),
                        LineSegment(x,0,b[0],b[1]))
            if a[1] > SCREEN_Y:
                x = a[0] + (b[0]-a[0])*(a[1]-SCREEN_Y)/(a[1]-b[1])
                return (LineSegment(a[0],a[1]-SCREEN_Y,x,0),
                        LineSegment(x,SCREEN_Y,b[0],b[1]))

    def goes_out(self):
        if self.start[0] < 0 or self.start[0] > SCREEN_X:
            return True
        if self.start[1] < 0 or self.start[1] > SCREEN_Y:
            return True
        if self.end[0] < 0 or self.end[0] > SCREEN_X:
            return True
        if self.end[1] < 0 or self.end[1] > SCREEN_Y:
            return True
