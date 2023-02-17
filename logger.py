class Logger:
    enabled = True

    _print_length = 12

    def print_log(self, msg):
        if self.enabled:
            if isinstance(msg, str):
                self._print_length = len(msg) + 3
                print("[*] " + msg)
            else:
                print("[#] ", end='')
                print(msg)
    
    def set_box(self, start):
        if not self.enabled:
            return
        
        if start:
            print("")
            print("|" + "¯" * self._print_length + "|")
        else:
            print("|" + "_" * self._print_length + "|")