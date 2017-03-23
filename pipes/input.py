class Input(object):

    def __init__(self, inp, out):
        super(Input, self).__init__()
        self.input_queue = inp
        self.output_queue = out
        return

    def scan(self):
        inp = input('')
        self.input_queue.append(inp)
        return inp