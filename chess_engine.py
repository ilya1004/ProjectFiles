



def illegal_move() -> None:
    print('Illegal move')


def unavailable_move() -> None:
    print('Not available move')


def incorrect_color() -> None:
    print('It\'s not your piece')


class Board:
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

    def __init__(self):
        self._lw_rook = True
        self._rw_rook = True
        self._lb_rook = True
        self._rb_rook = True
        self._w_king = True
        self._b_king = True
        self.__board = [
            [self.Rook('black'), self.Knight('black'), self.Bishop('black'), self.Queen('black'), self.King('black'),
             self.Prince('black'), self.Knight('black'), self.Bishop('black'), self.Rook('black')],
            [self.Pawn('black')] * 9,
            [self.Void('')] * 9,
            [self.Void('')] * 9,
            [self.Void(''), self.Void(''), self.Void(''), self.Void(''), self.Throne(''), self.Void(''), self.Void(''),
             self.Void(''), self.Void('')],
            [self.Void('')] * 9,
            [self.Void('')] * 9,
            [self.Pawn('white')] * 9,
            [self.Rook('white'), self.Bishop('white'), self.Knight('white'), self.Prince('white'), self.King('white'),
             self.Queen('white'), self.Bishop('white'), self.Knight('white'), self.Rook('white')]
        ]

    def check_move(self, temp_figure_, x_, y_, legal_moves_, for_user) -> bool:
        if self.__board[y_][x_].color() == '':
            legal_moves_.append((transform_back_x[x_], transform_back_y[y_])) if for_user \
                else legal_moves_.append((x_, y_))
        elif temp_figure_.color() != self.__board[y_][x_].color():
            legal_moves_.append((transform_back_x[x_], transform_back_y[y_])) if for_user \
                else legal_moves_.append((x_, y_))
            return True
        else:
            return True

    def available_move(self, start_x, start_y, for_user=False) -> tuple:
        temp_figure = self.__board[start_y][start_x]
        legal_moves = []

        if type(temp_figure) == self.Knight:
            moves = ((1, 2), (2, 1), (-1, -2), (-2, -1), (1, -2), (-1, 2), (2, -1), (-2, 1))
            for dx, dy in moves:
                new_x = start_x + dx
                new_y = start_y + dy
                if -1 < new_x < 9 and -1 < new_y < 9 and \
                        temp_figure.color() != self.__board[new_y][new_x].color():
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
                if self.check_move(temp_figure, new_x, start_y, legal_moves, for_user):
                    break
            for new_x in range(start_x + 1, min(start_x + 3, 9)):
                if self.check_move(temp_figure, new_x, start_y, legal_moves, for_user):
                    break
            for new_y in range(start_y + 1, min(start_y + 3, 9)):
                if self.check_move(temp_figure, start_x, new_y, legal_moves, for_user):
                    break
            for new_y in range(start_y - 1, max(start_y - 3, -1), -1):
                if self.check_move(temp_figure, start_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x + 1, min(start_x + 3, 9)),
                                    range(start_y + 1, min(start_y + 3, 9))):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x + 1, min(start_x + 3, 9)),
                                    range(start_y - 1, max(start_y - 3, -1), -1)):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x - 1, max(start_x - 3, -1), -1),
                                    range(start_y + 1, min(start_y + 3, 9))):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break
            for new_x, new_y in zip(range(start_x - 1, max(start_x - 3, -1), -1),
                                    range(start_y - 1, max(start_y - 3, -1), -1)):
                if self.check_move(temp_figure, new_x, new_y, legal_moves, for_user):
                    break

        elif type(temp_figure) == self.King:
            moves = ((0, 1), (1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1), (-1, 0), (0, -1))
            for dx, dy in moves:
                new_x = start_x + dx
                new_y = start_y + dy
                if -1 < new_x < 9 and -1 < new_y < 9 and \
                    temp_figure.color() != self.__board[new_y][new_x].color() and \
                        not self.is_under_attack(new_x, new_y):
                    # (self.prince_is_alive(temp_figure.color()) or
                    # (not self.prince_is_alive(temp_figure.color()) and not self.is_under_attack(new_x, new_y))):
                    if for_user:
                        legal_moves.append((transform_back_x[new_x], transform_back_y[new_y]))
                    else:
                        legal_moves.append((new_x, new_y))
            if temp_figure.color() == 'white':
                if self._w_king:
                    if self._rw_rook and self.__board[8][5].color() == '' and \
                            self.__board[8][6].color() == '' and self.__board[8][7].color() == '':
                        if for_user:
                            legal_moves.append(('g', '1'))
                            legal_moves.append(('h', '1'))
                        else:
                            legal_moves.append((6, 8))
                            legal_moves.append((7, 8))
                    if self._lw_rook and self.__board[8][3].color() == '' and \
                            self.__board[8][2].color() == '' and self.__board[8][1].color() == '':
                        if for_user:
                            legal_moves.append(('c', '1'))
                            legal_moves.append(('b', '1'))
                        else:
                            legal_moves.append((2, 8))
                            legal_moves.append((1, 8))
            elif temp_figure.color() == 'black':
                if self._b_king:
                    if self._rb_rook and self.__board[0][5].color() == '' and \
                            self.__board[0][6].color() == '' and self.__board[9][7].color() == '':
                        if for_user:
                            legal_moves.append(('g', '9'))
                            legal_moves.append(('h', '9'))
                        else:
                            legal_moves.append((6, 0))
                            legal_moves.append((7, 0))
                    if self._lw_rook and self.__board[0][3].color() == '' and \
                            self.__board[0][2].color() == '' and self.__board[0][1].color() == '':
                        if for_user:
                            legal_moves.append(('c', '9'))
                            legal_moves.append(('b', '9'))
                        else:
                            legal_moves.append((2, 0))
                            legal_moves.append((1, 0))

        elif type(temp_figure) == self.Pawn:
            if temp_figure.color() == 'white':
                if self.__board[start_y - 1][start_x].color() == '':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x], transform_back_y[start_y - 1]))
                    else:
                        legal_moves.append((start_x, start_y - 1))
                    if start_y == 7 and self.__board[start_y - 2][start_x].color() == '':
                        if for_user:
                            legal_moves.append((transform_back_x[start_x], transform_back_y[start_y - 2]))
                        else:
                            legal_moves.append((start_x, start_y - 2))
                if start_x + 1 != 9 and self.__board[start_y - 1][start_x + 1].color() == 'black':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x + 1], transform_back_y[start_y - 1]))
                    else:
                        legal_moves.append((start_x + 1, start_y - 1))
                if start_x - 1 != -1 and self.__board[start_y - 1][start_x - 1].color() == 'black':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x - 1], transform_back_y[start_y - 1]))
                    else:
                        legal_moves.append((start_x - 1, start_y - 1))
            elif temp_figure.color() == 'black':
                if self.__board[start_y + 1][start_x].color() == '':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x], transform_back_y[start_y + 1]))
                    else:
                        legal_moves.append((start_x, start_y + 1))
                    if start_y == 1 and self.__board[start_y + 2][start_x].color() == '':
                        if for_user:
                            legal_moves.append((transform_back_x[start_x], transform_back_y[start_y + 2]))
                        else:
                            legal_moves.append((start_x, start_y + 2))
                if start_x + 1 != 9 and self.__board[start_y + 1][start_x + 1].color() == 'white':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x + 1], transform_back_y[start_y + 1]))
                    else:
                        legal_moves.append((start_x + 1, start_y + 1))
                if start_x - 1 != -1 and self.__board[start_y + 1][start_x - 1].color() == 'white':
                    if for_user:
                        legal_moves.append((transform_back_x[start_x - 1], transform_back_y[start_y + 1]))
                    else:
                        legal_moves.append((start_x - 1, start_y + 1))

        return tuple(legal_moves)

    def is_under_attack(self, start_x, start_y) -> bool:
        if self.__board[start_y][start_x].color() == 'white':
            for i in range(9):
                for j in range(9):
                    if (start_x, start_y) in self.available_move(i, j):
                        return True
            return False
        elif self.__board[start_y][start_x].color() == 'black':
            for i in range(9):
                for j in range(9):
                    if (start_x, start_y) in self.available_move(i, j):
                        return True
            return False
        return False

    def king_is_alive(self, side):
        for i in range(9):
            for j in range(9):
                if type(self.__board[i][j]) == self.King and self.__board[i][j].color() == side:
                    return True
        return False

    def prince_is_alive(self, side):
        for i in range(9):
            for j in range(9):
                if type(self.__board[i][j]) == self.Prince and self.__board[i][j].color() == side:
                    return True
        return False

    def find_piece(self, kind, side):
        for i in range(9):
            for j in range(9):
                if type(self.__board[i][j]) == kind and self.__board[i][j].color() == side:
                    return j, i
        return -1, -1

    def show(self) -> None:
        for line in self.__board:
            for figure in line:
                print(figure, end=' ')
            print()

    def white_capture_throne(self, color_move):
        x, y = self.find_piece(self.King, 'white')
        if color_move == 'white' and self.__board[4][4].color() == 'white' and \
            not self.is_under_attack(4, 4) and ((type(self.__board[4][4]) == self.King or
            type(self.__board[4][4]) == self.Prince and 2 <= x <= 6 and 2 <= y <= 6)):
            return True
        return False

    def black_capture_throne(self, color_move):
        x, y = self.find_piece(self.King, 'black')
        if color_move == 'black' and self.__board[4][4].color() == 'black' and \
            not self.is_under_attack(4, 4) and ((type(self.__board[4][4]) == self.King or
            type(self.__board[4][4]) == self.Prince and 2 <= x <= 6 and 2 <= y <= 6)):
            return True
        return False

    def white_declares_mate(self, color_move):
        pass

    def black_declares_mate(self, color_move):
        pass

    def statement(self, color_move):
        for i in range(9):
            for j in range(9):
                if self.__board[i][j].color() == color_move and self.available_move(i, j):
                    return False
        return True

    '''
    0 - ход не сделан
    1 - ход сделан
    2 - белые победили(захват трона)
    3 - черные победили(захват трона)
    4 - белые победили(мат)
    5 - черные победили(мат)
    6 - ничья
    '''
    def make_a_move(self, x1, y1, x2, y2, color_move) -> int:
        if x1 not in transform_x or x2 not in transform_x or y1 not in transform_y or y2 not in transform_y:
            print('Incorrect input')
            return 0

        x1 = transform_x[x1]
        y1 = transform_y[y1]
        x2 = transform_x[x2]
        y2 = transform_y[y2]

        if color_move != self.__board[y1][x1].color():
            incorrect_color()
            return 0

        if (x2, y2) in self.available_move(x1, y1):
            if type(self.__board[y1][x1]) == self.King:
                if self.__board[y1][x1].color() == 'white':
                    self._w_king = 0
                elif self.__board[y1][x1].color() == 'black':
                    self._b_king = 0
            if type(self.__board[y1][x1]) == self.Rook:
                if self.__board[y1][x1].color() == 'white':
                    if x1 == 8:
                        self._rw_rook = 0
                    elif x1 == 0:
                        self._lw_rook = 0
                elif self.__board[y1][x1].color() == 'black':
                    if x1 == 8:
                        self._rb_rook = 0
                    elif x1 == 0:
                        self._lb_rook = 0

            if type(self.__board[y1][x1]) == self.King:
                if x2 - x1 > 1:
                    self.__board[y2][x2 - 1] = self.__board[y2][8]
                    self.__board[y2][8] = self.Void('')
                elif x1 - x2 > 1:
                    self.__board[y2][x2 + 1] = self.__board[y2][0]
                    self.__board[y2][0] = self.Void('')

            if type(self.__board[y2][x2]) == self.King:
                temp = self.find_piece(self.Prince, self.__board[y2][x2].color())
                if temp != (-1, -1):
                    self.__board[temp[1]][temp[0]] = self.King(self.__board[y2][x2].color())

            self.__board[y2][x2] = self.__board[y1][x1]
            self.__board[y1][x1] = self.Void('')
        else:
            unavailable_move()
            return 0

        if type(self.__board[y2][x2]) == self.Pawn:
            if self.__board[y2][x2].color() == 'white' and y2 == 0:
                new_piece = input()
                if new_piece not in transform_white_pawn:
                    illegal_move()
                    return 0
                else:
                    if new_piece != 'a' or new_piece == 'a' and not self.prince_is_alive('white'):
                        self.__board[y2][x2] = transform_white_pawn[new_piece]
                    return 1
            elif self.__board[y2][x2].color() == 'black' and y2 == 8:
                new_piece = input()
                if new_piece not in transform_black_pawn:
                    illegal_move()
                    return 0
                else:
                    if new_piece != 'A' or new_piece == 'A' and not self.prince_is_alive('black'):
                        self.__board[y2][x2] = transform_black_pawn[new_piece]
                    return 1
        return 1


