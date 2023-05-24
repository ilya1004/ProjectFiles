from datetime import datetime
from src.game_engine.player import Player


'''
class Game:
    def __init__(self, player1: Player, player2: Player, mode_id: int, time_start: datetime, is_rated: bool):
        self.player1 = player1
        self.player2 = player2
        self.mode_id = mode_id
        self.time_start = time_start
        self.is_rated = is_rated
        # Инициализация шахматной доски и других параметров игры

    def make_a_move(self, request: dict):
        pass

    def is_game_end(self):
        # возвращает True если последний ход привел к завершению партии
        pass
    def get_winner(self):
        # возвращает объект Player того кто выйграл
        pass
    def get_loser(self):
        # возвращает объект Player того кто проиграл
        pass
    def to_json(self):
        # Преобразование объекта игры в JSON (словарь)
        pass
    def get_id_player_to_move(self):
        # Вовзращает 1 или 2 в зависимости от того, чей ход (1го игрока или 2го)
        pass
'''


def illegal_move() -> None:
    print('Illegal move')


def unavailable_move() -> None:
    print('Not available move')


def incorrect_color() -> None:
    print('It\'s not your piece')


class Game:
    class Figure:

        def __init__(self, color):
            self._color = color

        def get_available_move(self):
            pass

        def cost(self):
            pass

        def color(self):
            return self._color

        def __str__(self):
            pass

    class Void(Figure):

        def __init__(self, color):
            super().__init__(color)

        def __str__(self):
            return '.'

        def cost(self):
            return 0

    class Throne(Figure):
        def __init__(self, color):
            super().__init__(color)

        def __str__(self):
            return 'T'

        def cost(self):
            return 0

    class Pawn(Figure):

        def __init__(self, color):
            super().__init__(color)

        def __str__(self):
            if self._color == 'white':
                return 'p'
            elif self._color == 'black':
                return 'P'
            return '0'

        def cost(self):
            return 1

    class Knight(Figure):
        def __init__(self, color):
            super().__init__(color)

        def __str__(self):
            if self._color == 'white':
                return 'n'
            elif self._color == 'black':
                return 'N'
            return '0'

        def cost(self):
            return 3

    class Bishop(Figure):
        def __init__(self, color):
            super().__init__(color)

        def __str__(self):
            if self._color == 'white':
                return 'b'
            elif self._color == 'black':
                return 'B'
            return '0'

        def cost(self):
            return 3

    class Rook(Figure):
        def __init__(self, color):
            super().__init__(color)

        def __str__(self):
            if self._color == 'white':
                return 'r'
            elif self._color == 'black':
                return 'R'
            return '0'

        def cost(self):
            return 5

    class Queen(Figure):
        def __init__(self, color):
            super().__init__(color)

        def __str__(self):
            if self._color == 'white':
                return 'q'
            elif self._color == 'black':
                return 'Q'
            return '0'

        def cost(self):
            return 9

    class Prince(Figure):
        def __init__(self, color):
            super().__init__(color)

        def __str__(self):
            if self._color == 'white':
                return 'a'
            elif self._color == 'black':
                return 'A'
            return '0'

        def cost(self):
            return 9

    class King(Figure):
        def __init__(self, color):
            super().__init__(color)

        def __str__(self):
            if self._color == 'white':
                return 'k'
            elif self._color == 'black':
                return 'K'
            return '0'

        def cost(self):
            return 0

    def __init__(self, player1: Player, player2: Player, mode_id: int, time_start: datetime, is_rated: bool):
        self.player1 = player1
        self.player2 = player2
        self.mode_id = mode_id
        self.time_start = time_start
        self.is_rated = is_rated

        self._lw_rook = True
        self._rw_rook = True
        self._lb_rook = True
        self._rb_rook = True
        self._w_king = True
        self._b_king = True

        self._count_of_passive_moves = 0
        self._move_number = 1
        self._available_moves = [[(), ((2, 2), (0, 2)), (), (), (), (), ((7, 2), (5, 2)), (), ()], [((0, 2), (0, 3)), ((1, 2), (1, 3)), ((2, 2), (2, 3)), ((3, 2), (3, 3)), ((4, 2), (4, 3)), ((5, 2), (5, 3)), ((6, 2), (6, 3)), ((7, 2), (7, 3)), ((8, 2), (8, 3))], [(), (), (), (), (), (), (), (), ()], [(), (), (), (), (), (), (), (), ()], [(), (), (), (), (), (), (), (), ()], [(), (), (), (), (), (), (), (), ()], [(), (), (), (), (), (), (), (), ()], [((0, 6), (0, 5)), ((1, 6), (1, 5)), ((2, 6), (2, 5)), ((3, 6), (3, 5)), ((4, 6), (4, 5)), ((5, 6), (5, 5)), ((6, 6), (6, 5)), ((7, 6), (7, 5)), ((8, 6), (8, 5))], [(), (), ((1, 6), (3, 6)), (), (), (), (), ((6, 6), (8, 6)), ()]]
        self.board = [
            [self.Rook('black'), self.Knight('black'), self.Bishop('black'), self.Queen('black'), self.King('black'),
             self.Prince('black'), self.Knight('black'), self.Bishop('black'), self.Rook('black')],
            [self.Pawn('black')] * 9,
            [self.Void('')] * 9,
            [self.Void('')] * 9,
            [self.Void(''), self.Void(''), self.Void(''), self.Void(''), self.Throne('gray'), self.Void(''), self.Void(''),
             self.Void(''), self.Void('')],
            [self.Void('')] * 9,
            [self.Void('')] * 9,
            [self.Pawn('white')] * 9,
            [self.Rook('white'), self.Bishop('white'), self.Knight('white'), self.Prince('white'), self.King('white'),
             self.Queen('white'), self.Bishop('white'), self.Knight('white'), self.Rook('white')]
        ]

    def check_move(self, temp_figure_, x_, y_, legal_moves_, for_user) -> bool:
        if self.board[y_][x_].color() == '':
            legal_moves_.append((transform_back_x[x_], transform_back_y[y_])) if for_user \
                else legal_moves_.append((x_, y_))
        elif temp_figure_.color() != self.board[y_][x_].color() != 'gray':
            legal_moves_.append((transform_back_x[x_], transform_back_y[y_])) if for_user \
                else legal_moves_.append((x_, y_))
            return True
        else:
            return True

    def check_prince_move(self, temp_figure_, x_, y_, legal_moves_, for_user) -> bool:
        king_coords = self.find_king(temp_figure_.color())
        if self.board[y_][x_].color() == '':
            legal_moves_.append((transform_back_x[x_], transform_back_y[y_])) if for_user \
                else legal_moves_.append((x_, y_))
        elif self.board[y_][x_].color() == 'gray':
            if temp_figure_.color() == 'white' and not self.throne_is_under_control('black')\
                    and 2 <= king_coords[0] <= 6 and 2 <= king_coords[1] <= 6:
                legal_moves_.append((transform_back_x[x_], transform_back_y[y_])) if for_user \
                    else legal_moves_.append((x_, y_))
            if temp_figure_.color() == 'black' and not self.throne_is_under_control('white') \
                    and 2 <= king_coords[0] <= 6 and 2 <= king_coords[1] <= 6:
                legal_moves_.append((transform_back_x[x_], transform_back_y[y_])) if for_user \
                    else legal_moves_.append((x_, y_))
        elif temp_figure_.color() != self.board[y_][x_].color():
            legal_moves_.append((transform_back_x[x_], transform_back_y[y_])) if for_user \
                else legal_moves_.append((x_, y_))
            return True
        else:
            return True

    def available_move(self, start_x, start_y, for_user=False) -> tuple:
        temp_figure = self.board[start_y][start_x]
        legal_moves = []

        if type(temp_figure) == self.Knight:
            moves = ((1, 2), (2, 1), (-1, -2), (-2, -1), (1, -2), (-1, 2), (2, -1), (-2, 1))
            for dx, dy in moves:
                new_x = start_x + dx
                new_y = start_y + dy
                if -1 < new_x < 9 and -1 < new_y < 9 and \
                        temp_figure.color() != self.board[new_y][new_x].color() != 'gray':
                    if for_user:
                        legal_moves.append((transform_back_x[new_x], transform_back_y[new_y]))
                    else:
                        legal_moves.append((new_x, new_y))

        elif type(temp_figure) == self.Rook:
            for new_x in range(start_x - 1, -1, -1):
                if self.check_move(temp_figure, new_x, start_y, legal_moves, for_user):
                    break
            for new_x in range(start_x + 1, 9):
                if self.check_move(temp_figure, new_x, start_y, legal_moves, for_user):
                    break
            for new_y in range(start_y + 1, 9):
                if self.check_move(temp_figure, start_x, new_y, legal_moves, for_user):
                    break
            for new_y in range(start_y - 1, -1, -1):
                if self.check_move(temp_figure, start_x, new_y, legal_moves, for_user):
                    break

        elif type(temp_figure) == self.Bishop:
            for new_x, new_y in zip(range(start_x + 1, 9), range(start_y + 1, 9)):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x + 1, 9), range(start_y - 1, -1, -1)):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x - 1, -1, -1), range(start_y + 1, 9)):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x - 1, -1, -1), range(start_y - 1, -1, -1)):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break

        elif type(temp_figure) == self.Queen:
            for new_x in range(start_x - 1, -1, -1):
                if self.check_move(temp_figure, new_x, start_y, legal_moves, for_user):
                    break
            for new_x in range(start_x + 1, 9):
                if self.check_move(temp_figure, new_x, start_y, legal_moves, for_user):
                    break
            for new_y in range(start_y + 1, 9):
                if self.check_move(temp_figure, start_x, new_y, legal_moves, for_user):
                    break
            for new_y in range(start_y - 1, -1, -1):
                if self.check_move(temp_figure, start_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x + 1, 9), range(start_y + 1, 9)):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x + 1, 9), range(start_y - 1, -1, -1)):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x - 1, -1, -1), range(start_y + 1, 9)):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x - 1, -1, -1), range(start_y - 1, -1, -1)):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break

        elif type(temp_figure) == self.Prince:
            for new_x in range(start_x - 1, max(start_x - 3, -1), -1):
                if self.check_prince_move(temp_figure, new_x, start_y, legal_moves, for_user):
                    break
            for new_x in range(start_x + 1, min(start_x + 3, 9)):
                if self.check_prince_move(temp_figure, new_x, start_y, legal_moves, for_user):
                    break
            for new_y in range(start_y + 1, min(start_y + 3, 9)):
                if self.check_prince_move(temp_figure, start_x, new_y, legal_moves, for_user):
                    break
            for new_y in range(start_y - 1, max(start_y - 3, -1), -1):
                if self.check_prince_move(temp_figure, start_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x + 1, min(start_x + 3, 9)),
                                    range(start_y + 1, min(start_y + 3, 9))):
                if self.check_prince_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x + 1, min(start_x + 3, 9)),
                                    range(start_y - 1, max(start_y - 3, -1), -1)):
                if self.check_prince_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x - 1, max(start_x - 3, -1), -1),
                                    range(start_y + 1, min(start_y + 3, 9))):
                if self.check_prince_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x - 1, max(start_x - 3, -1), -1),
                                    range(start_y - 1, max(start_y - 3, -1), -1)):
                if self.check_prince_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break

        elif type(temp_figure) == self.King:
            moves = ((0, 1), (1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1), (-1, 0), (0, -1))
            for dx, dy in moves:
                new_x = start_x + dx
                new_y = start_y + dy
                if new_x == 4 and new_y == 4:
                    if temp_figure.color() == 'black' and not self.throne_is_under_control('white'):
                        if for_user:
                            legal_moves.append((transform_back_x[new_x], transform_back_y[new_y]))
                        else:
                            legal_moves.append((new_x, new_y))
                    elif temp_figure.color() == 'white' and not self.throne_is_under_control('black'):
                        if for_user:
                            legal_moves.append((transform_back_x[new_x], transform_back_y[new_y]))
                        else:
                            legal_moves.append((new_x, new_y))
                elif -1 < new_x < 9 and -1 < new_y < 9 and \
                    temp_figure.color() != self.board[new_y][new_x].color():
                    if for_user:
                        legal_moves.append((transform_back_x[new_x], transform_back_y[new_y]))
                    else:
                        legal_moves.append((new_x, new_y))
            if temp_figure.color() == 'white':
                if self._w_king:
                    if self._rw_rook and self.board[8][5].color() == '' and \
                            self.board[8][6].color() == '' and self.board[8][7].color() == '':
                        if for_user:
                            legal_moves.append(('g', '1'))
                            legal_moves.append(('h', '1'))
                        else:
                            legal_moves.append((6, 8))
                            legal_moves.append((7, 8))
                    if self._lw_rook and self.board[8][3].color() == '' and \
                            self.board[8][2].color() == '' and self.board[8][1].color() == '':
                        if for_user:
                            legal_moves.append(('c', '1'))
                            legal_moves.append(('b', '1'))
                        else:
                            legal_moves.append((2, 8))
                            legal_moves.append((1, 8))
            elif temp_figure.color() == 'black':
                if self._b_king:
                    if self._rb_rook and self.board[0][5].color() == '' and \
                            self.board[0][6].color() == '' and self.board[9][7].color() == '':
                        if for_user:
                            legal_moves.append(('g', '9'))
                            legal_moves.append(('h', '9'))
                        else:
                            legal_moves.append((6, 0))
                            legal_moves.append((7, 0))
                    if self._lw_rook and self.board[0][3].color() == '' and \
                            self.board[0][2].color() == '' and self.board[0][1].color() == '':
                        if for_user:
                            legal_moves.append(('c', '9'))
                            legal_moves.append(('b', '9'))
                        else:
                            legal_moves.append((2, 0))
                            legal_moves.append((1, 0))

        elif type(temp_figure) == self.Pawn:
            if temp_figure.color() == 'white':
                if self.board[start_y - 1][start_x].color() == '':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x], transform_back_y[start_y - 1]))
                    else:
                        legal_moves.append((start_x, start_y - 1))
                    if start_y == 7 and self.board[start_y - 2][start_x].color() == '':
                        if for_user:
                            legal_moves.append((transform_back_x[start_x], transform_back_y[start_y - 2]))
                        else:
                            legal_moves.append((start_x, start_y - 2))
                if start_x + 1 != 9 and self.board[start_y - 1][start_x + 1].color() == 'black':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x + 1], transform_back_y[start_y - 1]))
                    else:
                        legal_moves.append((start_x + 1, start_y - 1))
                if start_x - 1 != -1 and self.board[start_y - 1][start_x - 1].color() == 'black':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x - 1], transform_back_y[start_y - 1]))
                    else:
                        legal_moves.append((start_x - 1, start_y - 1))
            elif temp_figure.color() == 'black':
                if self.board[start_y + 1][start_x].color() == '':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x], transform_back_y[start_y + 1]))
                    else:
                        legal_moves.append((start_x, start_y + 1))
                    if start_y == 1 and self.board[start_y + 2][start_x].color() == '':
                        if for_user:
                            legal_moves.append((transform_back_x[start_x], transform_back_y[start_y + 2]))
                        else:
                            legal_moves.append((start_x, start_y + 2))
                if start_x + 1 != 9 and self.board[start_y + 1][start_x + 1].color() == 'white':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x + 1], transform_back_y[start_y + 1]))
                    else:
                        legal_moves.append((start_x + 1, start_y + 1))
                if start_x - 1 != -1 and self.board[start_y + 1][start_x - 1].color() == 'white':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x - 1], transform_back_y[start_y + 1]))
                    else:
                        legal_moves.append((start_x - 1, start_y + 1))

        return tuple(legal_moves)

    def throne_is_under_control(self, side):
        anti_side = 'white' if side == 'black' else 'black'
        y = 4
        x = 4
        self.board[y][x] = self.Knight(anti_side)
        for i in range(9):
            for j in range(9):
                if self.board[j][i].color() == side and type(self.board[j][i]) != self.King \
                        and (x, y) in self.available_move(i, j):
                    self.board[y][x] = self.Throne('gray')
                    return True
        self.board[y][x] = self.Throne('gray')
        return False

    def find_prince(self, side):
        for i in range(9):
            for j in range(9):
                if self.board[i][j].color() == side and type(self.board[i][j]) == self.Prince:
                    return j, i
        return -1, -1

    def find_king(self, side):
        for i in range(9):
            for j in range(9):
                if self.board[i][j].color() == side and type(self.board[i][j]) == self.King:
                    return j, i
        return -1, -1

    def get_available_moves(self, x, y, for_user=False):
        if for_user:
            return tuple((transform_back_x[m[0]], transform_back_y[m[1]]) for m in self._available_moves[y][x])
        return self._available_moves[y][x]

    def king_is_alive(self, side):
        for i in range(9):
            for j in range(9):
                if type(self.board[i][j]) == self.King and self.board[i][j].color() == side:
                    return True
        return False

    def prince_is_alive(self, side):
        for i in range(9):
            for j in range(9):
                if type(self.board[i][j]) == self.Prince and self.board[i][j].color() == side:
                    return True
        return False

    def show(self) -> None:
        for line in self.board:
            for figure in line:
                print(figure, end=' ')
            print()

    def throne_is_captured(self, side):
        if self.board[4][4].color() == side:
            return True
        return False

    def no_active_moves(self):
        if self._count_of_passive_moves >= 100:
            return True
        return False

    # возвращает True если последний ход привел к завершению партии
    def is_game_end(self) -> bool:
        if self.throne_is_captured('white') or self.throne_is_captured('black') \
                or not self.king_is_alive('white') or not self.king_is_alive('black'):
            return True
        return False

    # возвращает объект Player того кто выйграл
    def get_winner(self) -> Player:
        if self.throne_is_captured('white') or not self.king_is_alive('black'):
            return self.player1
        elif self.throne_is_captured('black') or not self.king_is_alive('white'):
            return self.player2
        return None

    # возвращает объект Player того кто проиграл
    def get_loser(self):
        if self.throne_is_captured('white') or not self.king_is_alive('black'):
            return self.player2
        elif self.throne_is_captured('black') or not self.king_is_alive('white'):
            return self.player1
        return None

    def get_state(self) -> dict:
        str_game = ''
        for line in self.board:
            for figure in line:
                str_game += figure.__str__()
        return {
            "status": "success",
            "data": str_game,
            "details": "game_is_starting"
        }

    # Вовзращает 1 или 2 в зависимости от того, чей ход (1го игрока или 2го)
    async def get_id_player_to_move(self):
        if self._move_number % 2:
            return 1
        else:
            return 2


    def make_a_move(self, x1, y1, x2, y2) -> int:

        color_move = 'white' if self._move_number % 2 else 'black'

        if x1 not in transform_x or x2 not in transform_x or y1 not in transform_y or y2 not in transform_y:
            print('Incorrect input')
            return 0

        x1 = transform_x[x1]
        y1 = transform_y[y1]
        x2 = transform_x[x2]
        y2 = transform_y[y2]

        if color_move != self.board[y1][x1].color():
            incorrect_color()
            return 0

        if (x2, y2) in self.get_available_moves(x1, y1):
            if type(self.board[y1][x1]) == self.King:
                if self.board[y1][x1].color() == 'white':
                    self._w_king = 0
                elif self.board[y1][x1].color() == 'black':
                    self._b_king = 0
            elif type(self.board[y1][x1]) == self.Rook:
                if self.board[y1][x1].color() == 'white':
                    if x1 == 8:
                        self._rw_rook = 0
                    elif x1 == 0:
                        self._lw_rook = 0
                elif self.board[y1][x1].color() == 'black':
                    if x1 == 8:
                        self._rb_rook = 0
                    elif x1 == 0:
                        self._lb_rook = 0

            if type(self.board[y1][x1]) == self.King:
                if x2 - x1 > 1:
                    self.board[y2][x2 - 1] = self.board[y2][8]
                    self.board[y2][8] = self.Void('')
                elif x1 - x2 > 1:
                    self.board[y2][x2 + 1] = self.board[y2][0]
                    self.board[y2][0] = self.Void('')

            if type(self.board[y2][x2]) == self.King:
                coords = self.find_prince(self.board[y2][x2].color())
                if coords != (-1, -1):
                    self.board[coords[1]][coords[0]] = self.King(self.board[y2][x2].color())

            if self.board[y2][x2].color() == '':
                self._count_of_passive_moves += 1
            else:
                self._count_of_passive_moves = 0

            self.board[y2][x2] = self.board[y1][x1]
            self.board[y1][x1] = self.Void('')
        else:
            unavailable_move()
            return 0

        if type(self.board[y2][x2]) == self.Pawn:
            if self.board[y2][x2].color() == 'white' and y2 == 0:
                while True:
                    new_piece = input()
                    if new_piece not in transform_white_pawn:
                        print('there is no piece with that name')
                        continue
                    else:
                        if new_piece != 'a' or new_piece == 'a' and not self.prince_is_alive('white'):
                            self.board[y2][x2] = transform_white_pawn[new_piece]
                            break
                        else:
                            print('You prince is alive')
                            continue
            elif self.board[y2][x2].color() == 'black' and y2 == 8:
                while True:
                    new_piece = input()
                    if new_piece not in transform_black_pawn:
                        print('there is no piece with that name')
                        continue
                    else:
                        if new_piece != 'A' or new_piece == 'A' and not self.prince_is_alive('black'):
                            self.board[y2][x2] = transform_black_pawn[new_piece]
                            break
                        else:
                            print('You prince is alive')
                            continue
        self._available_moves = [[self.available_move(k, j) if self.board[j][k].color() in ('white', 'black') else () for k in range(9)] for j in range(9)]
        self._move_number += 1
        return 1


