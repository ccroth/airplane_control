import turtle
import math
import tkinter as tk

# so we can work with degrees exclusively
def sin(degrees):
    return math.sin((degrees/360)*2*math.pi)

def cos(degrees):
    return math.cos((degrees/360)*2*math.pi)

# origin
x = 0
y = 0

# screen
screen = turtle.Screen()
screen.setworldcoordinates(x-300, y-300, x+300, y+300)
screen.title("2D Airplane Trajectory")
screen.bgcolor(0.85,0.85,0.85)

# airplane characteristics + initialization
plane = turtle.Turtle()
plane.pen(pencolor=(0.85,0.85,0.85), fillcolor=(0.85,0.85,0.85), pensize=2, speed=10)
plane.rt(270)
plane.shapesize(1,2,2)
plane.pen(pencolor="blue", fillcolor="white", pensize=2)

# this dictionary is updated everytime a turn is initiated and completed
# the assumption is our pilot can only do one turn at a time (he is still an amateur)
next_turn = {"yaw": 0, "completed": True}

# make the airplane fly
def flight():
    v = airspeed_scale.get()
    x = plane.xcor()
    y = plane.ycor()
    if v != 0:
        launch_button["state"] = "disabled"
        launch_button["text"] = "Flight in progress"
        plane.pen(speed=v/550)
        if next_turn["completed"] == False:
            turn_button["state"] = "disabled"
            turn_button["text"] = "Turn in progress"
            airspeed_scale["state"] = "disabled"
            # turning right relative to direction of travel
            if next_turn["yaw"] >= 0:
                for i in range(1,next_turn["yaw"]+1):
                    new_direction = plane.heading() - 1
                    absolute_yaw = 90 - new_direction
                    x = x + (10*v/550)*sin(absolute_yaw)
                    y = y + (10*v/550)*cos(absolute_yaw)
                    plane.setheading(new_direction)
                    plane.goto(x, y)
                    screen.setworldcoordinates(x-300, y-300, x+300, y+300)
                    plane.shapesize(1,2,2)
                    plane.pen(pencolor="blue", fillcolor="white", pensize=2)
            # turning left relative to direction of travel
            if next_turn["yaw"] < 0:
                for i in range(1, -next_turn["yaw"]+1):
                    new_direction = plane.heading() + 1
                    absolute_yaw = 90 - new_direction
                    x = x + (10*v/550)*sin(absolute_yaw)
                    y = y + (10*v/550)*cos(absolute_yaw)
                    plane.setheading(new_direction)
                    plane.goto(x, y)
                    screen.setworldcoordinates(x-300, y-300, x+300, y+300)
                    plane.shapesize(1,2,2)
                    plane.pen(pencolor="blue", fillcolor="white", pensize=2)
            next_turn["completed"] = True
            turn_button["state"] = "normal"
            turn_button["text"] = "Initiate turn"
            airspeed_scale["state"] = "normal"
        else:
            new_direction = plane.heading()
            absolute_yaw = 90 - new_direction
            x = x + (10*v/550)*sin(absolute_yaw)
            y = y + (10*v/550)*cos(absolute_yaw)
            plane.setheading(new_direction)
            plane.goto(x, y)
            screen.setworldcoordinates(x-300, y-300, x+300, y+300)
            plane.shapesize(1,2,2)
            plane.pen(pencolor="blue", fillcolor="white", pensize=2)
        return flight()
    # flight has stopped
    else:
        launch_button["state"] = "normal"
        launch_button["text"] = "Relaunch flight"
        print("Plane has landed. Relaunch to resume flight.")
        return

def change_direction():
    next_turn["yaw"] = yaw_scale.get()
    next_turn["completed"] = False
    #print(f'Queued plane to turn {next_turn["yaw"]} degrees relative to direction of travel.')
    return

# user interface
canvas = turtle.getcanvas()
root = canvas.master
# label
main_label = tk.Label(root, text="Flight Settings", font=("Arial", 16, "bold"),padx=30)
main_label.pack(side="left")
# exit button
exit_button = tk.Button(root, text="Exit", height=2, command=root.destroy)
exit_button.pack(padx=30,side="right")
# air speed slider
airspeed_scale = tk.Scale(root, from_=0, to=550, orient=tk.HORIZONTAL, length=200, label="Airspeed (knots)")
airspeed_scale.pack(padx=20, pady=10, side="left")
# yaw slider
yaw_scale = tk.Scale(root, from_=-90, to=90, orient=tk.HORIZONTAL, length=120, label="Yaw (degrees)")
yaw_scale.pack(padx=20, pady=10, side="left")
# launch button
launch_button = tk.Button(root, text="Launch flight", height=2, command=flight)
launch_button.pack(pady=10, side="top")
# turn button
turn_button = tk.Button(root, text="Initiate turn", height=2, command=change_direction)
turn_button.pack(pady=10, side="top")

# main
screen.mainloop()