import turtle
import time
import random
import pygame

delay = 0.1
is_playing = False

# initialize pygame
pygame.init()

# screen
wn = turtle.Screen()
wn.title("lil worm")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "Right"

# food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# snake body
segments = []

# text
controls_text = turtle.Turtle()
controls_text.speed(0)
controls_text.color("white")
controls_text.penup()
controls_text.hideturtle()
controls_text.goto(0, 260)
controls_text.write("Controls: W, A, S, D | Space to Play/Pause", align="center", font=("Courier", 12, "normal"))

# movement functions
def go_up():
    if head.direction != "Down":
        head.direction = "Up"


def go_down():
    if head.direction != "Up":
        head.direction = "Down"


def go_left():
    if head.direction != "Right":
        head.direction = "Left"


def go_right():
    if head.direction != "Left":
        head.direction = "Right"


def toggle_play_pause():
    global is_playing
    is_playing = not is_playing


def move():
    if head.direction == "Up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "Down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "Left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "Right":
        x = head.xcor()
        head.setx(x + 20)


# controls
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(toggle_play_pause, "space")


def display_explosion():
    explosion_sound = pygame.mixer.Sound("death.wav")
    explosion_sound.play()

    for _ in range(10):
        wn.update()
        time.sleep(0.1)

    time.sleep(0.5)

# main game loop
while True:
    wn.update()

    if not is_playing:
        controls_text.clear()
        controls_text.write("Controls: W, A, S, D | Space to Play/Pause", align="center", font=("Courier", 12, "normal"))
        continue  # escape loop if game is paused

    controls_text.clear()  # clear text each time the game is playing

    if (
            head.xcor() > 290
            or head.xcor() < -290
            or head.ycor() > 290
            or head.ycor() < -290
    ):
        display_explosion()
        head.goto(0, 0)
        head.direction = "Right"

        for segment in segments:
            segment.goto(1000, 1000)

        segments.clear()

        time.sleep(1)

    if head.distance(food) < 20:
        x = random.randint(-270, 270)
        y = random.randint(-270, 270)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # also check for self body collision
    for segment in segments:
        if head.distance(segment) < 20:
            display_explosion()
            head.goto(0, 0)
            head.direction = "Right"

            # hide
            for seg in segments:
                seg.goto(1000, 1000)

            # clear body segement
            segments.clear()

    time.sleep(delay)