transform_x = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
transform_y = {'1': 8, '2': 7, '3': 6, '4': 5, '5': 4, '6': 3, '7': 2, '8': 1, '9': 0}
transform_back_x = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i'}
transform_back_y = {8: '1', 7: '2', 6: '3', 5: '4', 4: '5', 3: '6', 2: '7', 1: '8', 0: '9'}
transform_white_pawn = {'r': Board.Rook('white'), 'b': Board.Bishop('white'), 'n': Board.Knight('white'),
                        'a': Board.Prince('white'), 'q': Board.Queen('white')}
transform_black_pawn = {'R': Board.Rook('black'), 'B': Board.Bishop('black'), 'N': Board.Knight('black'),
                        'A': Board.Prince('black'), 'Q': Board.Queen('black')}

board = Board()
board.show()

i = 1
while True:
    n = int(input())
    if n == 1:
        try:
            color = 'white' if i % 2 else 'black'
            if board.white_capture_throne(color):
                print('White won')
                break
            if board.black_capture_throne(color):
                print('Black won')
                break
            if board.statement(color):
                print('statement')
                break
            print(board.is_under_attack(4, 8))
            x1, y1, x2, y2 = (i for i in input())
            res = board.make_a_move(x1, y1, x2, y2, color)
            if res == 1:
                i += 1
        except:
            print('Error')
    elif n == 2:
        try:
            x1, y1 = (i for i in input())
            print(board.available_move(transform_x[x1], transform_y[y1], for_user=True))
        except:
            print('Error')
    elif n == 3:
        try:
            x1, y1 = (i for i in input())
            print(board.is_under_attack(transform_x[x1], transform_y[y1]))
        except:
            print('Error')
    board.show()