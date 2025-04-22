import random
import curses

def main(screen):
    # Initialize the screen
    curses.curs_set(0)
    sh, sw = screen.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    # Difficulty selection
    difficulty = 100  # Default speed
    w.addstr(0, 2, "Select Difficulty: 1 (Easy), 2 (Medium), 3 (Hard)")
    w.refresh()
    while True:
        diff_key = w.getch()
        if diff_key == ord('1'):
            difficulty = 150
            break
        elif diff_key == ord('2'):
            difficulty = 100
            break
        elif diff_key == ord('3'):
            difficulty = 50
            break

    # Snake appearance selection
    snake_char = curses.ACS_CKBOARD  # Default character
    w.addstr(1, 2, "Select Snake Appearance: 1 (Block), 2 (Hash), 3 (Star)")
    w.refresh()
    while True:
        char_key = w.getch()
        if char_key == ord('1'):
            snake_char = curses.ACS_CKBOARD
            break
        elif char_key == ord('2'):
            snake_char = ord('#')
            break
        elif char_key == ord('3'):
            snake_char = ord('*')
            break

    # High score initialization
    high_score = 0

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
        # Adjust speed based on score
        w.timeout(max(50, difficulty - (len(snake) - 3) * 5))

        next_key = w.getch()
        if next_key == ord('p') or next_key == ord('P'):  # Pause functionality
            while True:
                pause_key = w.getch()
                if pause_key == ord('p') or pause_key == ord('P'):
                    break

        if next_key == -1:
            next_key = key
        if (next_key == curses.KEY_DOWN and key != curses.KEY_UP) or \
           (next_key == curses.KEY_UP and key != curses.KEY_DOWN) or \
           (next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT) or \
           (next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT):
            key = next_key

        # Calculate the new head of the snake
        if key == curses.KEY_DOWN:
            new_head = [(snake[0][0] + 1) % sh, snake[0][1]]
        elif key == curses.KEY_UP:
            new_head = [(snake[0][0] - 1) % sh, snake[0][1]]
        elif key == curses.KEY_LEFT:
            new_head = [snake[0][0], (snake[0][1] - 1) % sw]
        elif key == curses.KEY_RIGHT:
            new_head = [snake[0][0], (snake[0][1] + 1) % sw]

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

        w.addch(snake[0][0], snake[0][1], snake_char)

        # Display the score and high score
        score = len(snake) - 3
        if score > high_score:
            high_score = score
        w.addstr(0, 2, f'Score: {score} High Score: {high_score}')

        w.refresh()

    # Game over screen
    w.clear()
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