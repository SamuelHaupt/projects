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
                        