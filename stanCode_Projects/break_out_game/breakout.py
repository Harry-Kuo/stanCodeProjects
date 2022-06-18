"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

Name: Harry Kuo
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 2000 / 120  # 120 frames per second
NUM_LIVES = 10			 # Number of attempts


def main():
    graphics = BreakoutGraphics()
    graphics.set_lives(NUM_LIVES)
    # Add the animation loop here!
    while True:
        graphics.move_ball()
        graphics.check_for_collisions()
        graphics.handle_wall_collisions()
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
