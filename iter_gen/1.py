class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.lingth_list = len(self.list_of_list)
        self.cursor = 0
        self.cursor_in_list = 0
        self.stopped = False
        


    def __iter__(self):
        return self

    def __next__(self):
        if not self.stopped:
            while self.cursor < self.lingth_list:

                if self.cursor_in_list < len(self.list_of_list[self.cursor]):
                    v = self.list_of_list[self.cursor][self.cursor_in_list]
                    self.cursor_in_list += 1
                    return v
                
                self.cursor_in_list = 0
                self.cursor += 1
            self.stopped = True

        raise StopIteration
        
        


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]


    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()