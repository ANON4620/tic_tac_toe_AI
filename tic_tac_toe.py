


import random

player = None
computer = None
cur_player = None
available_pos = None
pos_left = None
board = None
cur_pos_played = None
cur_match_data = None
trained_data = None
move_count = None

def draw_board():
    print()
    print()
    print()
    print()
    print("            |             |")
    print("            |             |")
    print("      {}     |      {}      |     {}".format(board[0][0], board[0][1], board[0][2]))
    print("            |             |")
    print("            |             |")
    print("------------|-------------|------------")
    print("            |             |")
    print("            |             |")
    print("      {}     |      {}      |     {}".format(board[1][0], board[1][1], board[1][2]))
    print("            |             |")
    print("            |             |")
    print("------------|-------------|------------")
    print("            |             |")
    print("            |             |")
    print("      {}     |      {}      |     {}".format(board[2][0], board[2][1], board[2][2]))
    print("            |             |")
    print("            |             |")
    print()

def clear_board_data():
    for i in range(3):
        for j in range(3):
            board[i][j] = " "          # Space character

def check_rows():
    for i in range(3):
        count = 0
        for j in range(3):
            if board[i][j] == cur_player:
                count += 1
            else:
                break
        if count == 3:
            return True
    return False

def check_columns():
    for i in range(3):
        count = 0
        for j in range(3):
            if board[j][i] == cur_player:
                count += 1
            else:
                break
        if count == 3:
            return True
    return False

def check_diagonals():
    # Left diagonal
    if board[0][0] == cur_player and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return True
    # Right diagonal
    if board[0][2] == cur_player and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return True
    return False

def switch_player():
    global cur_player
    if cur_player == player:
        cur_player = computer
    else:
        cur_player = player

def setup_game():
    # Set up players
    global player, computer, cur_player
    player = "X"
    computer = "O"
    cur_player = player

    # Set up board
    global board
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("PLAYER   -- X")
    print("COMPUTER -- O")
    
    draw_board()
    clear_board_data()

    # Set available positions tracker
    global available_pos
    available_pos = []
    for i in range(3):
        for j in range(3):
            available_pos.append(str(i) + str(j))
    
    # Set number of available positions tracker
    global pos_left
    pos_left = len(available_pos)

    # Set default current match data
    global cur_match_data
    cur_match_data = []

    # Set default move count
    global move_count
    move_count = 0

def autoplay_last_position_left():
    pos = available_pos[0]
    row = int(pos[0])
    col = int(pos[1])
    board[row][col] = cur_player
    global cur_pos_played
    cur_pos_played = pos

def player_plays():
    while True:
        inp = int(input(">> ")) - 1
        row = inp // 3
        col = inp % 3
        pos = str(row) + str(col)
        if pos in available_pos:
            board[row][col] = cur_player
            global cur_pos_played
            cur_pos_played = pos
            break
        else:
            print("Invalid position!")

def check_immediate_win():
    for pos in available_pos:
        row = int(pos[0])
        col = int(pos[1])
        board[row][col] = cur_player
        if check_rows() or check_columns() or check_diagonals():
            global cur_pos_played
            cur_pos_played = pos
            return True
        board[row][col] = " "          # Space character
    return False
            
def check_block_player():
    for pos in available_pos:
        switch_player()
        row = int(pos[0])
        col = int(pos[1])
        board[row][col] = cur_player
        if check_rows() or check_columns() or check_diagonals():
            switch_player()
            board[row][col] = cur_player
            global cur_pos_played
            cur_pos_played = pos
            return True
        switch_player()
        board[row][col] = " "          # Space character
    return False

def play_random():
    pos = random.choice(available_pos)
    row = int(pos[0])
    col = int(pos[1])
    board[row][col] = cur_player
    global cur_pos_played
    cur_pos_played = pos

def computer_plays(search_training_data_enabled, immediate_win_enabled=True, block_player_enabled=True):
    computer_played = False
    
    if search_training_data_enabled:
        computer_played = play_on_training_data()
    if immediate_win_enabled and not computer_played:
        computer_played = check_immediate_win()
    if block_player_enabled and not computer_played:
        computer_played = check_block_player()
    if not computer_played:
        play_random()







##########   AI part   ##########
def write_new_training_data():
    new_data = " ".join(cur_match_data) + "\n"
    trained_data.append(new_data)
    trained_data.sort()
    file = open("training_data.txt", "w")
    file.writelines(trained_data)
    file.close()

def search_training_data():
    filtered_trained_data = []
    
    cur_match_data_str = " ".join(cur_match_data)
    for data in trained_data:
        if data.startswith(cur_match_data_str):
            filtered_trained_data.append(data)
            
    if filtered_trained_data == []:
        return ""
    
    data = random.choice(filtered_trained_data)
    return data

def play_on_training_data():
    data = search_training_data()
    if data == "":
        return False
    datalist = data.split()
    pos = datalist[move_count]
    row = int(pos[0])
    col = int(pos[1])
    board[row][col] = cur_player
    global cur_pos_played
    cur_pos_played = pos
    return True


##########   Training Mode   ##########
def train():
    setup_game()
    global pos_left
    while pos_left > 0:
        if pos_left == 1:
            autoplay_last_position_left()
        else:
            computer_plays(search_training_data_enabled = False)

        cur_match_data.append(cur_pos_played)
        available_pos.remove(cur_pos_played)
        pos_left -= 1
        global move_count
        move_count += 1

        draw_board()

        if check_rows() or check_columns() or check_diagonals():
            if cur_player == computer and search_training_data() == "":
                write_new_training_data()
            return

        switch_player()




##########   Play Mode   ##########
def play():
    setup_game()

    global pos_left
    while pos_left > 0:
        if pos_left == 1:
            autoplay_last_position_left()
        elif cur_player == player:
            player_plays()
        else:
            computer_plays(search_training_data_enabled = True)

        cur_match_data.append(cur_pos_played)
        available_pos.remove(cur_pos_played)
        pos_left -= 1
        global move_count
        move_count += 1

        draw_board()

        if check_rows() or check_columns() or check_diagonals():
            if cur_player == player:
                return "You Win :)"
            else:
                if search_training_data() == "":
                    write_new_training_data()

                return "You Lose :("

        switch_player()

    return "Match Draw :|"



# Load trained data in memory
file = open("training_data.txt", "r")
trained_data = file.readlines()
file.close()

# Game starts here
print("ENTER 1 to play.")
print("ENTER 2 to train.")
choice = int(input())
if choice == 1:
    result = play()
    print(result)
elif choice == 2:
    matches = int(input("Enter number of training matches: "))
    for match in range(matches):
        train()
else:
    print("Invalid input!")




