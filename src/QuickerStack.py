class QuickerStack:
    def __init__(self, initial_size=1):
        self.stack = list([None for _ in range(initial_size)])
        self.size = initial_size
        self.index = -1

    def push(self, item):
        self.index += 1
        self.stack[self.index] = item

    def pop(self):
        result = self.stack[self.index]
        self.index -= 1
        return result

    def __len__(self):
        return self.index + 1
