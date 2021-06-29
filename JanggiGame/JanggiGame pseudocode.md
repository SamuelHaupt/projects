

- Initializing the board
- Determining how to represent pieces  at a given location on the board
- Determining how to validate a given move according to the rules for each piece, turn taking and other game rules.
- Modifying the board state after each move.
- Determining how to track which player's turn it is to play right now.
- Determining how to detect the checkmate scenario.
- Determining which player has won and also figuring out when to check that.


1. Initialize the board:

    Initialize private data members used for board, such as board, palace, board columns and rows, and positions of each general.
    Create a board with lists within a list
    Iterate through 10 times creating 10 lists
    Iterate through 9 times creating 9 'None' placeholders within each list
    Set board to the entire list

2. Determining how to represent pieces at a given location on the board:

    Create seven different game pieces, such as General, Guard, Horse, Elephant, Chariot, Cannon, and Solider.
    Initialize private data members for each game piece, such as label, player owner, legal moves, and potential moves.
    Set legal moves to lists within a list within a dictionary within a dictionary that contains directional movements for red and blue players and diagonal movements within the palace
    Initilize a Janggi board game and create two of each game piece for each player, except only one General is created for each player.
    Transpose required game piece positions into index format for lists
    Place game pieces at transposed positions on the board
    None is a placeholder everywhere else a game piece does not exist

3. Determining how to validate a given move according to the rules for each piece, turn taking and other game rules.
    
    Turn taking:
    Check current player
    Retrieve game piece at position from which player wishes to move
    Retrieve player owner for game piece
    If player owner is opponent, return False
    If player owner is current player, continue

    Out of bounds:
    Retrieve 'position from' and 'position to' from given fields
    Transpose positions into board index format
    Set valid move to false if either position is outside the index limits of the board

    Capture friendly player:
    Use transposed position for either iterating over squares or whatever is the desired destination
        and retrieve game piece at position
    Retrieve current player
    Retrieve game piece player
    If current player and game piece player are equal, return False

    Cannon jump over cannon or capture cannon:
    Use transposed position for iterating over squares
    Check instance of game piece with Cannon
    If True, return False
    If False, set screen to True and continue iteration
    Use transposed position for either iterating over squares or whatever is the desired destination
        and retrieve game piece at position
    If game piece is None, continue
    If game piece is a game piece, check Check instance of game piece with Cannon
    If True, return False

    Guard or General out of bounds:
    Retrieve 'position from' and 'position to' from given fields
    Transpose positions into board index format
    Set valid move to false if either position is outside the index limits of palace

    Game Piece not at desired location:
    Retrieve 'position from' from given field
    Transpose position into board index format
    Retrieve game piece at transposed position
    If game piece is None, return False
    Otherwise, continue

    Move not within potential moves:
    Retrieve 'position from' from given field
    Transpose position into board index format
    Retrieve game piece at transposed position
    Retrieve potential moves from game piece
    Check if 'position to' (non-transposed) is in list of potential moves
    If not in list, return False
    If in list, continue

    Horse or Elephant are blocked (Possible Way To Do So):
    Retrieve 'position from' and 'position to' from given fields
    Use transposed position for iterating over squares
    Increment one step at a time
    Each step used transposed position to retrieve game piece
    If game piece is a game piece, return False
    Otherwise, continue iterating and repeat.

    Horse or Elephant are blocked (My Way Of Doing So):
    Retrieve 'position from' and 'position to' from given fields
    Transpose 'position from'
    Retrieve game piece from transposed position
    Check instance against Horse or Elephant
    Based on find, retrieve potential moves from Horse or Elephant
    Check if 'position_to' (non_transposed) is in potential moves list
    If True, return True
    Otherwise, return False.

4. Modifying the board state after each move.

    After valid move takes place, copy game piece object from previous location
    If location to which the move was successful, delete opponent game piece at position, if present
    Input copied game piece object into new position (Deleted game piece is still instantiated, but no longer accessible on the board)
    Update potential moves for all game pieces on the board
    Test whether current player has opponent general in checkmate
    If True, check player.
    If player is 'RED', change game state to 'RED_WON'
    If player is 'BLUE', change game state to 'BLUE_WON'
    Update turn to opponent
    Return True, since move was valid

5. Determining how to track which player's turn it is to play right now.

    Set private data member in board to 'BLUE' to indcate the blue player starts the game.
    Check if move was successful.
    Check private data member to determine if current player is 'BLUE' or 'RED'
    Set data member to opposite player.

6. Determining how to detect the checkmate scenario.
    
    Check which player is opponent
    Retrieve general position for opponent
    Get general at position
    Get potential moves for general
    Create a copied list that includes general's potential moves and current position
    Retrieve board
    Iterate through rows in the board
    Iterate through columns in each row and retrieve potential moves for each player (enemy to the general) game piece
    Any matching potential moves, remove from copied list

    Iterate through copied list testing remaining position simulations
    At each position for the remaining positions within copied list, copy game piece or None into a temporary holder
    Move general to remaining position
    Update all game piece potential moves based on general's new position
    Iterate through rows in the board
    Iterate through columns in each row and retrieve potential moves for each player (enemy to the general) Cannon/Chariot game piece
    Any matching potential moves, remove from copied list

    Copy general game piece and place into (original) general position
    Replace game piece from temporary holder at the remaining (original) position
    Return True if list is empty, otherwise return False

7. Determining which player has won and also figuring out when to check that.

    Use checkmate from detecting checkmake scenario and test checkmate against opponent general
    If True, check player.
    If player is 'RED' change game state to 'RED_WON'
    If player is 'BLUE' change game state to 'BLUE_WON'

    Only check checkmate after each valid move and after all potential moves have been updated for each game piece. If a checkmate was caused by the current player
    so that friendly general was in checkmate, valid move check would ensure that the move could not be done. Therefore, only check checkmate after each move and 
    for opponent general.