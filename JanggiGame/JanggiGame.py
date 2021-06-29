import copy

class GamePiece(object):
    """
    Parent class for the seven different game pieces: 
        General, Guard, Horse, Elephant, 
        Chariot, Cannon, and Soldier.
    GamePiece interacts with seven classes to record label, player owner, legal
    moves, and potential moves for each object. There are corresponding getters
    and setters methods. Label is used with the __repr__ function for official
    representation of each object. Player is either 'BLUE' or 'RED' to indicate
    player owner. Legal moves houses movements specific to the class that give
    each GamePiece dimension to their movements, which varies across the seven 
    subclasses. After GamePiece objects are composed within JanggiGame class, 
    legal moves are accessed by methods so titled for the corresponding 
    GamePiece subclasses. Potential moves is a container that is updated after 
    every move that takes place on the board. After objects are composed within 
    JanggiGame, potential moves is accessed by is_in_check and is_checkmate 
    methods within JanggiGame. Potential moves for each GamePiece speeds up the
    process for checking if game is in check or checkmate. GamePieces are 
    represented within Board/JanggiGame and become the object on which JanggiGame
    performs methods. 
    """
    
    def __init__(self, label, player):
        """
        Takes in label and player as strings and initizalized to corresponding
        data member. Private data members are _label, _player, _legal_moves, and 
        _potential_moves. Use .upper() method on _player to ensure consistency 
        throughout program. _legal_moves and _potential_moves are initialized to
        an empty dict() and list(), respectively.
        """
        
        self._label = label
        self._player = player.upper()
        self._legal_moves = dict()
        self._potential_moves = list()

    def get_label(self):
        """
        Takes in no parameters. Returns _label (string) for GamePiece.
        """

        return self._label

    def set_label(self, label):
        """
        Takes in label (string) and sets _label of GamePiece to it.
        """

        self._label = label

    def get_player(self):
        """
        Takes in no parameters. Returns _player (string) of GamePiece.
        """

        return self._player

    def set_player(self, player):
        """
        Takes in player (string) and sets _player of GamePiece to 'BLUE' or 'RED'.
        """

        self._player = player

    def get_legal_moves(self):
        """
        Takes in no parameters. 
        Returns _legal_moves (dict) for GamePiece.
        Further access includes 'RED' & 'BLUE' keys with 'board' and 'palace'
        keys for each first level key. Corresponding values for 'board' and
        'palace' contain lists within a list. The legal moves housed within the
        private data member are dimensional movements in Board. 'board'
        movements do not take into account the diagonal moves within the palace.
        Rather, 'palace' contains diagonal dimensional movements pertaining only
        to the palace.
        """

        return self._legal_moves

    def set_legal_moves(self, legal_moves):
        """
        Takes in legal_moves (dict) and sets _legal_moves to dict for GamePiece. 
        """

        self._legal_moves = legal_moves

    def get_potential_moves(self):
        """
        Takes in no parameters. 
        Returns _potential_moves (list) for GamePiece.
        The list contains positions, for example, 'a2', of all potential moves
        for a given GamePiece based on various rules and guidelines within 
        JanggiGame. 
        """

        return self._potential_moves

    def set_potential_moves(self, potential_moves):
        """
        Takes in potential_moves (list) and sets _potential_moves to the list
        for GamePiece. A list contains positions of all potential moves a given
        GamePiece can make based on methods within JanggiGame. Methods specific
        to each GamePiece will generate positions that are allowable for the
        next move.
        """

        self._potential_moves = potential_moves

    def __repr__(self):
        """
        USED ONLY FOR DEBUGGING
        Official representation of GamePiece. Used to print each GamePiece
        on board for visual representation of the current state of game.
        Takes in no parameters.
        """

        return self.get_label()


class General(GamePiece):
    """
    General inherits all private data members and methods from GamePiece.
    After composed within JanggiGame setup method, General interacts with
    general_guard_generate_potential_moves, generate_moves, is_in_check,
    is_checkmate, and other getter and setter type methods within JanggiGame.
    General's moves are confined to the palace when using 
    general_guard_generate_potential_moves method. Can move within lines of the 
    palace only, which includes diagonally at allowed positions.
    """

    def __init__(self, label, player):
        """
        Takes in label (string) and player (string).
        Inherits from GamePiece and initializes all attributes from parent class
        with super().__init__ method. Sets _legal_moves specific to General's
        movements. _potential_moves is not updated until all GamePieces are
        composed within JanggiGame setup method.
        """

        super().__init__(label, player)
        self.set_legal_moves({\
            'RED': {'board':[[0,-1],[-1,0],[1,0],[0,1]],\
                    'palace':[[-1,-1],[1,-1],[-1,1],[1,1]]},\
            'BLUE':{'board':[[0,-1],[-1,0],[1,0],[0,1]],\
                    'palace':[[-1,-1],[1,-1],[-1,1],[1,1]]}\
                             })


class Guard(GamePiece):
    """
    Guard inherits all private data members and methods from GamePiece.
    After composed within JanggiGame setup method, Guard interacts with
    general_guard_generate_potential_moves, generate_moves, and other getter
    and setter type methods within JanggiGame. Guard's moves are confined to the 
    palace when using general_guard_generate_potential_moves method. Can move
    within lines of the palace only, which includes diagonally at allowed 
    positions.
    """

    def __init__(self, label, player):
        """
        Takes in label (string) and player (string).
        Inherits from GamePiece and initializes all attributes from parent class
        with super().__init__ method. Sets _legal_moves specific to Guard's
        movements. _potential_moves is not updated until all GamePieces are
        composed within JanggiGame setup method.
        """

        super().__init__(label, player)
        self.set_legal_moves({\
            'RED': {'board':[[0,-1],[-1,0],[1,0],[0,1]],\
                    'palace':[[-1,-1],[1,-1],[-1,1],[1,1]]},\
            'BLUE':{'board':[[0,-1],[-1,0],[1,0],[0,1]],\
                    'palace':[[-1,-1],[1,-1],[-1,1],[1,1]]}\
                             })


class Horse(GamePiece):
    """
    Horse inherits all private data members and methods from GamePiece.
    After composed within JanggiGame setup method, Horse interacts with
    horse_generate_potential_moves, generate_moves, and other getter
    and setter type methods within JanggiGame. Horse can move anywhere within
    the boundary of the board: one step orthogonally and one step diagonally 
    in either direction. No restrictions are placed on movement within the
    palace. Palace is non-existent for the Horse.
    """

    def __init__(self, label, player):
        """
        Takes in label (string) and player (string).
        Inherits from GamePiece and initializes all attributes from parent class
        with super().__init__ method. Sets _legal_moves specific to Horse's
        movements: one step orthogonally and one step diagonally in either 
        direction. _potential_moves is not updated until all GamePieces are 
        composed within JanggiGame setup method.
        """
        
        super().__init__(label, player)
        self.set_legal_moves({\
            'RED': {'board':[[0,1,[-1,1],[1,1]],[1,0,[1,1],[1,-1]],[0,-1,[1,-1],[-1,-1]],[-1,0,[-1,-1],[-1,1]]],\
                    'palace':[]},\
            'BLUE':{'board':[[0,1,[-1,1],[1,1]],[1,0,[1,1],[1,-1]],[0,-1,[1,-1],[-1,-1]],[-1,0,[-1,-1],[-1,1]]],\
                    'palace':[]}\
                             })


class Elephant(GamePiece):
    """
    Elephant inherits all private data members and methods from GamePiece.
    After composed within JanggiGame setup method, Elephant interacts with
    elephant_generate_potential_moves, generate_moves, and other getter
    and setter type methods within JanggiGame. Elephant can move anywhere within
    the boundary of the board: one step orthogonally and two steps diagonally
    in either direction. No restrictions are placed on movement within the palace.
    Palace is non-existent for the Elephant.
    """

    def __init__(self, label, player):
        """
        Takes in label (string) and player (string).
        Inherits from GamePiece and initializes all attributes from parent class
        with super().__init__ method. Sets _legal_moves specific to Elephant's
        movements: one step orthogonally and two steps diagonally
        in either direction. _potential_moves is not updated until all 
        GamePieces are composed within JanggiGame setup method.
        """
        
        super().__init__(label, player)
        self.set_legal_moves({\
            'RED': {'board':[[0,1,[-1,1],[1,1]],[1,0,[1,1],[1,-1]],[0,-1,[1,-1],[-1,-1]],[-1,0,[-1,-1],[-1,1]]],\
                    'palace':[]},\
            'BLUE':{'board':[[0,1,[-1,1],[1,1]],[1,0,[1,1],[1,-1]],[0,-1,[1,-1],[-1,-1]],[-1,0,[-1,-1],[-1,1]]],\
                    'palace':[]}\
                             })


class Chariot(GamePiece):
    """
    Chariot inherits all private data members and methods from GamePiece.
    After composed within JanggiGame setup method, Chariot interacts with
    chariot_generate_potential_moves, generate_moves, and other getter
    and setter type methods within JanggiGame. Chariot can move anywhere within
    the boundary of the board: any number of squares orthogonally.
    Restrictions apply to the palace when moving along diagonal lines and only
    apply to the palace and no where else.
    """

    def __init__(self, label, player):
        """
        Takes in label (string) and player (string).
        Inherits from GamePiece and initializes all attributes from parent class
        with super().__init__ method. Sets _legal_moves specific to Chariot's
        movements: any number of squares orthogonally. _potential_moves is not 
        updated until all GamePieces are composed within JanggiGame setup method.
        """

        super().__init__(label, player)
        self.set_legal_moves({\
            'RED': {'board':[[8,0],[-8,0],[0,9],[0,-9]],\
                    'palace':[[-1,-1],[1,-1],[-1,1],[1,1]]},\
            'BLUE':{'board':[[8,0],[-8,0],[0,9],[0,-9]],\
                    'palace':[[-1,-1],[1,-1],[-1,1],[1,1]]}\
                             })


