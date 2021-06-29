import unittest
from JanggiGame import GamePiece, Board, JanggiGame, General, Guard, Horse, Elephant, Chariot, Cannon, Soldier


class JanggiGameTester(unittest.TestCase):
    
    def test_1(self):

        board = Board()
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

        locations_to_test = ['a1', 'a10', 'i1', 'i10', 'd8', 'g4']

        for index, position in enumerate(locations_to_test):
            temp = board.transpose_position(position)
            locations_to_test[index] = temp

        desired_outputs =   [(0,0), (0,9), (8,0), (8,9), (3,7), (6,3)]

        self.assertEqual(locations_to_test, desired_outputs)

    def test_2(self):
        """
        Tests is_position_inside_palace for red.
        """

        board = Board()
        true_1 = board.is_position_inside_palace('d3')
        true_2 = board.is_position_inside_palace('d1')
        true_3 = board.is_position_inside_palace('f1')
        true_4 = board.is_position_inside_palace('f3')

        self.assertEqual([true_1, true_2, true_3, true_4], [True, True, True, True])

    def test_3(self):
        """
        Tests is_position_inside_palace for blue.
        """

        board = Board()
        true_1 = board.is_position_inside_palace('d8')
        true_2 = board.is_position_inside_palace('d10')
        true_3 = board.is_position_inside_palace('f8')
        true_4 = board.is_position_inside_palace('f10')

        self.assertEqual([true_1, true_2, true_3, true_4], [True, True, True, True])

    def test_4(self):
        """
        Tests is_out_of_bounds().
        """

        game = JanggiGame()
        result_1 = game.is_out_of_bounds('d7', 'd8') # False
        result_2 = game.is_out_of_bounds('j10', 'i10') # True
        result_3 = game.is_out_of_bounds('i11', 'i10') # True
        result_4 = game.is_out_of_bounds('i10', 'j10') # True
        result_5 = game.is_out_of_bounds('i10', 'i11') # True

        self.assertEqual([result_1, result_2, result_3, result_4, result_5],\
                         [False, True, True, True, True])

    def test_5(self):
        """
        Tests get_player_turn and update_player_turn.
        """

        game = JanggiGame()
        first_play = game.get_player_turn() # Should be 'BLUE'
        game.update_player_turn()
        second_play = game.get_player_turn() # Should be 'RED'
        game.update_player_turn()
        third_play = game.get_player_turn() # Should be 'BLUE'

        self.assertEqual([first_play, second_play, third_play], ['BLUE', 'RED', 'BLUE'])

    def test_6(self):
        """
        Tests general_guard_generate_potential_moves
        """

        game = JanggiGame()
        red_general_moves = game.general_guard_generate_potential_moves('e2')
        red_guard_moves = game.general_guard_generate_potential_moves('f1')
        blue_general_moves = game.general_guard_generate_potential_moves('e9')
        blue_guard_moves = game.general_guard_generate_potential_moves('d10')

        expected_outputs = [['e1', 'd2', 'f2', 'e3', 'd3', 'f3'],\
                            ['e8', 'd9', 'f9', 'e10', 'd8', 'f8'],\
                            ['d9', 'e10'],['e1', 'f2']]

        self.assertEqual([red_general_moves, blue_general_moves, blue_guard_moves,\
                          red_guard_moves], expected_outputs)

    def test_7(self):
        """
        Tests chariot_generate_potential_moves, not including palace.
        """

        game = JanggiGame()
        red_chariot = Chariot('red_chariot', 'RED')
        game.adjust_board(red_chariot, 'b5')
        moves = game.chariot_generate_potential_moves('b5')

        expected_outputs = ['c5', 'd5', 'e5', 'f5', 'g5', 'h5', 'i5', 'a5', 'b6', 'b7', 'b8', 'b4']

        self.assertEqual(moves, expected_outputs)


    def test_8(self):
        """
        Tests chariot_generate_potential_moves within opponent palace.
        """

        game = JanggiGame()
        red_chariot = Chariot('red_chariot', 'RED')
        game.adjust_board(red_chariot, 'e9')
        moves = game.chariot_generate_potential_moves('e9')

        expected_outputs = ['f9', 'g9', 'h9', 'i9', 'd9', 'c9', 'b9', 'a9', 'e10', 'e8', 'e7', 'd8', 'f8', 'd10', 'f10']

        self.assertEqual(moves, expected_outputs)

    def test_9(self):
        """
        Tests chariot_generate_potential_moves within opponent palace.
        """

        game = JanggiGame()
        red_chariot = Chariot('red_chariot', 'RED')
        game.adjust_board(red_chariot, 'f8')
        moves = game.chariot_generate_potential_moves('f8')

        expected_outputs = ['g8', 'h8', 'e8', 'd8', 'c8', 'b8', 'f9', 'f10', 'f7', 'f6', 'f5', 'f4', 'f3', 'f2', 'e9']

        self.assertEqual(moves, expected_outputs)

    def test_10(self):
        """
        Tests chariot_generate_potential_moves within opponent palace allowing only horizontal and vertical moves.
        """

        game = JanggiGame()
        red_chariot = Chariot('blue_chariot', 'BLUE')
        game.adjust_board(red_chariot, 'f2')
        moves = game.chariot_generate_potential_moves('f2')

        expected_outputs = ['g2', 'h2', 'i2', 'e2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f1']

        self.assertEqual(moves, expected_outputs)        

    def test_11(self):
        """
        Tests general_guard_generate_potential_moves when space available is greater than 1 space.
        """

        game = JanggiGame()
        blue_general = game.get_game_piece_object_at_position('e9')
        game.adjust_board(blue_general,'d10', 'e9')
        blue_general_moves = game.general_guard_generate_potential_moves('d10')

        expected_outputs = ['d9', 'e10', 'e9']

        self.assertEqual(blue_general_moves, expected_outputs)

    def test_12(self):
        """
        Tests general_guard_generate_potential_moves with no diagonals.
        """

        game = JanggiGame()
        blue_general = game.get_game_piece_object_at_position('e9')
        game.adjust_board(blue_general,'d9', 'e9')
        blue_general_moves = game.general_guard_generate_potential_moves('d9')

        expected_outputs = ['d8', 'e9']

        self.assertEqual(blue_general_moves, expected_outputs)

    def test_13(self):
        """
        Tests general_guard_generate_potential_moves with no diagonals.
        """

        game = JanggiGame()
        blue_guard = game.get_game_piece_object_at_position('d10')
        game.adjust_board(blue_guard,'d9', 'd10')
        blue_guard_moves = game.general_guard_generate_potential_moves('d9')

        expected_outputs = ['d8', 'd10']

        self.assertEqual(blue_guard_moves, expected_outputs)

    def test_14(self):
        """
        Tests soldier_generate_potential_moves for soldier GamePiece.
        """

        game = JanggiGame()
        blue_soldier = game.get_game_piece_object_at_position('c7')
        game.adjust_board(blue_soldier, 'd3', 'c7')
        blue_soldier_moves = game.soldier_generate_potential_moves('d3')

        expected_outputs = ['c3', 'e3', 'd2', 'e2']

        self.assertEqual(blue_soldier_moves, expected_outputs)

    def test_15(self):
        """
        Tests soldier_generate_potential_moves for soldier GamePiece.
        Moves in all allowable directions in opponent palace.
        """

        game = JanggiGame()
        red_soldier = game.get_game_piece_object_at_position('c4')
        game.adjust_board(red_soldier, 'e9', 'c4')
        red_soldier_moves = game.soldier_generate_potential_moves('e9')

        expected_outputs = ['d9', 'f9', 'e10', 'd10', 'f10']

        self.assertEqual(red_soldier_moves, expected_outputs)

    def test_16(self):
        """
        Tests soldier_generate_potential_moves for soldier GamePiece.
        Checks moves from 'f' column side of opponent palace.
        """

        game = JanggiGame()
        red_soldier = game.get_game_piece_object_at_position('c4')
        game.adjust_board(red_soldier, 'f9', 'c4')
        red_soldier_moves = game.soldier_generate_potential_moves('f9')

        expected_outputs = ['e9', 'g9', 'f10']

        self.assertEqual(red_soldier_moves, expected_outputs)

    def test_17(self):
        """
        Tests cannon_generate_potential_moves.
        """

        game = JanggiGame()
        blue_cannon_1_moves = game.cannon_generate_potential_moves('b8') # Tests jumping over cannon of opponent.
        blue_cannon = game.get_game_piece_object_at_position('b8')
        game.adjust_board(blue_cannon,'e5', 'b8')
        blue_cannon_2_moves = game.cannon_generate_potential_moves('e5') # Tests jumping over opponent to capture General.
        game.adjust_board(blue_cannon,'d3', 'e5')
        blue_cannon_3_moves = game.cannon_generate_potential_moves('d3') # Tests diagonal jump within palace with capture.
        game.adjust_board(blue_cannon,'e2', 'd3')
        blue_cannon_4_moves = game.cannon_generate_potential_moves('e2') # Tests jump but no captures within palace.

        red_guard = game.get_game_piece_object_at_position('d1')
        game.adjust_board(red_guard,'d2', 'd1')
        red_cannon = game.get_game_piece_object_at_position('b3')
        game.adjust_board(red_cannon,'c2', 'b3')
        red_cannon_1_moves = game.cannon_generate_potential_moves('c2') # Tests horizontal jump but no captures
                                                                       # and vertical jump with capture.

        blue_cannon = game.get_game_piece_object_at_position('h8')
        game.adjust_board(blue_cannon,'g8', 'h8')

        blue_cannon_5_moves = game.cannon_generate_potential_moves('g8') # Tests jumping over friendly with capture.

        expected_outputs = [[], ['e8','e3','e2'], ['f1'], ['e5', 'e6'], ['c5','c6','c7'], ['g6', 'g5','g4']]

        self.assertEqual([blue_cannon_1_moves, blue_cannon_2_moves, blue_cannon_3_moves,\
                          blue_cannon_4_moves, red_cannon_1_moves, blue_cannon_5_moves],\
                          expected_outputs)

    def test_18(self):
        """
        Tests cannon_generate_potential_moves.
        """

        game = JanggiGame()
        blue_soldier = game.get_game_piece_object_at_position('g7')
        game.adjust_board(blue_soldier,'g8', 'g7')
        red_soldier = game.get_game_piece_object_at_position('c4')
        game.adjust_board(red_soldier,'c3', 'c4')
        blue_cannon_moves = game.cannon_generate_potential_moves('b8') # Tests jumping and trying to capture Cannon for both players.

        expected_outputs = [[]]

        self.assertEqual([blue_cannon_moves],\
                          expected_outputs)

    def test_19(self):
        """
        Tests is_in_check for both generals.
        """

        game = JanggiGame()
        red_soldier = game.get_game_piece_object_at_position('c4')
        game.adjust_board(red_soldier, 'd8', 'c4')
        red_soldier.set_potential_moves(game.generate_moves('d8'))
        red_soldier.get_potential_moves()
        game.get_game_piece_object_at_position('e9')
        red = game.is_in_check('red')
        blue = game.is_in_check('blue')

        expected_outputs = [False, True]

        self.assertEqual([red, blue], expected_outputs)

    def test_20(self):
        """
        Tests is_checkmate.
        """

        game = JanggiGame()

        blue_soldier_1 = game.get_game_piece_object_at_position('a7') 
        blue_soldier_2 = game.get_game_piece_object_at_position('c7')
        blue_soldier_3 = game.get_game_piece_object_at_position('e7')
        blue_cannon_1 = game.get_game_piece_object_at_position('b8')
        blue_chariot_2 = game.get_game_piece_object_at_position('i10')

        game.adjust_board(blue_soldier_1, 'c3', 'a7')
        game.adjust_board(blue_soldier_2, 'c2', 'c7')
        game.adjust_board(blue_soldier_3, 'd4', 'e7')
        game.adjust_board(blue_cannon_1, 'e5', 'b8')
        game.adjust_board(blue_chariot_2, 'f4', 'i10')
        game.update_potential_moves()

        result = game.is_checkmate()

        self.assertEqual(result, True)

    def test_21(self):
        """
        Tests horse_elephant_generate_potential_moves.
        """

        game = JanggiGame()
        blue_horse_1 = game.horse_generate_potential_moves('h10')
        blue_horse = game.get_game_piece_object_at_position('h10')
        game.adjust_board(blue_horse, 'f6', 'h10')
        blue_horse_2 = game.horse_generate_potential_moves('f6')
        game.adjust_board(blue_horse, 'e5', 'f6')
        red_horse = game.get_game_piece_object_at_position('c1')
        game.adjust_board(red_horse, 'f6')
        red_horse_1 = game.horse_generate_potential_moves('f6')


        expected_outputs = [['i8', 'g8'], ['e8', 'g8', 'h7', 'h5', 'g4', 'e4', 'd5', 'd7'],\
                                                  ['e8', 'g8', 'h7', 'h5', 'd5', 'd7']]

        self.assertEqual([blue_horse_1, blue_horse_2, red_horse_1], expected_outputs)

    def test_22(self):
        """
        Tests horse_elephant_generate_potential_moves.
        """

        game = JanggiGame()
        blue_elephant_1 = game.elephant_generate_potential_moves('b10')
        blue_elephant = game.get_game_piece_object_at_position('b10')

        game.adjust_board(blue_elephant, 'c5')
        blue_elephant_2 = game.elephant_generate_potential_moves('c5')
        red_soldier = game.get_game_piece_object_at_position('c4')
        game.adjust_board(red_soldier, 'b4', 'c4')
        blue_elephant_3 = game.elephant_generate_potential_moves('c5')


        expected_outputs = [['d7'], ['a8', 'e8', 'f7'], ['a8', 'e8', 'f7', 'e2']]

        self.assertEqual([blue_elephant_1, blue_elephant_2, blue_elephant_3], expected_outputs)

    def test_23(self):
        """
        Tests is_in_check.
        """

        game = JanggiGame()
        blue_elephant = game.get_game_piece_object_at_position('b10')
        game.adjust_board(blue_elephant, 'c5', 'b10')
        red_soldier = game.get_game_piece_object_at_position('c4')
        game.adjust_board(red_soldier, 'b4', 'c4')
        game.update_potential_moves()
        red_result = game.is_in_check('red')
        blue_result = game.is_in_check('blue')

        expected_outputs = [True, False]

        self.assertEqual([red_result, blue_result], expected_outputs)

    def test_24(self):
        """
        Tests is_in_check.
        """

        game = JanggiGame()
        t1 = game.make_move('e9', 'e9')
        t2 = game.make_move('i1', 'i2')
        t3 = game.make_move('e7', 'f7')
        t4 = game.make_move('i2', 'f2')
        t5 = game.make_move('e9', 'f9')
        t6 = game.make_move('f2', 'f2')
        t7 = game.make_move('f7', 'e7')
        t8 = game.is_in_check('blue')

        expected_outputs = [True, True, True, True, True, True, False, False]

        self.assertEqual([t1, t2 ,t3, t4, t5, t6, t7, t8], expected_outputs)

    def test_25(self):
        """
        Tests is_checkmate.
        """

        game = JanggiGame()
        game.make_move('i10','i9')
        game.make_move('g4','g5')
        game.make_move('g7','h7')
        game.make_move('g5', 'g6')
        game.make_move('h8','h6')
        game.make_move('e5','e5')
        game.make_move('i9','f9')
        game.make_move('e5','e5')
        game.make_move('a10','a9')
        game.make_move('e5','e5')
        game.make_move('a9','d9')
        game.make_move('e5','e5')
        game.make_move('h6','e6')
        blue_won = game.get_game_state()

        self.assertEqual(blue_won, 'BLUE_WON')

    def test_26(self):
        """
        Tests cannon with checkmate.
        """

        game = JanggiGame()
        game.make_move('i10','i9')
        game.make_move('g4','g5')
        game.make_move('g7','h7')
        game.make_move('g5', 'g6')
        game.make_move('h8','h6')
        game.make_move('e5','e5')
        game.make_move('i9','f9')
        game.make_move('e5','e5')
        game.make_move('a10','a9')
        game.make_move('e5','e5')
        game.make_move('a9','d9')
        game.make_move('e4','d4')
        game.make_move('h6','e6')
        unfinished = game.get_game_state()
        
        self.assertEqual(unfinished, 'UNFINISHED')

    def test_27(self):
        """
        Tests if put in check.
        """

        game = JanggiGame()
        game.make_move('i10','i9')
        game.make_move('g4','g5')
        game.make_move('g7','h7')
        game.make_move('g5', 'g6')
        game.make_move('h8','h6')
        game.make_move('e5','e5')
        game.make_move('i9','f9')
        game.make_move('e5','e5')
        game.make_move('a10','a9')
        game.make_move('e5','e5')
        game.make_move('a9','d9')
        game.make_move('e4','d4')
        game.make_move('h6','e6')
        result = game.make_move('d4', 'e4')
        
        self.assertEqual(result, False)

    def test_28(self):
        """
        Tests passing turn and switching player turn.
        """

        game = JanggiGame()
        game.make_move('i10','i9')
        game.make_move('g4','g5')
        game.make_move('g7','h7')
        game.make_move('g5', 'g6')
        game.make_move('h8','h6')
        game.make_move('e5','e5')
        game.make_move('i9','f9')
        game.make_move('e5','e5')
        game.make_move('a10','a9')
        game.make_move('e5','e5')
        game.make_move('a9','d9')
        game.make_move('e4','d4')
        game.make_move('h6','e6')
        game.make_move('d4', 'e4')
        game.make_move('d4', 'd5')
        game.make_move('d9', 'd5')
        game.make_move('e2', 'e3')
        result = game.make_move('e2', 'e2')
        player_turn = game.get_player_turn()

        self.assertEqual([result, player_turn], [True, 'RED'])

    def test_29(self):
        """
        Test General trying to leave palace.
        """

        game = JanggiGame()
        game.make_move('i10','i9')
        game.make_move('g4','g5')
        game.make_move('g7','h7')
        game.make_move('g5', 'g6')
        game.make_move('h8','h6')
        game.make_move('e5','e5')
        game.make_move('i9','f9')
        game.make_move('e5','e5')
        game.make_move('a10','a9')
        game.make_move('e5','e5')
        game.make_move('a9','d9')
        game.make_move('e4','d4')
        game.make_move('h6','e6')
        game.make_move('d4', 'e4')
        game.make_move('d4', 'd5')
        game.make_move('d9', 'd5')
        game.make_move('e2', 'e3')
        game.make_move('e2', 'e2')
        result = game.make_move('e3', 'e4')

        self.assertEqual(result, False)

    def test_30(self):
        """
        Test General remaining in check and moving out of check.
        """

        game = JanggiGame()
        game.make_move('i10','i9')
        game.make_move('g4','g5')
        game.make_move('g7','h7')
        game.make_move('g5', 'g6')
        game.make_move('h8','h6')
        game.make_move('e5','e5')
        game.make_move('i9','f9')
        game.make_move('e5','e5')
        game.make_move('a10','a9')
        game.make_move('e5','e5')
        game.make_move('a9','d9')
        game.make_move('e4','d4')
        game.make_move('h6','e6')
        game.make_move('d4', 'e4')
        game.make_move('d4', 'd5')
        game.make_move('d9', 'd5')
        game.make_move('e2', 'e3')
        game.make_move('d5', 'e5')
        check_1 = game.is_in_check('red')
        invalid_move = game.make_move('e3', 'f3')
        check_2 = game.is_in_check('red')
        valid_move = game.make_move('e3', 'd3')

        expected_outputs = [True, False, True, True]

        self.assertEqual([check_1, invalid_move, check_2, valid_move], expected_outputs)

    def test_31(self):
        """
        Test General remaining in check and moving out of check.
        """

        game = JanggiGame()
        game.make_move('i10','i9')
        game.make_move('g4','g5')
        game.make_move('g7','h7')
        game.make_move('g5', 'g6')
        game.make_move('h8','h6')
        game.make_move('e5','e5')
        game.make_move('i9','f9')
        game.make_move('e5','e5')
        game.make_move('a10','a9')
        game.make_move('e5','e5')
        game.make_move('a9','d9')
        game.make_move('e4','d4')
        game.make_move('h6','e6')
        game.make_move('d4', 'e4')
        game.make_move('d4', 'd5')
        game.make_move('d9', 'd5')
        game.make_move('e2', 'e3')
        game.make_move('d5', 'e5')
        game.make_move('e3', 'f3')
        game.make_move('e3', 'd3')
        game.make_move('f9', 'f2')
        is_in_check = game.is_in_check('red')
        valid_move = game.make_move('d3', 'd3')

        expected_outputs = [False, True]

        self.assertEqual([is_in_check, valid_move], expected_outputs)

    def test_32(self):
        """
        Test General remaining in check and moving out of check.
        """

        game = JanggiGame()
        game.make_move('i10','i9')
        game.make_move('g4','g5')
        game.make_move('g7','h7')
        game.make_move('g5', 'g6')
        game.make_move('h8','h6')
        game.make_move('e5','e5')
        game.make_move('i9','f9')
        game.make_move('e5','e5')
        game.make_move('a10','a9')
        game.make_move('e5','e5')
        game.make_move('a9','d9')
        game.make_move('e4','d4')
        game.make_move('h6','e6')
        game.make_move('d4', 'e4')
        game.make_move('d4', 'd5')
        game.make_move('d9', 'd5')
        game.make_move('e2', 'e3')
        game.make_move('d5', 'e5')
        game.make_move('e3', 'f3')
        game.make_move('e3', 'd3')
        game.make_move('f9', 'f3')
        invalid_move = game.make_move('d3', 'd3')
        is_in_check = game.is_in_check('red')
        valid_move = game.make_move('d3', 'd2')

        expected_outputs = [False, True, True]

        self.assertEqual([invalid_move, is_in_check, valid_move], expected_outputs)

    def test_33(self):
        """
        Test General remaining in check and moving out of check.
        """

        game = JanggiGame()
        game.make_move('i10','i9')
        game.make_move('g4','g5')
        game.make_move('g7','h7')
        game.make_move('g5', 'g6')
        game.make_move('h8','h6')
        game.make_move('e5','e5')
        game.make_move('i9','f9')
        game.make_move('e5','e5')
        game.make_move('a10','a9')
        game.make_move('e5','e5')
        game.make_move('a9','d9')
        game.make_move('e4','d4')
        game.make_move('h6','e6')
        game.make_move('d4', 'e4')
        game.make_move('d4', 'd5')
        game.make_move('d9', 'd5')
        game.make_move('e2', 'e3')
        game.make_move('d5', 'e5')
        game.make_move('e3', 'f3')
        game.make_move('e3', 'd3')
        game.make_move('f9', 'f3')
        game.make_move('d3', 'd2')
        game.make_move('c7', 'c6')
        game.make_move('e5','e5')
        game.make_move('c6','c5')
        game.make_move('e5','e5')
        game.make_move('c5','c4')
        game.make_move('e5','e5')
        test_1 = game.make_move('c4','c3')
        test_2 = game.make_move('e5','e5')
        test_3 = game.make_move('c3','c2')
        game_state = game.get_game_state()
        can_move = game.make_move('a4', 'a5')

        expected_outputs = [True, True, True, 'BLUE_WON', False]

        self.assertEqual([test_1, test_2, test_3, game_state, can_move], expected_outputs)

    def test_34(self):
        """
        Test red General checkmate.
        """

        game = JanggiGame()
        game.make_move('i9','i9')
        game.make_move('a1', 'a2')
        game.make_move('i9','i9')
        game.make_move('a2','d2')
        game.make_move('i9','i9')
        game.make_move('i1','i2')
        game.make_move('i9','i9')
        game.make_move('i2','f2')
        game.make_move('i9','i9')
        game.make_move('g4','h4')
        game.make_move('i9','i9')
        game.make_move('h3','h5')
        game.make_move('i9','i9')
        game.make_move('e4','f4')
        game.make_move('i9','i9')
        game.make_move('f4','f5')
        game.make_move('i9','i9')
        game.make_move('f5','g5')
        game.make_move('i9','i9')
        game.make_move('h5','e5')
        result = game.make_move('d10', 'd9')
        game_state = game.get_game_state()

        self.assertEqual([game_state, result], ['RED_WON', False])

    def test_35(self):
        """
        Test red General checkmate.
        """

        game = JanggiGame()
        game.make_move('i9','i9')
        game.make_move('a1','a2')
        game.make_move('i9','i9')
        game.make_move('a2','d2')
        game.make_move('i9','i9')
        game.make_move('i1','i2')
        game.make_move('i9','i9')
        game.make_move('i2','f2')
        game.make_move('i9','i9')
        game.make_move('g4','h4')
        game.make_move('i9','i9')
        game.make_move('h3','h5')
        game.make_move('i9','i9')
        game.make_move('e4','f4')
        game.make_move('i9','i9')
        game.make_move('f4','f5')
        game.make_move('i9','i9')
        game.make_move('f5','g5')
        game.make_move('i9','i9')
        game.make_move('c1','d3')
        game.make_move('i9','i9')
        game.make_move('d3','e5')
        game.make_move('i9','i9')
        game.make_move('e5','d7')
        is_in_check_1 = game.is_in_check('blue')
        game.make_move('e9', 'e10')
        is_in_check_2 = game.is_in_check('blue')
        invalid_move = game.make_move('e10', 'e9')
        game_state = game.get_game_state()

        self.assertEqual([is_in_check_1,is_in_check_2, invalid_move, game_state], [True, False, False, 'UNFINISHED'])


# Tests whether file is ran as script and whether the main function ought be called.
if __name__ == '__main__':

    print()
    unittest.main()








