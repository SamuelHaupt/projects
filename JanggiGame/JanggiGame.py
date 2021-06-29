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

                             