class Cannon(GamePiece):
    """
    Cannon inherits all private data members and methods from GamePiece.
    After composed within JanggiGame setup method, Cannon interacts with
    cannon_generate_potential_moves, generate_moves, and other getter
    and setter type methods within JanggiGame. Cannon can move anywhere within
    the boundary of the board: any number of squares orthogonally with a 
    required screen or jump. The jump is required for a move or capture to be 
    successful. Cannons, of either player, cannot be used for screens or be 
    captured by another cannon. Same movements are allowed in the palace except
    that there must be a GamePiece in the middle column of the palace for the 
    move to be successful.
    """

    def __init__(self, label, player):
        """
        Takes in label (string) and player (string).
        Inherits from GamePiece and initializes all attributes from parent class
        with super().__init__ method. Sets _legal_moves specific to Cannon's
        movements: any number of squares orthogonally with a required screen or
        jump. The screen restriction is further developed in
        cannon_generate_potential_moves. _potential_moves is not updated until 
        all GamePieces are composed within JanggiGame setup method.
        """

        super().__init__(label, player)
        self.set_legal_moves({\
            'RED': {'board':[[8,0],[-8,0],[0,9],[0,-9]],\
                    'palace':[[-1,-1],[1,-1],[-1,1],[1,1]]},\
            'BLUE':{'board':[[8,0],[-8,0],[0,9],[0,-9]],\
                    'palace':[[-1,-1],[1,-1],[-1,1],[1,1]]}\
                             })


class Soldier(GamePiece):
    """
    Soldier inherits all private data members and methods from GamePiece.
    After composed within JanggiGame setup method, Soldier interacts with
    soldier_generate_potential_moves, generate_moves, and other getter and setter
    type methods within JanggiGame. Soldier can move anywhere within
    the boundary of the board: moving forward or sideways one square.
    Restrictions apply to the palace when moving forward along diagonal lines and
    only apply to the palace and no where else.
    """

    def __init__(self, label, player):
        """
        Takes in label (string) and player (string).
        Inherits from GamePiece and initializes all attributes from parent class
        with super().__init__ method. Sets _legal_moves specific to Soldier's
        movements: moving forward or sideways one square. _potential_moves is not 
        updated until all GamePieces are composed within JanggiGame setup method.
        """

        super().__init__(label, player)
        self.set_legal_moves({\
            'RED': {'board':[[-1,0],[1,0],[0,1]],\
                    'palace':[[-1,1],[1,1]]},\
            'BLUE':{'board':[[-1,0],[1,0],[0,-1]],\
                    'palace':[[-1,-1],[1,-1]]}\
                             })

  
class Board(object):
    """
    Board is the parent class for JanggiGame. Board interacts with all other 
    classes: GamePiece, General, Guard, Horse, Elephant, Chariot, Cannon, and
    Soldier. The interaction happens through composition within the JanggiGame.
    Every unqiue method within JanggiGame uses methods within Board. Mainly, 
    any changes needing to be processed to the board – whether through transposing
    or reversing a position, getting GamePiece objects from positions, diagonal
    palace moves, palace moves – happen through an interaction with Board methods.
    
    Board contains private data members, such as board, palace board blue, palace
    board red, palace diagonal blue, palace diagonal red, board columns, board
    rows, general position blue, and general position red. Board is a list of 
    lists with 10 rows and 9 columns each row. GamePiece objects are stored
    within the board based on a position ranging from 'a1' to 'i10' transposed
    into board index format.

    Besides the standard getter and setter methods, there are unqiue methods 
    commonly used within JanggiGame. Is inside palace detects wether a GamePiece's
    position is inside palace. Can move diagonally inside palace detects whether a 
    GamePiece position allows for a diagonal move inside specified palace. 
    Get game piece object at position returns a given GamePiece at a requested
    position. Transpose and reverse position either takes position, for example,
    'a1', and changes it into board indexed formated, for example, '00'; or takes
    a board indexed position, for example, '00', and changes it into a
    non-transposed position, for example, 'a1'.
    """
    
    def __init__(self):
        """
        Initializes Board and takes in no parameters.
        Board contains private data members, such as _board, _palace_board_blue,
        _palace_board_red, _palace_diagonal_blue, _palace_diagonal_red, _board_columns, 
        _board_rows, _general_position_blue, and _general_position_red.

        _palace_board* data members contain all positions within the palace for each
        side of the board that do not allow for diagonal moves.
        _palace_diagonal* data members contain all positions within the palace for
        each side of the board that do allow for diagonal moves.
        _board_columns&_rows are used to transpose and reverse positions. The 
        index for each row or column is used to index into the board.
        _general_positions* for each player are recorded for use with checkmate in
        order to determine quickly the location of each general.

        A setup helper method is used to generate a list of 10 lists with 9 NoneType
        in each list. The result is 10 rows by 9 columns each row.
        """

        self._board = list()
        self._palace_board_blue = ['d9', 'e8', 'e10', 'f9']
        self._palace_board_red = ['d2', 'e1', 'e3', 'f2']
        self._palace_diagonal_blue = ['d8', 'd10', 'e9', 'f8', 'f10']
        self._palace_diagonal_red = ['d1', 'd3', 'e2', 'f1', 'f3']
        self._board_columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        self._board_rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self._general_position_blue = 'e9'
        self._general_position_red = 'e2'

        self.setup_board()

    def setup_board(self):
        """
        Takes in no parameters.
        Used within __init__ method to create a board represented by 10 rows
        and 9 columns. Sets _board to a list of lists. Inputs None at each
        position.
        """

        for row in range(10):

            row_list = list()

            for column in range(9):

                row_list.append(None)

            self._board.append(row_list)

    def get_board(self):
        """
        Takes in no parameters. Returns _board of Board.
        """

        return self._board

    def get_board_coordinates(self):
        """
        USED ONLY FOR DEBUGGING.
        Takes in no parameters. 
        Converts _board and prints out positional data based on list indexing.
        """

        temp_board = copy.deepcopy(self.get_board())
        board_columns = self.get_board_columns()
        board_rows = self.get_board_rows()

        for board_row in board_rows:

            for board_column in board_columns:
            
                index_column, index_row = self.transpose_position(board_column + board_row)
                temp_board[index_row][index_column] = (str(index_row)+str(index_column), board_column + board_row)

        return '\n'.join(map(str, temp_board))

    def get_palace_board_blue(self):
        """
        Takes in no parameters.
        Returns _palace_board_blue of Board, from which horizontal and vertical moves
        can happen. Interacts with is_inside_palace to confirm that a position is
        inside blue palace.
        """

        return self._palace_board_blue

    def get_palace_board_red(self):
        """
        Takes in no parameters.
        Returns _palace_board_red of Board, from which horizontal and vertical moves
        can happen. Interacts with is_inside_palace to confirm that a position is
        inside red palace.
        """

        return self._palace_board_red

    def get_palace_diagonal_blue(self):
        """
        Takes in no parameters.
        Returns _palace_diagonal_blue of Board, from which diagonal moves can happen.
        Interacts with is_inside_palace and can_move_diagonally_inside_palace
        to confirm that a position is inside blue palace and from which positions
        allow diagonal moves.
        """

        return self._palace_diagonal_blue

    def get_palace_diagonal_red(self):
        """
        Takes in no parameters.
        Returns _palace_diagonal_red of Board, from which diagonal moves can happen.
        Interacts with is_inside_palace and can_move_diagonally_inside_palace
        to confirm that a position is inside red palace and from which positions
        allow diagonal moves.
        """

        return self._palace_diagonal_red

    def get_board_columns(self):
        """
        Takes in no parameters.
        Returns _board_columns of Board.
        Interacts with transpose_position and reverse_position for the purpose 
        of producing transposed column index and reversing from column index to
        non-transposed column. Additionally, interacts with is_out_of_bounds to
        determine if a position is out of bounds.
        """

        return self._board_columns

    def get_board_rows(self):
        """
        Takes in no parameters.
        Returns _board_rows of Board.
        Interacts with transpose_position and reverse_position for the purpose 
        of producing transposed row index and reversing from row index to
        non-transposed row. Additionally, interacts with is_out_of_bounds to
        determine if a position is out of bounds.
        """

        return self._board_rows

    def get_general_position_blue(self):
        """
        Takes in no parameters.
        Returns _general_position_blue of Board.
        Interacts with is_in_check and is_checkmate to determine the position
        at which the blue general is located. The position is then used to 
        retrieve GamePiece.
        """

        return self._general_position_blue

    def set_general_position_blue(self, position):
        """
        Takes in position (string) and sets _general_position_blue to it.
        """

        self._general_position_blue = position

    def get_general_position_red(self):
        """
        Takes in no parameters.
        Returns _general_position_red of Board.
        Interacts with is_in_check and is_checkmate to determine the position
        at which the red general is located. The position is then used to 
        retrieve GamePiece.
        """

        return self._general_position_red

    def set_general_position_red(self, position):
        """
        Takes in position (string) and sets _general_position_red to it.
        """

        self._general_position_red = position

    def is_position_inside_palace(self, position):
        """
        Takes in position (string).
        Returns True if position is inside either palace.
        Otherwise returns False.
        Interacts with get_palace_board*/_diagonal* methods.
        """

        return position in self.get_palace_board_blue() or\
               position in self.get_palace_board_red() or\
               position in self.get_palace_diagonal_blue() or\
               position in self.get_palace_diagonal_red()

    def can_move_diagonally_inside_palace(self, position):
        """
        Takes in position (string)
        Returns True if position is located on a position from which diagonal
        moves can happen.
        Otherwise returns False.
        Interacts with general_guard_generate_moves, chariot_generate_moves,
        cannon_generate_moves, and soldier_generate_moves. The purpose of the
        method is to set a Boolean to True in order to iniate a for loop in 
        each of the listed methods. It will generate potential positions based
        on diagonal paths as they relate to the position in a given palace. 
        """

        return position in self.get_palace_diagonal_blue() or\
               position in self.get_palace_diagonal_red()

    def get_game_piece_object_at_position(self, position):
        """
        Takes in position (string).
        Returns GamePiece object at position.
        Interacts with every method in JanggiGame in order to retrieve
        GamePiece object from position.
        """

        column, row = self.transpose_position(position)

        return self.get_board()[int(row)][int(column)]

    def adjust_board(self, game_piece_object, position_to, position_from=str()):
        """
        Takes in game_piece_object (GamePiece), position_from (string), 
        position_to (defaulted to string) and moves the GamePiece to the requested position.
        Adjusting the board is a generic method used for placing GamePieces on
        the board. Used within JanggiGame setup method to initialize GamePieces on
        the board. Interacts with is_checkmate and make_move. is_checkmate uses it
        to switch out the General to a simulated position and make_move moves 
        GamePiece from one position to the next using adjust_board. 
        """

        if position_from == str():

            position_from = position_to

        from_column, from_row = self.transpose_position(position_from)
        to_column, to_row = self.transpose_position(position_to)

        # Adjusts row one to the left for indexing; column is already adjusted.
        self.get_board()[from_row][from_column] = None
        self.get_board()[to_row][to_column] = game_piece_object

    def transpose_position(self, position):
        """
        Takes in position (string) and returns stringed numerical coordinates
        for use with _board (board index format). Used everytime prior to
        accessing _board. Returns column, row as integers. Interacts with all
        unique methods in JanggiGame for specifically accessing _board to 
        adjust and retrieve a GamePiece on _board.
        """

        board_columns = self.get_board_columns()
        column = board_columns.index(position[0])
        row = int(position[1:]) - 1

        return (column, row)

    def reverse_position(self, column, row):
        """
        Takes in column and row (integers), reverses transposed position,
        and returns position as string. Used with is_in_check, is_checkmate,
        and all generate_move methods in JanggiGame. Used mainly for setting
        potential moves for each GamePiece and also to check if a General
        is in check or checkmate.
        """

        board_columns = self.get_board_columns()
        board_rows = self.get_board_rows()
        column = str(board_columns[column])
        row = str(board_rows[row])

        return column + row

    def __repr__(self):
        """
        USED ONLY FOR DEBUGGING
        Takes in no parameters.
        Official represenation of the current state of game.
        """

        # Creates a deep copy of _board and changes all None values to underscores.
        temp_board = copy.deepcopy(self.get_board())

        for row_index, row in enumerate(temp_board):

            for column_index, column in enumerate(row):

                if column is None:

                    row[column_index] = '____' + self.reverse_position(column_index, row_index) + '_____'

        # str() with position is mapped onto each list within _board list,
        # converted to string, and then joined by a nextline character.
        return '\n\n'.join(map(str, temp_board))


