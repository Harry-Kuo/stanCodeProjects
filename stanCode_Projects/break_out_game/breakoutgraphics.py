"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

Name: Harry Kuo
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Height of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, lives=3,
                 title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(width=paddle_width, height=paddle_height, x=(window_width - paddle_width) / 2,
                            y=window_height - (paddle_offset + paddle_height))
        self.paddle.filled = True
        self.paddle.color = 'darkgrey'
        self.paddle.fill_color = 'darkgrey'
        self.window.add(self.paddle)

        # Center a filled ball in the graphical window
        self.ball = GOval(width=ball_radius*2, height=ball_radius*2, x=window_width / 2 - ball_radius,
                          y=window_height / 2 - ball_radius)
        self.ball.filled = True
        self.ball.color = 'royalblue'
        self.ball.fill_color = 'royalblue'
        self.window.add(self.ball)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Initialize our mouse listeners
        onmouseclicked(self.start_ball)
        self.mouse_disable = False                  # create a switch to disable mouse event
        self.lives = lives                          # to count the lives remained
        onmousemoved(self.move_paddle)

        # Draw bricks
        self.bricks_num = brick_cols * brick_rows   # to count the total bricks remained
        color = ''
        for j in range(brick_rows):
            for i in range(brick_cols):
                self.brick = GRect(width=brick_width, height=brick_height)
                self.brick.filled = True
                if j <= 1:
                    color = 'salmon'
                elif 1 < j <= 3:
                    color = 'gold'
                elif 3 < j <= 5:
                    color = 'lightsage'
                elif 5 < j <= 7:
                    color = 'lightskyblue'
                elif 7 < j <= 9:
                    color = 'mediumpurple'
                self.brick.color = color
                self.brick.fill_color = color
                self.window.add(self.brick, x=i * (brick_width + brick_spacing),
                                y=brick_offset + j * (brick_height + brick_spacing))

        # Set up lives label
        self.lives_label = GLabel('Lives: ' + str(self.lives))
        self.lives_label.font = '-25'
        self.window.add(self.lives_label, x=0, y=self.lives_label.height)

    def set_lives(self, new_lives):            # enable user to change the round limit
        self.lives = new_lives
        self.lives_label.text = 'Lives: ' + str(self.lives)

    def move_paddle(self, event):              # trace the mouse position and move paddle
        self.paddle.x = event.x - self.paddle.width / 2
        if self.paddle.x + self.paddle.width >= self.window.width:
            self.paddle.x = self.window.width - self.paddle.width
        if self.paddle.x <= 0:
            self.paddle.x = 0

    def set_ball_velocity(self):               # to set up initial velocity by random
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx
        self.__dy = INITIAL_Y_SPEED

    def move_ball(self):                       # to move the ball by private ivar
        self.ball.move(self.__dx, self.__dy)

    def handle_wall_collisions(self):          # make the ball bounce when it hits the boundary of window
        if self.ball.x <= 0 or self.ball.x + self.ball.width >= self.window.width:
            self.__dx = -self.__dx
        if self.ball.y <= 0:
            self.__dy = -self.__dy
        if self.ball.y + self.ball.height > self.window.height:
            self.lives -= 1                    # to count the lives remained when paddle cannot hit the ball
            self.reset_ball()
            self.lives_label.text = 'Lives: '+str(self.lives)

    def start_ball(self, event):               # mouse-clicked event to trick the game
        if not self.mouse_disable and self.lives > 0 and self.bricks_num > 0:
            self.mouse_disable = True
            self.set_ball_velocity()
            self.move_ball()

    def check_for_collisions(self):            # to determine the objects that was hit by ball
        for i in range(0, 2):
            for j in range(0, 2):              # to loop over the four corners of the ball
                obj_x = self.ball.x + i * self.ball.width
                obj_y = self.ball.y + j * self.ball.width
                maybe_obj = self.window.get_object_at(obj_x, obj_y)
                if maybe_obj is not None and maybe_obj is not self.paddle and maybe_obj is not self.lives_label:
                    self.__dy = -self.__dy     # the conditions that the ball hits the bricks
                    self.move_ball()
                    self.window.remove(maybe_obj)
                    self.bricks_num -= 1
                    if self.bricks_num == 0:
                        self.reset_ball()
                elif maybe_obj is not None and maybe_obj.y == self.paddle.y and maybe_obj is not self.lives_label:
                    self.__dy = -self.__dy     # the conditions that the ball hits the paddle
                    self.move_ball()

    def reset_ball(self):                      # make the ball back to the initial status
        self.__dx = 0
        self.__dy = 0
        self.window.add(self.ball, x=self.window.width / 2 - self.ball.width / 2,
                        y=self.window.height / 2 - self.ball.height / 2)
        self.mouse_disable = False
