"""
DOCSTRING
"""
import sys
import terminal

def healthy_neighbors(x, y, grid):
    """ 
    healthy_neighbors: Returns the number of live cells neighboring the 
    given coordinate. Given it treats the grid as a loop (making this
    optional is a to-do) it should be able to handle most dumb calls.
    """
    live_neighbors = 0
    for i in range(-1, 2):
        testx = (x+i) % len(grid[0])
        for j in range(-1, 2):
            testy = (y+j) % len(grid)
            if j == 0 and i == 0:
                continue
            if grid[testy][testx] == 1:
                live_neighbors += 1
    return live_neighbors

def main():
    """
    DOCSTRING
    """
    (width, height) = terminal.get_term_size()
    grid = [(width-5)*[0] for i in range(height-5)]
    update_screen(grid)
    read_initial_conf(grid)
    prompt = ('ITER %d: Type anything to continue, the number of steps to ' + 
              'perform (or quit to exit): ')
    iter_step = 1
    update_screen(grid)
    while True:
        play = input('%s' % (prompt % iter_step))
        if play == 'quit':
            break
        try:
            batch_steps = int(play)
        except:
            batch_steps = 1
            pass
        for i in range(batch_steps):
            new_grid = [len(grid[0])*[0] for i in range(len(grid))]
            next_step(grid, new_grid)
            grid, new_grid = new_grid, grid
            update_screen(grid)
        iter_step += batch_steps

def next_step(grid, new_grid):
    """ 
    next_step: Computes the grid's next step and stores it in the list
    new_grid. The latter needing to have been previously defined.
    """
    for x in range(0, len(grid[0])):
        for y in range(0, len(grid)):
            live_neighbors = healthy_neighbors(x, y, grid)
            if grid[y][x]:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = grid[y][x]
            else:
                if live_neighbors == 3:
                    new_grid[y][x] = 1

def read_initial_conf(grid):
    """ 
    read_initial_conf: Reads coordinates from the user to configure the
    initial game's grid.
    It takes an already defined grid and modifies it according to user input.
    (It shouldn't let invalid input leak)
    """
    done = False
    prompt = 'CONFIG %d: Type coordinates to toggle (or start to finish) %s: '
    config_step = 0
    last_coord = ''
    while True:
        coord = []
        sys.stdout.write(prompt % (config_step, last_coord))
        while coord == []:
            cmd = input()
            if cmd == 'start' or cmd == '':
                done = True
                break
            try:
                cmd = cmd.split()
                coord = [int(cmd[i]) for i in range(2)]
            except:
                sys.stdout.write(terminal.bcolors.RED + '[Invalid input] %s' %
                                 (prompt % (config_step, last_coord)) 
                                 + terminal.bcolors.ENDC)
            last_coord = str(coord)
            config_step += 1
        if done:
            break
        grid [coord[1]][coord[0]] = (grid[coord[1]][coord[0]] + 1) % 2
        update_screen(grid)
    
def update_screen(grid):
    """ 
    update_screen: Takes the grid and updates the terminal to display it.
    (Making this function more efficient and informative is a to-do)
    """
    terminal.clear_terminal()
    print(terminal.bcolors.RED + ' GAME OF LIFE' + terminal.bcolors.ENDC)
    print(terminal.bcolors.YELLOW + '-'*( len(grid[0]) + 5) + terminal.bcolors.ENDC)
    print
    for i, line in enumerate(grid):
        print(terminal.bcolors.BLUE + '%3d ' % i + terminal.bcolors.ENDC)
        for element in line:
            if element:
                sys.stdout.write(terminal.bcolors.RED + str(element) + terminal.bcolors.ENDC)
            else:
                sys.stdout.write('0')
        print()
    print(terminal.bcolors.YELLOW + '-' * ( len(grid[0]) + 5 ) + terminal.bcolors.ENDC)

if __name__ == '__main__':
    main()
