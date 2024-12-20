import random
import curses

def main(screen):
    # Initialize the screen
    curses.curs_set(0)
    sh, sw = screen.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    # Initial position of the snake
    snk_x = sw // 4
    snk_y = sh // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    # Initial position of the food
    food = [sh // 2, sw // 2]
    w.addch(food[0], food[1], curses.ACS_PI)

    # Initial direction of the snake
    key = curses.KEY_RIGHT

    while True:
        next_key = w.getch()
        if next_key == -1:
            next_key = key
        if (next_key == curses.KEY_DOWN and key != curses.KEY_UP) or \
           (next_key == curses.KEY_UP and key != curses.KEY_DOWN) or \
           (next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT) or \
           (next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT):
            key = next_key

        # Calculate the new head of the snake
        if key == curses.KEY_DOWN:
            new_head = [snake[0][0] + 1, snake[0][1]]
        elif key == curses.KEY_UP:
            new_head = [snake[0][0] - 1, snake[0][1]]
        elif key == curses.KEY_LEFT:
            new_head = [snake[0][0], snake[0][1] - 1]
        elif key == curses.KEY_RIGHT:
            new_head = [snake[0][0], snake[0][1] + 1]

        # Insert the new head of the snake
        snake.insert(0, new_head)

        # Check if snake has hit the border or itself
        if (snake[0][0] in [0, sh - 1] or
            snake[0][1] in [0, sw - 1] or
            snake[0] in snake[1:]):
            break

        # Check if snake has eaten the food
        if snake[0] == food:
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
        
        # Draw the border
        w.border(0)

        # Display the score
        score = len(snake) - 3
        w.addstr(0, 2, 'Score: ' + str(score) + ' ')

        w.refresh()

    # Game over screen
    w.addstr(sh // 2, sw // 2 - len("Game Over!") // 2, "Game Over!")
    w.addstr(sh // 2 + 1, sw // 2 - len("Press Enter to restart") // 2, "Press Enter to restart")
    w.refresh()
    while True:
        key = w.getch()
        if key == 10:  # Enter key
            main(screen)
            break

if __name__ == "__main__":
    curses.wrapper(main)