from a1_support import *
import re


# # Print dashes
def printLine(grid_size):
    for i in range((grid_size+1) ** 2):
        print("-", end='')
    print()


# # 1. display_game Show grid
def display_game(game, grid_size):
    print(" ", end="")
    for i in range(grid_size):
        print(" |", i + 1, end='')
    print(" |")
    for i in range(grid_size):
        printLine(grid_size)
        print(ALPHA[i], "|", end="")
        for j in range(grid_size):
            print("",game[i * grid_size + j] , "|", end='')
        print()
    printLine(grid_size)
    print()


# # 2. parse_position
# # Command to be entered action ，Convert to 2D coordinates position
def parse_position(action, grid_size):
    # # # 正则匹配
    # if action.isdigit()==False and action.isalpha()==False and action!='':
    #    ch = re.findall(r'[0-9]+|[A-Z]+|[a-z]', action)
    #    num = re.findall(r'[0-9]+|[A-Z]+|[a-z]', action)
    #
    # # if len(ch) != 1 or len(num) != 1:
    # #     return None
    #    ch = ord(ch) - 64
    #    num = int(num)
    #    if ch and num <= grid_size:
    #       position = (ch - 1, num - 1)
    #    else:
    #     position = None
    #    return position
    # return None
    # #Regular match
    chars = re.findall(r'[A-Z]+|[0-9]+', action)
    if chars is None or len(chars) != 2:
        return None
    # # Letters to numbers
    ch = ord(chars[0]) - 64
    num = int(chars[1])
    # print('ch**: ', ch)
    # print('num**: ', num)
    if ch and num <= grid_size:
        position = (ch - 1, num - 1)
    else:
        position = None
    return position


# # 3. position to index
def position_to_index(position, grid_size):
    x = position[0]
    y = position[1]
    index = x * grid_size + y
    return index


# # 4. replace character at index
def replace_character_at_index(game, index, character):
    game = list(",".join(game).replace(',', ''))
    game[index] = str(character)
    return "".join(game)


# # 5. flag cell
def flag_cell(game, index):
    if game[index] == UNEXPOSED:
        return replace_character_at_index(game, index, FLAG)
    elif game[index] == FLAG:
        return replace_character_at_index(game, index, UNEXPOSED)
    else:
        print("Flag Error, the cell can't flag.")
        return game


# # 6. index in direction
def index_in_direction(index, grid_size, direction):
    row = int(index / grid_size)
    col = index % grid_size
    if direction == UP:
        if row == 0:
            return None
        return (row - 1) * grid_size + col
    elif direction == DOWN:
        if row == grid_size - 1:
            return None
        return (row + 1) * grid_size + col
    elif direction == LEFT:
        if col == 0:
            return None
        return row * grid_size + col - 1
    elif direction == RIGHT:
        if col == grid_size - 1:
            return None
        return row * grid_size + col + 1
    elif direction == "up-left":
        if row == 0 or col == 0:
            return None
        return (row - 1) * grid_size + col - 1
    elif direction == "up-right":
        if row == 0 or col == grid_size - 1:
            return None
        return (row - 1) * grid_size + col + 1
    elif direction == "down-left":
        if row == grid_size - 1 or col == 0:
            return None
        return (row + 1) * grid_size + col - 1
    elif direction == "down-right":
        if row == grid_size - 1 or col == grid_size - 1:
            return None
        return (row + 1) * grid_size + col + 1
    return None


# # 6. neighbour directions
# Indexed list with adjacent cells
def neighbour_directions(index, grid_size):
    data = [index_in_direction(index, grid_size, UP), index_in_direction(index, grid_size, DOWN),
            index_in_direction(index, grid_size, LEFT), index_in_direction(index, grid_size, RIGHT),
            index_in_direction(index, grid_size, "up-left"), index_in_direction(index, grid_size, "up-right"),
            index_in_direction(index, grid_size, "down-left"), index_in_direction(index, grid_size, "down-right")]
    return list(filter(None, data))


# # 7. number at cell
def number_at_cell(game, pokemon_locations, grid_size, index):
    neighbours = neighbour_directions(index, grid_size)
    count = 0
    for pokemon_location in pokemon_locations:
        if pokemon_location in neighbours:
            count = count + 1
    return count


# # 8. check win
def check_win(game, pokemon_locations):
    uncover=game.count(UNEXPOSED)
    flag=game.count(FLAG)
    if uncover==0 and flag==len(pokemon_locations):
        return True
    else:
        return False



