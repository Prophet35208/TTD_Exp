import Tokens as tok


class LL1:
    def __init__(self, terminal_list):
        self.tape = []
        self.terminal_list = terminal_list
        self.error_flag = False
        self.error_msg = ""
        self.next_terminal_index = 0

    def push_in_tape(self, token_list: list):
        token_list.reverse()
        self.tape = self.tape + token_list

    def get_next_terminal(self):
        if self.next_terminal_index >= len(self.terminal_list):
            return None
        return self.terminal_list[self.next_terminal_index]
    
    def run(self):
        self.error_flag = False
        self.error_msg = ""
        self.next_terminal_index = 0
        self.tape = [tok.Program()]

        while len(self.tape) > 0:
            token = self.tape.pop()
            token.execute(self)
            if self.error_flag:
                return 1
        
        return 0
