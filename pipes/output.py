class Output(object):
        
    def __init__(self, inp, out):
        super(Output, self).__init__()
        self.input_queue = inp
        self.output_queue = out
        return

    def print(self, text, end="\n"):
        print(text, end=end)
        return