class JanggiGame(Board):
    """
    JanggiGame is a subclass to Board and inherits all private data members and
    methods from Board. JanggiGame interacts with all other 
    classes: GamePiece, General, Guard, Horse, Elephant, Chariot, Cannon,
    and Soldier. JanggiGame is where the workhorse of the program is run
    The interaction happens through composition within the setup method.
    Every unqiue method within JanggiGame uses methods within Board. Mainly, 
    any changes needing to be processed to the board – whether through transposing
    or reversing a position, getting GamePiece objects from positions, diagonal
    palace moves, palace moves – happen through an interaction with Board methods.
    
    JanggiGame contains private data members, such as game state and player turn.
    Additionally, the helper setup method instantiates (through composition) all
    GamePieces required for a JanggiGame and then updates potential moves for 
    all GamePieces.

    JanggiGame detects whether a move is valid based on player turn, position 
    input out of bounds, and General is in check or checkmate. It generates 
    moves for all GamePieces and sets each GamePiece with their potential moves
    for next turn. Game state is changed when a player has maneuvered another's
    General into a position of checkmate. 
    """

    def __init__(self):
        """
        Inherits from GamePiece and initializes all attributes from parent class
        with super().__init__ method. Other private data members are _game_state,
        which tracks whether the game has finished with a winner, and _player_turn,
        which tracks player turn throughout game.
    
        A setup helper method is used to instantiate two of each GamePiece and one
        General per player for a total of 26 GamePieces. Each GamePiece is then
        loaded to starting board position. Finally, update potential moves 
        generates all potential moves for every GamePiece on the board and
        stores the potential moves in a list within each GamePiece.
        """

        super().__init__()
        self.setup_janggi_game()
        self._game_state = 'UNFINISHED'
        self._player_turn = 'BLUE'

    def setup_janggi_game(self):
        """
        Used within __init__ method by loading GamePieces onto the board.
        Generates potential moves for each GamePiece and uses set_potential_moves
        method at the end for each GamePiece to set potential moves.
        """

        blue_general = General('blue_general', 'BLUE')
        blue_guard_1 = Guard('blue_guard_1', 'BLUE')
        blue_guard_2 = Guard('blue_guard_2', 'BLUE')

        self.adjust_board(blue_general, 'e9')
        self.adjust_board(blue_guard_1, 'd10',)
        self.adjust_board(blue_guard_2, 'f10',)
        
        blue_horse_1 = Horse('blue_horse_1', 'BLUE')
        blue_horse_2 = Horse('blue_horse_2', 'BLUE')
        blue_elephant_1 = Elephant('blue_elephant_1', 'BLUE')
        blue_elephant_2 = Elephant('blue_elephant_2', 'BLUE')
        blue_chariot_1 = Chariot('blue_chariot_1', 'BLUE')
        blue_chariot_2 = Chariot('blue_chariot_2', 'BLUE')
        blue_cannon_1 = Cannon('blue_cannon_1', 'BLUE')
        blue_cannon_2 = Cannon('blue_cannon_2', 'BLUE')

        self.adjust_board(blue_horse_1, 'c10',)
        self.adjust_board(blue_horse_2, 'h10',)
        self.adjust_board(blue_elephant_1, 'b10',)
        self.adjust_board(blue_elephant_2, 'g10',)
        self.adjust_board(blue_chariot_1, 'a10',)
        self.adjust_board(blue_chariot_2, 'i10',)
        self.adjust_board(blue_cannon_1, 'b8')
        self.adjust_board(blue_cannon_2, 'h8')

        blue_soldier_1 = Soldier('blue_soldier_1', 'BLUE')
        blue_soldier_2 = Soldier('blue_soldier_2', 'BLUE')
        blue_soldier_3 = Soldier('blue_soldier_3', 'BLUE')
        blue_soldier_4 = Soldier('blue_soldier_4', 'BLUE')
        blue_soldier_5 = Soldier('blue_soldier_5', 'BLUE')

        self.adjust_board(blue_soldier_1, 'a7')
        self.adjust_board(blue_soldier_2, 'c7')
        self.adjust_board(blue_soldier_3, 'e7')
        self.adjust_board(blue_soldier_4, 'g7')
        self.adjust_board(blue_soldier_5, 'i7')
   
        red_general = General('red_general', 'RED')
        red_guard_1 = Guard('red_guard_1', 'RED')
        red_guard_2 = Guard('red_guard_2', 'RED')
        
        self.adjust_board(red_general, 'e2')
        self.adjust_board(red_guard_1, 'd1')
        self.adjust_board(red_guard_2, 'f1')

        red_horse_1 = Horse('red_horse_1', 'RED')
        red_horse_2 = Horse('red_horse_2', 'RED')
        red_elephant_1 = Elephant('red_elephant_1', 'RED')
        red_elephant_2 = Elephant('red_elephant_2', 'RED')
        red_chariot_1 = Chariot('red_chariot_1', 'RED')
        red_chariot_2 = Chariot('red_chariot_2', 'RED')
        red_cannon_1 = Cannon('red_cannon_1', 'RED')
        red_cannon_2 = Cannon('red_cannon_2', 'RED')

        self.adjust_board(red_horse_1, 'c1')
        self.adjust_board(red_horse_2, 'h1')
        self.adjust_board(red_elephant_1, 'b1')
        self.adjust_board(red_elephant_2, 'g1')
        self.adjust_board(red_chariot_1, 'a1')
        self.adjust_board(red_chariot_2, 'i1')
        self.adjust_board(red_cannon_1, 'b3')
        self.adjust_board(red_cannon_2, 'h3')

        red_soldier_1 = Soldier('red_soldier_1', 'RED')
        red_soldier_2 = Soldier('red_soldier_2', 'RED')
        red_soldier_3 = Soldier('red_soldier_3', 'RED')
        red_soldier_4 = Soldier('red_soldier_4', 'RED')
        red_soldier_5 = Soldier('red_soldier_5', 'RED')

        self.adjust_board(red_soldier_1, 'a4')
        self.adjust_board(red_soldier_2, 'c4')
        self.adjust_board(red_soldier_3, 'e4')
        self.adjust_board(red_soldier_4, 'g4')
        self.adjust_board(red_soldier_5, 'i4')

        self.update_potential_moves()

    def get_game_state(self):
        """
        Takes in no parameters.
        Returns _game_state of JanggiGame.
        Three possible conditions: 'UNFINISHED', 'RED_WON', & 'BLUE_WON'.
        Interacts with make move to determine if the game is unfinished or has
        already been won.
        """

        return self._game_state

    def set_game_state(self, game_state):
        """
        Takes in game_state (string).
        Three possible conditions: 'UNFINISHED', 'RED_WON', & 'BLUE_WON'.
        Interacts with make move to set the state of the game.
        """

        self._game_state = game_state

    def get_player_turn(self):
        """
        Takes in no parameters.
        Returns _player_turn of JanggiGame.
        Interacts with update_player, make_move, is_in_check, and is_checkmate methods.
        Update_player uses method to simply switch to next player.
        Make moves uses the method to check whether an invalid player has played
        a move when they should not have. The latter two methods use the method
        to determine the opponent from the current player.
        """

        return self._player_turn

    def update_player_turn(self):
        """
        Takes in no parameters.
        Changes _player_turn to next player. 
        Two possible options: 'BLUE' & 'RED'.
        Interacts with make_move when a successful move is detected.
        Upon completion of make_move, player turn is updated by alternating to
        opposite player.
        """

        if self.get_player_turn() != 'BLUE':

            self._player_turn = 'BLUE'

        else:

            self._player_turn = 'RED'

    def get_all_game_pieces_potential_moves(self):
        """
        USED ONLY FOR DEBUGGING
        Takes in no parameters.
        Returns a print out of each GamePiece's potential moves on new lines.
        """

        board = self.get_board()

        for row in board:

            for column in row:

                if column is not None:

                    print(column.get_label(), ': ' , column.get_potential_moves())

    def is_out_of_bounds(self, position_to, position_from):
        """
        Takes in position_to and position_from (strings).
        Returns True if position_to or position_from is out of bounds.
        Otherwiser returns False.
        Interacts with make_move to determine whether either position submitted
        is out of bounds.
        """

        board_columns = self.get_board_columns()
        board_rows = self.get_board_rows()

        # Need column/row ordering to simplify code.
        if position_to[0] not in board_columns or\
           position_to[1:] not in board_rows:

            return True

        elif position_from[0] not in board_columns or\
             position_from[1:] not in board_rows:

            return True

        return False

    def is_in_check(self, player):
        """
        Takes in player (string), either 'blue' or 'red', and returns True if
        player is in check when comparing to the position of the opponent's 
        GamePieces.
        Otherwise returns False.
        Interacts with get_general_position* in order to detect if any potential
        move for any opponent's GamePiece matches. Additionally, method is used
        with make_move in order to determine if a player must make move to 
        ensure General is no in check.
        """

        current_player = player.upper()

        # Gathers current player's General and sets opponent player.
        if current_player == 'BLUE':

            current_player_general_position = self.get_general_position_blue()
            opponent_player = 'RED'

        else:

            current_player_general_position = self.get_general_position_red()
            opponent_player = 'BLUE'

        board = self.get_board()

        # Iterates over every row in the board.
        for board_row in board:

            # Iterates over every column in a row.
            # Either can be None or a GamePiece object.
            for game_piece_object in board_row:

                # If current player's general is in a position that exists
                # within _potential_moves for any opponent GamePiece,
                # returns True; current player's general is in check.
                if game_piece_object is not None:

                    # Check opponent player against GamePiece because the entire method's goal
                    # is to check whether or not a move by current player caused its
                    # General to be in check.
                    if game_piece_object.get_player() == opponent_player:

                        potential_moves = game_piece_object.get_potential_moves()

                        if current_player_general_position in potential_moves:

                            return True

        return False

    def is_checkmate(self):
        """
        Takes in no parameters and returns True if player's General is checkmate
        when comparing to all potential moves for all opponent's GamePieces. 
        Otherwise returns False.
        Interacts with get_general_position* in order to retrieve opponent's 
        General. A list of potential moves for the General and current position
        is copied and compared against potential moves of opponent's GamePieces.
        Matches are removed from the list and when positions are leftover, they
        are compared against Cannon and Chariot's potential moves after a simulated
        move by the General.
        Interacts also with get_game_piece_object_at_position, adjust_board,
        and update_potential_moves in order to simulate moves of the General and
        whether the checkmate is truly a checkmate.
        """

        current_player = self.get_player_turn()

        # Gathers opponent player's General and sets opponent player.
        if current_player == 'BLUE':

            opponent_general_position = self.get_general_position_red()
            opponent_player = 'RED'

        else:

            opponent_general_position = self.get_general_position_blue()
            opponent_player = 'BLUE'

        opponent_general = self.get_game_piece_object_at_position(opponent_general_position)

        potential_moves_for_general = opponent_general.get_potential_moves()
        potential_moves_for_general.append(opponent_general_position)

        board = self.get_board()

        # Iterates over every row in the board.
        for board_row in board:

            # Iterates over every column in a row.
            # Either can be None or a GamePiece object.
            for game_piece_object in board_row:

                # If opponent general is in a position that exists
                # within _potential_moves for any current player's GamePiece,
                # removes position from potential_moves_for_general.
                if game_piece_object is not None:

                    # Check current player against GamePiece because the entire method's goal
                    # is to check opponent General for checkmate based on current player's move.
                    if game_piece_object.get_player() == current_player:

                        for game_piece_potential_move in game_piece_object.get_potential_moves():

                            # Tries to remove potential moves from General's potential moves.
                            try:
                                
                                potential_moves_for_general.remove(game_piece_potential_move)
                            
                            except ValueError:

                                continue

        # List is copied to ensure the iterated list is not mutated.        
        copied_potential_moves_for_general = potential_moves_for_general.copy()

        # Simulates extra General moves. Takes into account Cannon or Chariot's other
        # potential moves if General were to move to its remaining possible moves.
        # For example, blue General position is at 'e9' and red chariot is at 'e6'
        # without any barriers in between. 'e10' would count as a potential
        # move for the blue General; however, only 'e9' and not 'e10' would be listed
        # as potential moves for the red chariot. The blue General would thus not be 
        # in checkmate unless an additional simulation is conducted.
        for move in copied_potential_moves_for_general:

            # Records NoneType from position to which the General will move.
            # Ensures a GamePiece is not accidently removed if there is a bug 
            # somewhere else in the program.
            temp_holder = self.get_game_piece_object_at_position(move)

            # Simulates move for General at new position.
            self.adjust_board(opponent_general, move, opponent_general_position)
            self.update_potential_moves()

            for board_row in board:

                for game_piece_object in board_row:

                    # If opponent general is in a position that exists
                    # within _potential_moves for any current player's GamePiece,
                    # removes position from potential_moves_for_general.
                    if game_piece_object is not None:

                        if game_piece_object.get_player() == current_player\
                           and (isinstance(game_piece_object, Chariot) or isinstance(game_piece_object, Cannon)):

                            # Check current player against GamePiece because the entire method's goal
                            # is to check opponent General for checkmate based on current player's move.
                            for game_piece_potential_move in game_piece_object.get_potential_moves():

                                # Tries to remove potential moves from General's potential moves.
                                try:
                                
                                    potential_moves_for_general.remove(game_piece_potential_move)

                                except ValueError:

                                    continue

            # Returns General to previous position and resets Nonetype at previous position.
            self.adjust_board(opponent_general, opponent_general_position, move)
            self.adjust_board(temp_holder, move)
            self.update_potential_moves()

        return not any(potential_moves_for_general)

    def remains_in_check(self, player, position_to, position_from):
        """
        Takes in current_player, position_to, and position_from (strings) and
        returns True if player's General remains in check even after player makes
        a move. Move is simulated and all GamePieces and potential moves are 
        returned to original state prior to move.
        Otherwise returns False.
        Interacts with get_game_piece_object_at_position, adjust_board,
        update_potential_moves, and is_in_check in order to run simulation and
        determine if current_player is still in check after move.
        """

        game_piece_object = self.get_game_piece_object_at_position(position_from)
        temp_holder = self.get_game_piece_object_at_position(position_to)
        is_in_check = False

        # Simulates move for GamePiece.
        self.adjust_board(game_piece_object, position_to, position_from)
        self.update_potential_moves()

        # Sets positional data for player General if move is simulated for General.
        if player == 'BLUE' and isinstance(game_piece_object, General):

            self.set_general_position_blue(position_to)

        elif player == 'RED' and isinstance(game_piece_object, General):
            
            self.set_general_position_red(position_to)

        # Tests if current_player remains in check even after simuluated move.
        if self.is_in_check(player) is True:

            is_in_check = True

        # Returns board back to original state prior to simulation.
        self.adjust_board(game_piece_object, position_from, position_to)
        self.adjust_board(temp_holder, position_to)
        self.update_potential_moves()

        # Resets positional data for player General if move is simulated for General.
        if player == 'BLUE' and isinstance(game_piece_object, General):

            self.set_general_position_blue(position_from)

        elif player == 'RED' and isinstance(game_piece_object, General):
            
            self.set_general_position_red(position_from)

        # Returns True if check remains.
        if is_in_check is True:

            return True
        # Returns False if check is cleared.
        else:

            return False

    def general_guard_generate_potential_moves(self, position_from):
        """
        Takes in position_from (string). 
        Generates potential moves based on General and Guard GamePiece and 
        starting position. Returns list of generated potential moves, if any move exists.
        Returns empty list if no move exists. Diagonal moves are handled with an 
        iteration over a range of one and simply added to simulated colum and row.
        Interacts with get_game_piece_object_at_position, get_player, get_legal_moves,
        transpose_position, reverse_position, can_move_diagonally_inside_palace. 
        Methods are used to interact with GamePieces to retrieve legal moves and
        player owner. Methods are also used for transposing and reversing positions
        for use with Board and to determine whether GamePiece can be used diagonally
        within a palace.
        """

        game_piece_object = self.get_game_piece_object_at_position(position_from)
        player = game_piece_object.get_player()
        board_moves = game_piece_object.get_legal_moves()[player]['board']
        from_column, from_row = self.transpose_position(position_from)
        all_moves = list()

        for legal_move_column, legal_move_row in board_moves:

            simulated_column = from_column + legal_move_column
            simulated_row = from_row + legal_move_row

            # Sets row boundaries based on player owner.
            if player == 'BLUE':

                blue_palace = simulated_row <= 9 and simulated_row >= 7
                red_palace = None

            elif player == 'RED':

                blue_palace = None
                red_palace = simulated_row <= 2 and simulated_row >= 0

            # Ensures simulated column move is within the boundaies of both palaces.
            if simulated_column <= 5 and simulated_column >= 3:
                
                # Ensures simulated row move is within the boundaries of the palace
                # controlled by player owner. Or-statement ensures NoneType does not 
                # interfer with generating correct potential positions.
                if blue_palace or red_palace:
                    
                    # simulated_game_piece_object may be None at times;
                    # the first if-statement will ensure .get_player() isn't
                    # improperly called on None.
                    move = self.reverse_position(simulated_column, simulated_row)
                    simulated_game_piece_object = self.get_game_piece_object_at_position(move)

                    # Move is legal if no GamePiece occupies position.
                    if simulated_game_piece_object is None:
                    
                        all_moves.append(move)

                    # Move is legal if position is occupied by GamePiece of 
                    # opponent.
                    elif simulated_game_piece_object is not None:

                        if simulated_game_piece_object.get_player() != player:
                            
                            all_moves.append(move)

                        # Simulated move is not legal if position is occupied by
                        # another friendly GamePiece. This is redundant; kept to 
                        # show consistenancy among methods.
                        elif simulated_game_piece_object.get_player() == player:

                            pass

        # Generates a list comprehension based on whether the GamePiece position
        # can move diagonally inside either palace.
        move_diagonally_inside_palace = self.can_move_diagonally_inside_palace(position_from)
        diagonal_moves = [diagonal_move for diagonal_move in game_piece_object.get_legal_moves()[player]['palace'] if move_diagonally_inside_palace is True]

        for legal_move_column, legal_move_row in diagonal_moves:

            simulated_column = from_column + legal_move_column
            simulated_row = from_row + legal_move_row

            # Sets row boundaries based on player owner.
            if player == 'BLUE':

                blue_palace = simulated_row <= 9 and simulated_row >= 7
                red_palace = None

            elif player == 'RED':

                blue_palace = None
                red_palace = simulated_row <= 2 and simulated_row >= 0

            # Ensures simulated column move is within the boundaies of both palaces.
            if simulated_column <= 5 and simulated_column >= 3:
                
                # Ensures simulated row move is within the boundaries of the palace
                # controlled by player owner. Or-statement ensures NoneType does not 
                # interfer with generating correct potential positions.
                if blue_palace or red_palace:
                    
                    # simulated_game_piece_object may be None at times;
                    # the first if-statement will ensure .get_player() isn't
                    # improperly called on None.
                    move = self.reverse_position(simulated_column, simulated_row)
                    simulated_game_piece_object = self.get_game_piece_object_at_position(move)
                    
                    # Move is legal if no GamePiece occupies position.
                    if simulated_game_piece_object is None:
                    
                        all_moves.append(move)

                    # Move is legal if position is occupied by GamePiece of 
                    # opponent.
                    elif simulated_game_piece_object is not None:

                        if simulated_game_piece_object.get_player() != player:
                            
                            all_moves.append(move)

                        # Simulated move is not legal if position is occupied by
                        # another friendly GamePiece. This is redundant; kept to 
                        # show consistenancy among methods.
                        elif simulated_game_piece_object.get_player() == player:

                            pass

        return all_moves

    def chariot_generate_potential_moves(self, position_from):
        """
        Takes in position_from (string). 
        Generates potential moves based on Chariot GamePiece and 
        starting position. Returns list of generated potential moves, if any move exists.
        Returns empty list if no move exists. Diagonal moves are handled with an 
        iteration over a range up to 10 and simply added to simulated colum and row.
        Interacts with get_game_piece_object_at_position, get_player, get_legal_moves,
        transpose_position, reverse_position, can_move_diagonally_inside_palace. 
        Methods are used to interact with GamePieces to retrieve legal moves and
        player owner. Methods are also used for transposing and reversing positions
        for use with Board and to determine whether GamePiece can be used diagonally
        within a palace.
        """

        game_piece_object = self.get_game_piece_object_at_position(position_from)
        player = game_piece_object.get_player()
        board_moves = game_piece_object.get_legal_moves()[player]['board']
        from_column, from_row = self.transpose_position(position_from)
        all_moves = list()

        # Generates all legal moves for the board based on GamePiece.
        for legal_move_column, legal_move_row in board_moves:

            iterate_column, iterate_row = False, False

            # Sets stop; used for determining when to stop appending moves to
            # all_moves
            stop = False

            # Determines direction of simulated moves. Sets range_to_iterate
            # before simulating moves.
            if legal_move_column == 0:
                
                iterate_row = True

                if legal_move_row > 0:

                    range_to_iterate = range(1, legal_move_row+1)

                elif legal_move_row < 0:

                    range_to_iterate = range(-1, legal_move_row-1, -1)

            elif legal_move_row == 0:

                iterate_column = True

                if legal_move_column > 0:

                    range_to_iterate = range(1, legal_move_column+1)

                elif legal_move_column < 0:

                    range_to_iterate = range(-1, legal_move_column-1, -1)

            # Tests whether to simulate moves along the column.
            if iterate_column is True:

                for column in range_to_iterate:
                    
                    simulated_column = from_column + column
                    unchanged_row = from_row + legal_move_row

                    # Ensures simulated move is within boundary of board.
                    if simulated_column <= 8 and simulated_column >= 0:
                        
                        # simulated_game_piece_object may be None at times;
                        # the first if-statement will ensure .get_player() isn't
                        # improperly called on None.
                        move = self.reverse_position(simulated_column, unchanged_row)
                        simulated_game_piece_object = self.get_game_piece_object_at_position(move)

                        # Stop indicates continue to append move to all_moves.
                        if stop is False:   

                            # Move is legal if no GamePiece occupies position.
                            if simulated_game_piece_object is None:

                                all_moves.append(move)

                            # Move is legal if position is occupied by GamePiece of 
                            # opponent.
                            elif simulated_game_piece_object.get_player() != player:
                                
                                all_moves.append(move)
                                stop = True

                            # Simulated move is not legal if position is occupied by
                            # another friendly GamePiece. 
                            elif simulated_game_piece_object.get_player() == player:

                                stop = True

            # Resets stop; used for determining when to stop appending moves to
            # all_moves
            stop = False

            # Tests whether to simulate moves along the row.
            if iterate_row is True:

                for row in range_to_iterate:

                    unchanged_column = from_column + legal_move_column
                    simulated_row = from_row + row

                    # Ensures simulated move is within boundary of board.
                    if simulated_row <= 9 and simulated_row >= 0:

                        # simulated_game_piece_object may be None at times;
                        # the first if statement will ensure .get_player() doesn't
                        # improperly call a method on None.
                        move = self.reverse_position(unchanged_column, simulated_row)
                        simulated_game_piece_object = self.get_game_piece_object_at_position(move)

                        # Stop indicates continue to append move to all_moves.
                        if stop is False:  

                            # Move is legal if no GamePiece occupies position.
                            if simulated_game_piece_object is None:

                                all_moves.append(move)

                            # Move is legal if position is occupied by GamePiece of 
                            # opponent.
                            elif simulated_game_piece_object.get_player() != player:

                                all_moves.append(move)
                                stop = True

                            # Simulated move is not legal if position is occupied by
                            # another friendly GamePiece. 
                            elif simulated_game_piece_object.get_player() == player:

                                stop = True

        # Generates a list comprehension based on whether the GamePiece position
        # can move diagonally inside either palace.
        move_diagonally_inside_palace = self.can_move_diagonally_inside_palace(position_from)
        diagonal_moves = [diagonal_move for diagonal_move in game_piece_object.get_legal_moves()[player]['palace'] if move_diagonally_inside_palace is True]

        # Generates all legal diagonal moves within palace for the GamePiece.
        # Does not generate a list of legal moves if diagonal_moves is empty.
        for legal_move_column, legal_move_row in diagonal_moves:

                simulated_column = from_column
                simulated_row = from_row

                # Resets stop; used for determining when to stop appending moves to
                # all_moves
                stop = False

                for index in range(2):

                    simulated_column += legal_move_column
                    simulated_row += legal_move_row

                    # Ensures simulated column move is within the boundaies of both palaces.
                    if simulated_column <= 5 and simulated_column >= 3:
                
                        # Ensures simulated row move is within the boundaries of both palaces.
                        # Increments are not great enough to jump the gap in rows between palaces, 
                        # which is the reason for the or-statement.
                        if simulated_row <= 9 and simulated_row >= 7 or simulated_row <= 2 and simulated_row >= 0:
                        
                            # simulated_game_piece_object may be None at times;
                            # the first if-statement will ensure .get_player() isn't
                            # improperly called on None.
                            move = self.reverse_position(simulated_column, simulated_row)
                            simulated_game_piece_object = self.get_game_piece_object_at_position(move)
                            
                            # Stop indicates continue to append move to all_moves.
                            if stop is False: 

                                # Move is legal if no GamePiece occupies position.
                                if simulated_game_piece_object is None:
                                    
                                    all_moves.append(move)

                                # Move is legal if position is occupied by GamePiece of 
                                # opponent.
                                elif simulated_game_piece_object.get_player() != player:
                                    
                                    all_moves.append(move)
                                    stop = True

                                # Simulated move is not legal if position is occupied by
                                # another friendly GamePiece. This is redundant; kept to 
                                # show consistenancy among methods.
                                elif simulated_game_piece_object.get_player() == player:

                                    stop = True
                                
        return all_moves

    def cannon_generate_potential_moves(self, position_from):
        """
        Takes in position_from (string). 
        Generates potential moves based on Cannon GamePiece and 
        starting position. Returns list of generated potential moves, if any move exists.
        Returns empty list if no move exists. Diagonal moves are handled with an 
        iteration over a range up to 10 and simply added to simulated colum and row.
        Interacts with get_game_piece_object_at_position, get_player, get_legal_moves,
        transpose_position, reverse_position, can_move_diagonally_inside_palace. 
        Methods are used to interact with GamePieces to retrieve legal moves and
        player owner. Methods are also used for transposing and reversing positions
        for use with Board and to determine whether GamePiece can be used diagonally
        within a palace.
        """

        game_piece_object = self.get_game_piece_object_at_position(position_from)
        player = game_piece_object.get_player()
        board_moves = game_piece_object.get_legal_moves()[player]['board']
        from_column, from_row = self.transpose_position(position_from)
        all_moves = list()

        # Generates all legal moves for the board based on GamePiece.
        for legal_move_column, legal_move_row in board_moves:

            iterate_column, iterate_row = False, False

            # Sets screen and stop; stop is used for determining when to stop
            # appending moves to all_moves.
            screen = False
            stop = False

            # Determines direction of simulated moves. Sets range_to_iterate
            # before simulating moves.
            if legal_move_column == 0:
                
                iterate_row = True

                if legal_move_row > 0:

                    range_to_iterate = range(1, legal_move_row+1)

                elif legal_move_row < 0:

                    range_to_iterate = range(-1, legal_move_row-1, -1)

            elif legal_move_row == 0:

                iterate_column = True

                if legal_move_column > 0:

                    range_to_iterate = range(1, legal_move_column+1)

                elif legal_move_column < 0:

                    range_to_iterate = range(-1, legal_move_column-1, -1)

            # Tests whether to simulate moves along the column.
            if iterate_column is True:

                for column in range_to_iterate:
                    
                    simulated_column = from_column + column
                    unchanged_row = from_row + legal_move_row

                    # Ensures simulated move is within boundary of board.
                    if simulated_column <= 8 and simulated_column >= 0:

                        move = self.reverse_position(simulated_column, unchanged_row)
                        simulated_game_piece_object = self.get_game_piece_object_at_position(move)

                        # Checks if valid screen exists; stop indicates continue to
                        # append move to all_moves.
                        if screen is True and stop is False:

                            # Determines if a GamePiece is present at position.
                            if simulated_game_piece_object is not None:

                                # Checks if the GamePiece is an opponent.
                                if simulated_game_piece_object.get_player() != player:

                                    # Sets stop to True if GamePiece is opponent's Cannon.
                                    # Indicates no more moves will be added to all_moves.
                                    if isinstance(simulated_game_piece_object, Cannon):

                                        stop = True

                                    # Appends move if opponent's GamePiece is anything
                                    # other than the opponent's Cannon.
                                    # Sets stop to True; which indicates no more 
                                    # moves will be added to all_moves.
                                    else:
                                        
                                        all_moves.append(move)
                                        stop = True

                                # Sets stop to True if GamePiece is a friendly capture.
                                # Indicates no more moves will be added to all_moves.
                                elif simulated_game_piece_object.get_player() == player:

                                    stop = True

                            # GamePiece is not present and valid screen exists;
                            # move is appended to all_moves.
                            else:

                                all_moves.append(move)
                                
                        # Checks if screen is legal.
                        elif simulated_game_piece_object is not None:

                            # Sets stop to True if GamePiece is any player's Cannon.
                            # Indicates no moves will be added to all_moves. 
                            if isinstance(simulated_game_piece_object, Cannon):

                                stop = True
                            
                            # Sets screen to True if screen is any GamePiece
                            # aside from a Cannon. Indicates a valid screen exists.
                            screen = True

            # Resets screen and stop; stop is used for determining when to stop
            # appending moves to all_moves.
            screen = False
            stop = False

            # Tests whether to simulate moves along the row.
            if iterate_row is True:

                for row in range_to_iterate:

                    unchanged_column = from_column + legal_move_column
                    simulated_row = from_row + row

                    # Ensures simulated move is within boundary of board.
                    if simulated_row <= 9 and simulated_row >= 0:

                        move = self.reverse_position(unchanged_column, simulated_row)
                        simulated_game_piece_object = self.get_game_piece_object_at_position(move)

                        # Checks if valid screen exists; stop indicates continue to
                        # append move to all_moves.
                        if screen is True and stop is False:

                            # Determines if a GamePiece is present at position.
                            if simulated_game_piece_object is not None:

                                # Checks if the GamePiece is an opponent.
                                if simulated_game_piece_object.get_player() != player:

                                    # Sets stop to True if GamePiece is opponent's Cannon.
                                    # Indicates no more moves will be added to all_moves.
                                    if isinstance(simulated_game_piece_object, Cannon):

                                        stop = True

                                    # Appends move if opponent's GamePiece is anything
                                    # other than the opponent's Cannon.
                                    # Sets stop to True; which indicates no more 
                                    # moves will be added to all_moves.
                                    else:
                                        
                                        all_moves.append(move)
                                        stop = True

                                # Sets stop to True if GamePiece is a friendly capture.
                                # Indicates no more moves will be added to all_moves.
                                elif simulated_game_piece_object.get_player() == player:

                                    stop = True

                            # GamePiece is not present and valid screen exists;
                            # move is appended to all_moves.
                            else:

                                all_moves.append(move)
                                
                        # Checks if screen is legal.
                        elif simulated_game_piece_object is not None:

                            # Sets stop to True if GamePiece is any player's Cannon.
                            # Indicates no moves will be added to all_moves. 
                            if isinstance(simulated_game_piece_object, Cannon):

                                stop = True
                            
                            # Sets screen to True if screen is any GamePiece
                            # aside from a Cannon. Indicates a valid screen exists.
                            screen = True

        # Generates a list comprehension based on whether the GamePiece position
        # can move diagonally inside either palace.
        move_diagonally_inside_palace = self.can_move_diagonally_inside_palace(position_from)
        diagonal_moves = [diagonal_move for diagonal_move in game_piece_object.get_legal_moves()[player]['palace'] if move_diagonally_inside_palace is True]

        # Generates all legal diagonal moves within palace for the GamePiece.
        # Does not generate a list of legal moves if diagonal_moves is empty.
        for legal_move_column, legal_move_row in diagonal_moves:

                simulated_column = from_column
                simulated_row = from_row

                # Resets screen and stop.
                screen = False
                stop = False

                for index in range(2):

                    simulated_column += legal_move_column
                    simulated_row += legal_move_row

                    # Ensures simulated column move is within the boundaies of both palaces.
                    if simulated_column <= 5 and simulated_column >= 3:
                
                        # Ensures simulated row move is within the boundaries of both palaces.
                        # Increments are not great enough to jump the gap in rows between palaces, 
                        # which is the reason for the or-statement.
                        if simulated_row <= 9 and simulated_row >= 7 or simulated_row <= 2 and simulated_row >= 0:
                        
                            move = self.reverse_position(simulated_column, simulated_row)
                            simulated_game_piece_object = self.get_game_piece_object_at_position(move)

                            # Checks if valid screen exists; stop indicates continue to
                            # append move to all_moves.
                            if screen is True and stop is False:

                                # Determines if a GamePiece is present at position.
                                if simulated_game_piece_object is not None:

                                    # Checks if the GamePiece is an opponent.
                                    if simulated_game_piece_object.get_player() != player:

                                        # Sets stop to True if GamePiece is opponent's Cannon.
                                        # Indicates no more moves will be added to all_moves.
                                        if isinstance(simulated_game_piece_object, Cannon):

                                            stop = True

                                        # Appends move if opponent's GamePiece is anything
                                        # other than the opponent's Cannon.
                                        # Sets stop to True; which indicates no more 
                                        # moves will be added to all_moves.
                                        else:
                                            
                                            all_moves.append(move)
                                            stop = True

                                    # Sets stop to True if GamePiece is a friendly capture.
                                    # Indicates no more moves will be added to all_moves.
                                    elif simulated_game_piece_object.get_player() == player:

                                        stop = True

                                # GamePiece is not present and valid screen exists;
                                # move is appended to all_moves.
                                else:

                                    all_moves.append(move)
                                    
                            # Checks if screen is legal.
                            elif simulated_game_piece_object is not None:

                                # Sets stop to True if GamePiece is any player's Cannon.
                                # Indicates no moves will be added to all_moves. 
                                if isinstance(simulated_game_piece_object, Cannon):

                                    stop = True
                                
                                # Sets screen to True if screen is any GamePiece
                                # aside from a Cannon. Indicates a valid screen exists.
                                screen = True
                                
        return all_moves

    def horse_generate_potential_moves(self, position_from):
        """
        Takes in position_from (string). 
        Generates potential moves based on Horse GamePiece and 
        starting position. Returns list of generated potential moves, if any move exists.
        Returns empty list if no move exists. Diagonal moves are handled with an 
        iteration over a range of one and simply added to simulated colum and row.
        Interacts with get_game_piece_object_at_position, get_player, get_legal_moves,
        transpose_position, reverse_position, can_move_diagonally_inside_palace. 
        Methods are used to interact with GamePieces to retrieve legal moves and
        player owner. Methods are also used for transposing and reversing positions
        for use with Board and to determine whether GamePiece can be used diagonally
        within a palace.
        """

        game_piece_object = self.get_game_piece_object_at_position(position_from)
        player = game_piece_object.get_player()
        board_moves = game_piece_object.get_legal_moves()[player]['board']
        from_column, from_row = self.transpose_position(position_from)
        all_moves = list()

        # Generates all legal moves for the board based on GamePiece.
        for movement in board_moves:
            
            # Creates a base position from which to step diagonally after initial step.
            column_step = movement[0] + from_column
            row_step = movement[1] + from_row

            # Ensures simulated step is within boundary of board.
            if column_step <= 8 and column_step >= 0 and row_step <= 9 and row_step >= 0:

                checked_position = self.reverse_position(column_step, row_step)
                simulated_game_piece_object = self.get_game_piece_object_at_position(checked_position)

                # Bypasses if first position checked has a GamePiece in the way.
                if simulated_game_piece_object is None:

                    right_movement = movement[2]
                    left_movement = movement[3]

                    # Sets simulated move to a right diagonal move.
                    simulate_column = column_step + right_movement[0]
                    simulate_row = row_step + right_movement[1]

                    # Ensures simulated diagonal step to the right is within boundary of board.
                    if simulate_column <= 8 and simulate_column >= 0 and simulate_row <= 9 and simulate_row >= 0:

                        checked_position = self.reverse_position(simulate_column, simulate_row)
                        simulated_game_piece_object = self.get_game_piece_object_at_position(checked_position)
                        game_piece_is_present = simulated_game_piece_object is not None

                        # Only two conditions should allow for a position to be added to all_moves.
                        # Either the diagonal move is to capture opponent or there is no GamePiece.
                        if game_piece_is_present:

                            if simulated_game_piece_object.get_player() != player:

                                all_moves.append(self.reverse_position(simulate_column, simulate_row))

                        elif not game_piece_is_present:

                            all_moves.append(self.reverse_position(simulate_column, simulate_row))

                    # Sets simulated move to a right diagonal move.
                    simulate_column = column_step + left_movement[0]
                    simulate_row = row_step + left_movement[1]

                    # Ensures simulated diagonal step to the left is within boundary of board.
                    if simulate_column <= 8 and simulate_column >= 0 and simulate_row <= 9 and simulate_row >= 0:

                        checked_position = self.reverse_position(simulate_column, simulate_row)
                        simulated_game_piece_object = self.get_game_piece_object_at_position(checked_position)
                        game_piece_is_present = simulated_game_piece_object is not None

                        # Only two conditions should allow for a position to be added to all_moves.
                        # Either the diagonal move is to capture opponent or there is no GamePiece.
                        if game_piece_is_present:

                            if simulated_game_piece_object.get_player() != player:

                                all_moves.append(self.reverse_position(simulate_column, simulate_row))

                        elif not game_piece_is_present:

                            all_moves.append(self.reverse_position(simulate_column, simulate_row))

        return all_moves

    def elephant_generate_potential_moves(self, position_from):
        """
        Takes in position_from (string). 
        Generates potential moves based on Elephant GamePiece and 
        starting position. Returns list of generated potential moves, if any move exists.
        Returns empty list if no move exists. Diagonal moves are handled with an 
        iteration over a range of two and simply added to simulated colum and row.
        Interacts with get_game_piece_object_at_position, get_player, get_legal_moves,
        transpose_position, reverse_position, can_move_diagonally_inside_palace. 
        Methods are used to interact with GamePieces to retrieve legal moves and
        player owner. Methods are also used for transposing and reversing positions
        for use with Board and to determine whether GamePiece can be used diagonally
        within a palace.
        """

        game_piece_object = self.get_game_piece_object_at_position(position_from)
        player = game_piece_object.get_player()
        board_moves = game_piece_object.get_legal_moves()[player]['board']
        from_column, from_row = self.transpose_position(position_from)
        all_moves = list()

        # Generates all legal moves for the board based on GamePiece.
        for movement in board_moves:
            column_step = movement[0] + from_column
            row_step = movement[1] + from_row

            # Ensures simulated step is within boundary of board.
            if column_step <= 8 and column_step >= 0 and row_step <= 9 and row_step >= 0:

                checked_position = self.reverse_position(column_step, row_step)
                simulated_game_piece_object = self.get_game_piece_object_at_position(checked_position)

                # Bypasses if first position checked has a GamePiece in the way.
                if simulated_game_piece_object is None:

                    right_movement = movement[2]
                    left_movement = movement[3]

                    # Sets base condition and steps.
                    simulate_column = column_step 
                    simulate_row = row_step
                    stop = False

                    # Simulates two right diagonal positions.
                    for step in range(2):

                        simulate_column += right_movement[0]
                        simulate_row += right_movement[1]

                        # Ensures each simulated diagonal step is within boundary of board.
                        if simulate_column <= 8 and simulate_column >= 0 and simulate_row <= 9 and simulate_row >= 0:

                            checked_position = self.reverse_position(simulate_column, simulate_row)
                            simulated_game_piece_object = self.get_game_piece_object_at_position(checked_position)
                            game_piece_is_present = simulated_game_piece_object is not None

                            # Creates a bypass if GamePiece is present at first diagonal step.
                            if step == 0 and game_piece_is_present:

                                stop = True

                            # Condition requires previous step not to have GamePiece in order to proceed.
                            elif step == 1 and stop is False:

                                # Only two conditions should allow for a position to be added to all_moves.
                                # Either the diagonal move is to capture opponent or there is no GamePiece.
                                if game_piece_is_present:

                                    if simulated_game_piece_object.get_player() != player:

                                        all_moves.append(self.reverse_position(simulate_column, simulate_row))

                                elif not game_piece_is_present:

                                    all_moves.append(self.reverse_position(simulate_column, simulate_row))

                    # Resets base condition and steps.
                    simulate_column = column_step
                    simulate_row = row_step
                    stop = False

                    # Simulates two left diagonal positions.
                    for step in range(2):

                        simulate_column += left_movement[0]
                        simulate_row += left_movement[1]

                        # Ensures each simulated diagonal step is within boundary of board.
                        if simulate_column <= 8 and simulate_column >= 0 and simulate_row <= 9 and simulate_row >= 0:

                            checked_position = self.reverse_position(simulate_column, simulate_row)
                            simulated_game_piece_object = self.get_game_piece_object_at_position(checked_position)
                            game_piece_is_present = simulated_game_piece_object is not None

                            # Creates a bypass if GamePiece is present at first diagonal step.
                            if step == 0 and game_piece_is_present:

                                stop = True

                            # Condition requires previous step not to have GamePiece in order to proceed.
                            elif step == 1 and stop is False:

                                # Only two conditions should allow for a position to be added to all_moves.
                                # Either the diagonal move is to capture opponent or there is no GamePiece.
                                if game_piece_is_present:

                                    if simulated_game_piece_object.get_player() != player:

                                        all_moves.append(self.reverse_position(simulate_column, simulate_row))

                                elif not game_piece_is_present:

                                    all_moves.append(self.reverse_position(simulate_column, simulate_row))

        return all_moves

    def soldier_generate_potential_moves(self, position_from):
        """
        Takes in position_from (string). 
        Generates potential moves based on Soldier GamePiece and 
        starting position. Returns list of generated potential moves, if any move exists.
        Returns empty list if no move exists.
        Interacts with get_game_piece_object_at_position, get_player, get_legal_moves,
        transpose_position, reverse_position, can_move_diagonally_inside_palace. 
        Methods are used to interact with GamePieces to retrieve legal moves and
        player owner. Methods are also used for transposing and reversing positions
        for use with Board and to determine whether GamePiece can be used diagonally
        within a palace.
        """

        game_piece_object = self.get_game_piece_object_at_position(position_from)
        player = game_piece_object.get_player()
        board_moves = game_piece_object.get_legal_moves()[player]['board']
        from_column, from_row = self.transpose_position(position_from)
        all_moves = list()

        for legal_move_column, legal_move_row in board_moves:

            simulated_column = from_column + legal_move_column
            simulated_row = from_row + legal_move_row

            # Ensures simulated column move is within the boundaies of board.
            if simulated_column <= 8 and simulated_column >= 0:

                # Ensures simulated row move is within the boundaries of board.
                if simulated_row <= 9 and simulated_row >= 0:
                    
                    # simulated_game_piece_object may be None at times;
                    # the first if-statement will ensure .get_player() isn't
                    # improperly called on None.
                    move = self.reverse_position(simulated_column, simulated_row)
                    simulated_game_piece_object = self.get_game_piece_object_at_position(move)

                    # Move is legal if no GamePiece occupies position.
                    if simulated_game_piece_object is None:
                    
                        all_moves.append(move)

                    # Move is legal if position is occupied by GamePiece of 
                    # opponent.
                    elif simulated_game_piece_object.get_player() != player:
                            
                        all_moves.append(move)

                    # Simulated move is not legal if position is occupied by
                    # another friendly GamePiece. This is redundant; kept to 
                    # show consistenancy among methods.
                    elif simulated_game_piece_object.get_player() == player:

                        pass

        # Generates a list comprehension based on whether the GamePiece position
        # can move diagonally inside either palace.
        move_diagonally_inside_palace = self.can_move_diagonally_inside_palace(position_from)
        diagonal_moves = [diagonal_move for diagonal_move in game_piece_object.get_legal_moves()[player]['palace'] if move_diagonally_inside_palace is True]

        for legal_move_column, legal_move_row in diagonal_moves:

            simulated_column = from_column + legal_move_column
            simulated_row = from_row + legal_move_row

            # Ensures simulated column move is within the boundaies of both palaces.
            if simulated_column <= 5 and simulated_column >= 3:
                
                # Ensures simulated row move is within the boundaries of both palaces.
                # Increments are not great enough to jump the gap in rows between palaces, 
                # which is the reason for the or-statement.
                if simulated_row <= 9 and simulated_row >= 7 or simulated_row <= 2 and simulated_row >= 0:
                    
                    # simulated_game_piece_object may be None at times;
                    # the first if-statement will ensure .get_player() isn't
                    # improperly called on None.
                    move = self.reverse_position(simulated_column, simulated_row)
                    simulated_game_piece_object = self.get_game_piece_object_at_position(move)

                    # Move is legal if no GamePiece occupies position.
                    if simulated_game_piece_object is None:
                    
                        all_moves.append(move)

                    # Move is legal if position is occupied by GamePiece of 
                    # opponent.
                    elif simulated_game_piece_object.get_player() != player:
                            
                        all_moves.append(move)

                    # Simulated move is not legal if position is occupied by
                    # another friendly GamePiece. This is redundant; kept to 
                    # show consistenancy among methods.
                    elif simulated_game_piece_object.get_player() == player:

                        pass

        return all_moves

    def generate_moves(self, position):
        """
        Takes in position (string).
        Uses all generate_move_methods to generates all potential moves for
        every GamePiece based on sublass. Interacts with General, Guard, Horse,
        Elephant, Chariot, Cannon, and Soldier.
        Retrieves a list of potential moves and returns it. 
        Interacts with update_potential_moves to set potential moves for every
        GamePiece on the board every turn.
        """

        game_piece_object = self.get_game_piece_object_at_position(position)

        if isinstance(game_piece_object, General):

            return self.general_guard_generate_potential_moves(position)

        elif isinstance(game_piece_object, Guard):

            return self.general_guard_generate_potential_moves(position)

        elif isinstance(game_piece_object, Horse):

            return self.horse_generate_potential_moves(position)

        elif isinstance(game_piece_object, Elephant):

            return self.elephant_generate_potential_moves(position)

        elif isinstance(game_piece_object, Chariot):

            return self.chariot_generate_potential_moves(position)

        elif isinstance(game_piece_object, Cannon):

            return self.cannon_generate_potential_moves(position)

        elif isinstance(game_piece_object, Soldier):

            return self.soldier_generate_potential_moves(position)

        return list()

    def update_potential_moves(self):
        """
        Takes in position (string).
        Uses all generate_move_methods to generates all potential moves for
        every GamePiece based on sublass. Interacts with General, Guard, Horse,
        Elephant, Chariot, Cannon, and Soldier.
        Retrieves a list of potential moves and returns it. 
        Interacts with update_potential_moves to set potential moves for every
        GamePiece on the board every turn.
        """

        board = self.get_board()

        for row_index, row in enumerate(board):

            for column_index, column in enumerate(row):

                if column is not None:
                    
                    position = self.reverse_position(column_index, row_index)
                    game_piece_object = self.get_game_piece_object_at_position(position)
                    game_piece_object.set_potential_moves(self.generate_moves(position))

    def legal_move(self, position_to, position_from):
        """
        Takes in position_to and position_from (strings).
        Returns True if move is legal; otherwise, false.
        Determines if move to or from are out of bounds or not within list of 
        potential moves. Implementation is simplier when using generating 
        potential moves for each GamePiece. The methods provide for guard rails
        that won't allow a move to be recorded to potenial moves. Therefore, if
        a position_to isn't in the list of potential moves, then the method
        returns False. Most of the game rules are handled within 
        'generate_potential_moves' specific to each class. Only a few rules are 
        handled within make_move method. However, legal_moves handles whether GamePiece
        move is out of bounds, if current player is in check and move leaves 
        general in check, if move is out of turn, and if move is to capture a
        General.
        Interacts with is_in_check, get_game_piece_object_at_position,
        get_potential_moves, and get_player.
        """

        # Returns False if either position_to or position_from is out of bounds.
        if self.is_out_of_bounds(position_to, position_from) is True:

            return False

        # Return False if position_from does not contain a GamePiece to move.
        game_piece_object = self.get_game_piece_object_at_position(position_from)

        if game_piece_object is not None:

            game_piece_player_owner = game_piece_object.get_player()
            current_player = self.get_player_turn()

            # Returns False if current player does not move out of check on current
            # move or the move causes a check.
            if self.remains_in_check(current_player, position_to, position_from) is True:

                return False

            # Returns True if current player wishes to pass on their move.
            # Any position on the board will suffice, including a General's position.
            # Tested after simulated move to ensure current_player does not remain
            # in check. Bypasses following tests to make allowance for any position.
            if position_to == position_from:

                return True

            else:

                # Returns False if move is out of turn and GamePiece is moved by wrong
                # player.
                if current_player != game_piece_player_owner:

                    return False

                # Returns False if current play is to capture General.
                # Capturing General is not allowed. Goal of game is checkmate.
                if position_to in [self.get_general_position_red(), self.get_general_position_blue()]:

                    return False

                # All JangiGame rules are handled by not allowing potential moves to which
                # a player could move a GamePiece. These rules include elephant and horse
                # being blocked, cannon not having proper screen or jump/capture being another
                # cannon.
                elif position_to not in game_piece_object.get_potential_moves():

                    return False

                return True

        else:

            if position_to == position_from:

                return True

            return False

    def make_move(self, position_from, position_to):
        """
        Takes in position_from and position_to (strings). Make_move is the only
        method that has an ordered input of position_to and position_from.
        All other methods reorder so that the order is position_to and position_from.
        Returns False if inputs are not strings or not two or three characters in length.
        Returns False if game state is not 'UNFINISHED'
        Returns False if move is not legal.
        Returns True if position_from and position_to equal each other (pass).
        Otherwise move is made using adjust_board, captured GamePieces are removed
        from the board by simply replacing the new GamePiece in the position of the
        captured, update potential moves for each GamePiece on Board, test 
        checkmate to determine if game_state out to be changed to player has won, 
        player turn is updated and method returns True. Interacts with get_game_state,
        get_game_piece_object_at_position, legal_move, adjust_board, 
        update_potential_moves, is_checkmate, set_game_state, and update_player_turn.
        """

        # Returns False if position_from or position_to are not an actual position
        # ranging from 'a1' to 'i10' for columns 'a' through 'i' and rows '1' 
        # through '10'.
        if not isinstance(position_to, str) or\
           not isinstance(position_from,str) or\
           len(position_to) > 3 or len(position_to) < 2 or\
           len(position_from) > 3 or len(position_from) < 2:

            return False 

        # Returns False if game has been won.
        elif self.get_game_state() != 'UNFINISHED':

            return False

        position_to = position_to.lower()
        position_from = position_from.lower()
        current_player = self.get_player_turn()

        # Returns False if move is not legal based on Janggi game rules.
        if self.legal_move(position_to, position_from) is not True:

            return False

        # Returns True if current player wishes to pass on their move.
        # Any position on the board will suffice, including a General's position.
        # Tested in legal_move to exit legal_move safely. The second test for pass
        # updates player turn and returns True, so long as the player is not
        # currently in check.
        if position_to == position_from:

            if self.is_in_check(current_player) is True:
            
                return False

            self.update_player_turn()
            return True

        # Move is valid. Adjusted board, update potential moves for all GamePieces,
        # test checkmate (change game_state if True), update player turn, and
        # return True.
        else:

            game_piece_object = self.get_game_piece_object_at_position(position_from)
            self.adjust_board(game_piece_object, position_to, position_from)
            self.update_potential_moves()
            
            # Sets the General's Board position attribute if the position has
            # changed.
            if isinstance(game_piece_object, General):

                if current_player == 'BLUE':

                    self.set_general_position_blue(position_to)

                else:

                    self.set_general_position_red(position_to)

            # Sets game_state to the player who won if checkmate is detected.
            if self.is_checkmate() is True:

                if current_player == 'BLUE':

                    self.set_game_state('BLUE_WON')
                
                else:

                    self.set_game_state('RED_WON')

            self.update_player_turn()
            return True


def main():
    """
    Main function.
    """
    game = JanggiGame()
    move_result = game.make_move('c1', 'e3') #should be False because it's not Red's turn
    print(move_result, False)
    move_result = game.make_move('a7','b7') # should return True
    print(move_result, True)
    blue_in_check = game.is_in_check('blue') #should return False
    print(blue_in_check, False)
    print(game.make_move('a4', 'a5'), True) #should return True
    state = game.get_game_state() #should return UNFINISHED
    print(state, 'UNFINISHED')
    print(game.make_move('b7','b6'), True) #should return True
    print(game.make_move('b3','b6'), False) #should return False because it's an invalid move
    print(game.make_move('a1','a4'), True) #should return True
    print(game.make_move('c7','d7'), True) #should return True
    print(game.make_move('a4','a4'), True) #this will pass the Red's turn and return True


# Tests whether file is ran as script and whether the main function ought be called.
if __name__ == '__main__':

    main()