transform_x = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
transform_y = {'1': 8, '2': 7, '3': 6, '4': 5, '5': 4, '6': 3, '7': 2, '8': 1, '9': 0}
transform_back_x = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i'}
transform_back_y = {8: '1', 7: '2', 6: '3', 5: '4', 4: '5', 3: '6', 2: '7', 1: '8', 0: '9'}
transform_white_pawn = {'r': Game.Rook('white'), 'b': Game.Bishop('white'), 'n': Game.Knight('white'),
                        'a': Game.Prince('white'), 'q': Game.Queen('white')}
transform_black_pawn = {'R': Game.Rook('black'), 'B': Game.Bishop('black'), 'N': Game.Knight('black'),
                        'A': Game.Prince('black'), 'Q': Game.Queen('black')}


# board = Game()
# board.show()



# while True:
#     n = int(input())
#     if n == 1:
#         if board.throne_is_captured('white'):
#             print('White captured the throne. White won')
#             break
#         if board.throne_is_captured('black'):
#             print('Black cpatured the throne. Black won')
#             break
#         if not board.king_is_alive('white'):
#             print('White king and prince are dead. Black won')
#             break
#         if not board.king_is_alive('black'):
#             print('Black king and prince are dead. White won')
#             break
#         if board.no_active_moves():
#             print('50 moves have passed without capturing any piece.')
#             break
#         x1, y1, x2, y2 = (i for i in input())
#         res = board.make_a_move(x1, y1, x2, y2)
#     elif n == 2:
#         x1, y1 = (i for i in input())
#         print(board.get_available_moves(transform_x[x1], transform_y[y1], for_user=True))
#     elif n == 4:
#         pass
#     elif n == 5:
#         print(board.board_condition())
#
#     board.show()




