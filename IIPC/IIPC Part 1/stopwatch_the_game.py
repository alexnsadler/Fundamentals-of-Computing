# template for "Stopwatch: The Game"

import simplegui

# define global variables
counter = 0
stops_t = 0
stops_s = 0
stop = True


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    A = t // 600
    B = ((t // 10) % 60) / 10
    C = ((t // 10) % 60) % 10
    D = t % 10
    string = str(A) + ":" + str(B) + str(C) + "." + str(D)
    return string


# define event handlers for buttons; "Start", "Stop", "Reset"
def Start():
    global stop, counter
    stop = False
    timer.start()


def Stop():
    global stops_t, stops_s, stop
    if stop == False:
        if counter % 10 == 0 and counter != 0:
            stops_s += 1
            stops_t += 1
        elif counter != 0:
            stops_t += 1
    stop = True
    timer.stop()


def Reset():
    global counter, stops_t, stops_s
    counter = 0
    stop = True
    stops_t = 0
    stops_s = 0
    timer.stop()


# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    counter += 1


# define draw handler
def draw(canvas):
    canvas.draw_text(format(counter), (70, 100), 30, "white")
    canvas.draw_text(str(stops_s) + "/" + str(stops_t) , (160, 25), 30, "white")


# create frame
frame = simplegui.create_frame("Stopwatch Game", 200, 200)

# register event handlers
frame.add_button("Start", Start)
frame.add_button("Stop", Stop)
frame.add_button("Reset", Reset)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)

# start frame
frame.start()
