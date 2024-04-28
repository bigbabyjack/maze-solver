from window import Window
from cell import Cell


def main():
    win = Window(800, 600)

    c1 = Cell(win)
    c1.has_left_wall = False
    c1.draw(50, 50, 100, 100)

    c2 = Cell(win)
    c2.has_right_wall = False
    c2.draw(120, 120, 250, 250)

    c1.draw_move(c2)

    c3 = Cell(win)
    c3.has_top_wall = False
    c3.draw(300, 300, 800, 800)
    c2.draw_move(c3)

    c4 = Cell(win)
    c4.has_bottom_wall = False
    c4.draw(500, 500, 200, 200)
    win.wait_for_close()

    c3.draw_move(c4)


main()
