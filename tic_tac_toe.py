


import random

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

def clear_board():
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

def train(training_data_exist):
    global number_of_new_records_added
    new_training_data = " ".join(cur_match_moves) + "\n"

    if training_mode:
        # Check whether data already exist in training data or not
        if new_training_data in trained_moves_set:
            training_data_exist = True
        else:
            training_data_exist = False
    
    if not training_data_exist:
        trained_moves_set.add(new_training_data)
        trained_moves_updated = list(trained_moves_set)
        trained_moves_updated.sort()
        file = open("training_data.txt", "w")
        file.writelines(trained_moves_updated)
        file.close()
        number_of_new_records_added += 1


print("ENTER 1 to play.")
print("ENTER 2 to train.")
choice = int(input())

##### Training mode just trains the computer (you don't get to play) #####
# Note: This does not mean that the computer does not trains itself when training mode is off. When training mode is off, the computer trains itself based on how you play.
# You don't need to change the value here because on running the program you are asked whether to play or just train the computer.
training_mode = False
matches = 0
if choice == 1:
    matches = 1
elif choice == 2:
    training_mode = True
    matches = int(input("Enter number of training matches: "))
else:
    print("Invalid input!")


# On training mode the training data file is read at once rather than reading line by line
trained_moves_set = set()
if training_mode:
    file = open("training_data.txt", "r")
    trained_moves_set = set(file.readlines())
    file.close()



for match in range(matches):
    

    ########################     Flags or switches (these are safe to change)     ########################

    ##### Turn on or off computer's playing logic #####
    # Change these flags to better train the computer, otherwise turn all of them to True
    # Caution!: If you turn off both check_immediate_win and check_block_player
    #           And enter training mode, the computer will be trained on random moves which will not produce an intelligent AI
    check_training_data = True        # Make sure the training data is sorted otherwise the program will not work correctly
    check_immediate_win = True
    check_block_player = True

    ##### Debug_mode prints critical information about how the game acts #####
    debug_mode = True



    if not training_mode:
        file = open("training_data.txt", "r")

    #############  Setting up variables (Caution!: Changing these may result in unexpected behaviour)  #############
    player = "X"
    computer = "O"
    cur_player = player
    move_number = 0
    cur_match_moves = []
    trained_moves = []
    game_is_draw = True
    pos = ""
    is_computers_first_move = True      # Computer plays its first move randomly. (When on training mode computer plays from both the sides so both the first moves are random)
    training_data_exist = True
    first_scan_on_training_data = True
    number_of_new_records_added = 0
    
    # Setting up board
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("PLAYER   -- X")
    print("COMPUTER -- O")
    draw_board()

    # Clearing the board
    clear_board()

    # Tracking the available positions
    available_pos = []
    for i in range(3):
        for j in range(3):
            available_pos.append(str(i) + str(j))
    pos_left = len(available_pos)

    while pos_left > 0:
        
        # Automatically play last position left
        if pos_left == 1:
            pos = available_pos[0]
            row = int(pos[0])
            col = int(pos[1])
            board[row][col] = cur_player
            
        # If current player is player
        elif cur_player == player and not training_mode:
            inp = int(input(">> ")) - 1
            row = inp // 3
            col = inp % 3
            pos = str(row) + str(col)
            if pos in available_pos:
                board[row][col] = cur_player
            else:
                print("Invalid position!")
                continue
                
        # If current player is computer (if on training mode current player can be player as well)
        else:
            computer_played = False

            if not is_computers_first_move:
            # Play on trained data
            # Make sure the training data is sorted otherwise the program will not work correctly
                if check_training_data and not training_mode and training_data_exist:
                    # Try to match the already searched training data with the current match moves
                    if trained_moves[0:move_number] == cur_match_moves:
                        row, col = int(trained_moves[move_number][0]), int(trained_moves[move_number][1])
                        pos = str(row) + str(col)
                        board[row][col] = cur_player
                        computer_played = True
                        if debug_mode:
                            print("Played on trained data")
                    else:
                        # Find the training data
                        line = file.readline()
                        while line:
                            if debug_mode:
                                print("Searching training data")
                            trained_moves = line.split()
                            
                            # Extract that number of moves from the trained data that we have played in the current match
                            # And check if that equals the current match moves
                            if trained_moves[0:move_number] == cur_match_moves:
                                row, col = int(trained_moves[move_number][0]), int(trained_moves[move_number][1])
                                pos = str(row) + str(col)
                                board[row][col] = cur_player
                                computer_played = True
                                first_scan_on_training_data = False
                                if debug_mode:
                                    print("Played on trained data")
                                break
                            if not first_scan_on_training_data and trained_moves[0:move_number-1] != cur_match_moves[0:-1]:
                                training_data_exist = False
                                if debug_mode:
                                    print("Data does not exist")
                                break
                            line = file.readline()
                        # Check if file is empty or if file pointer reaches the end of the file
                        if line == "":
                            training_data_exist = False
                            if debug_mode:
                                print("Data does not exist")

                # Check for an immediate win
                if check_immediate_win and not computer_played:
                    for pos in available_pos:
                        row = int(pos[0])
                        col = int(pos[1])
                        board[row][col] = cur_player
                        if check_rows() or check_columns() or check_diagonals():
                            computer_played = True
                            if debug_mode:
                                print("Played on logic")
                            break
                        board[row][col] = " "          # Space character

                # Check for blocking the opponent ( From the computer's point of view )
                if check_block_player and not computer_played:
                    for pos in available_pos:
                        switch_player()
                        row = int(pos[0])
                        col = int(pos[1])
                        board[row][col] = cur_player
                        if check_rows() or check_columns() or check_diagonals():
                            switch_player()
                            board[row][col] = cur_player
                            computer_played = True
                            if debug_mode:
                                print("Played on logic")
                            break
                        switch_player()
                        board[row][col] = " "          # Space character
                    
            # Play random
            if not computer_played:
                pos = random.choice(available_pos)
                row = int(pos[0])
                col = int(pos[1])
                board[row][col] = cur_player
                computer_played = True
                if debug_mode:
                    print("Played randomly")

                # After the first move is played by the computer
                if move_number > 0:
                    is_computers_first_move = False

        # Remove the available position from list
        available_pos.remove(pos)
        pos_left -= 1

        # Store Current Match Data in Buffer
        cur_match_moves.append(pos)
        move_number += 1
        
        # Draw on screen #
        draw_board()

        # Check if result is a win
        if check_rows() or check_columns() or check_diagonals():
            game_is_draw = False
            print(cur_player, "WON!")

            #############         Train the computer         #############
            # If computer won
            if cur_player == computer:
                train(training_data_exist)
            
            if not training_mode:
                input("Press ENTER to exit...")
            break

        # Switch player
        switch_player()

    # Check if result is a draw
    if game_is_draw:
        print("DRAW!")
        if not training_mode:
            input("Press ENTER to exit...")


    if not training_mode:
        file.close()

if debug_mode:
    print("Number of new records added =", number_of_new_records_added)