def main():
    # # grid_size
    while True:
        grid_size = int(input("Please input the size of the grid: "))
        if grid_size < 0 or grid_size > 26:
            print("Input Error, grid_size is error. ( 26 is the maximum. )")
        else:
            #print("Input Successful.")
            break
    # # number of pokemons
    while True:
        m = int(input("Please input the number of pokemons: "))
        if m < 0 or m > grid_size ** 2:
            print("That ain't a valid action buddy.")
        else:
            #print("Input Successful.")
            break
    # # New game game list
    game = [UNEXPOSED] * grid_size ** 2
    # # display game game list
    display_game(game, grid_size)
    # # Get random pokemon list
    pokemons = generate_pokemons(grid_size, m)
    # # Execute game command action
    while True:
        action = input("Please input action: ")
        if action == ':)':
            print("It's rewind time.")
            game =  [UNEXPOSED] * grid_size ** 2
            pokemons = generate_pokemons(grid_size, m)
            display_game(game, grid_size)
            continue

        #if len(action)==2:
          #ch, num = re.findall(r'[0-9]+|[A-Z]+', action)
          #print('ch:', ch)
          #print('num: ', num)
        tag = re.findall(r'[a-z]', action)
        #print('tag: ', tag)


        if len(tag) == 1:
            # # help
            if tag[0] == 'h':
                print(HELP_TEXT)
                display_game(game, grid_size)
                continue
            # # exit game
            elif tag[0] == 'q':
                command = input("You sure about that buddy? (y/n): ")
                if command == 'y':
                    print("Catch you on the flip side.")
                    return
                elif command == 'n':
                    print("Let's keep going.")
                    display_game(game, grid_size)
                    continue
                else:
                    print("That ain't a valid action buddy.")
                    display_game(game, grid_size)
                    continue


            # # label grid
            elif tag[0] == 'f':
                position = parse_position(action, grid_size)
                if position is None:
                    print("That ain't a valid action buddy.")
                else:
                    index = position_to_index(position, grid_size)
                    game = flag_cell(game, index)
                    display_game(game, grid_size)
                    if check_win(game, pokemons):
                        print("You win.")
                        return
                continue
        # # choose grid
        position = parse_position(action, grid_size)
        if position is None:
            print("That ain't a valid action buddy.")
            display_game(game, grid_size)
            continue
        index = position_to_index(position, grid_size)
        #print('index: ', index)
        # # Click to pokemon
        if index in pokemons:
            for pokemon in pokemons:
                game = replace_character_at_index(game, pokemon, POKEMON)
            display_game(game, grid_size)
            print("You have scared away all the pokemons.")
            return
        # # Point to non-pokemon and unexposed areas
        if game[index] != UNEXPOSED:
            print("You didn't do anything.")
            display_game(game, grid_size)
        else:
            count = number_at_cell(game, pokemons, grid_size, index)
            #print('count: ', count)
            #print('index: ', index)
            game = replace_character_at_index(game, index, count)
            if count != 0:
                display_game(game, grid_size)
            else:
                neighbours = big_fun_search(game, grid_size, pokemons, index)
                for neighbour in neighbours:
                    count = number_at_cell(game, pokemons, grid_size, neighbour)
                    game = replace_character_at_index(game, neighbour, count)
                display_game(game, grid_size)
        if check_win(game, pokemons):
            print("You win.")
            return



#########################UNCOMMENT THIS FUNCTION WHEN READY#######################
def big_fun_search(game, grid_size, pokemon_locations, index):
    """Searching adjacent cells to see if there are any Pokemon"s present.

    Using some sick algorithms.

    Find all cells which should be revealed when a cell is selected.

    For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
    neighbours are revealed. If one of the neighbouring cells is also zero then
    all of that cell"s neighbours are also revealed. This repeats until no
    zero value neighbours exist.

    For cells which have a non-zero value (i.e. cells with neightbour pokemons), only
    the cell itself is revealed.

    Parameters:
        game (str): Game string.
        grid_size (int): Size of game.
        pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
        index (int): Index of the currently selected cell

    Returns:
        (list<int>): List of cells to turn visible.
    """
    queue = [index]
    discovered = [index]
    visible = []

    if game[index] == FLAG:
        return queue

    number = number_at_cell(game, pokemon_locations, grid_size, index)
    if number != 0:
        return queue

    while queue:
        node = queue.pop()
        for neighbour in neighbour_directions(node, grid_size):
            if neighbour in discovered or neighbour is None:
                continue
            discovered.append(neighbour)
            if game[neighbour] != FLAG:
                number = number_at_cell(game, pokemon_locations, grid_size, neighbour)
                if number == 0:
                    queue.append(neighbour)
            visible.append(neighbour)
    return visible


#########################UNCOMMENT THIS FUNCTION WHEN READY#######################

if __name__ == "__main__":
    main()
