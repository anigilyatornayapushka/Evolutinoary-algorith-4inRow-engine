class OutOfRangeError(Exception):
    def __init__(self):
        super().__init__('Overflow of one of the board columns.')


class NoLastMoveError(Exception):
    def __init__(self):
        super().__init__('Cannot cancel move if there are none of them.')
