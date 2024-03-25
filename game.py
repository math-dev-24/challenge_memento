from term_printer import Color, Color256, ColorRGB, Format, cprint, StdText


class Game:
    def __init__(self, config):
        self.config = config
        self.level: int = 10

    @staticmethod
    def msg_warning(text: str):
        cprint(StdText(f'🚨 - {text}', Color.BRIGHT_RED))

    @staticmethod
    def msg_ok(text: str):
        cprint(StdText(f'✅️ - {text} ', Color.BRIGHT_GREEN))

    @staticmethod
    def msg_info(text: str):
        cprint(StdText(f'ℹ️ - {text} ', Color.BRIGHT_BLUE))

    def init_game(self):
        choice_level: bool = False
        q_level: int = len(self.config['level'])
        while not choice_level:
            cprint('Niveaux disponibles :', attrs=[Format.UNDERLINE, Format.BOLD, Color.MAGENTA])
            for index, grid in enumerate(self.config['level']):
                cprint(f"Niveau {index + 1} : {grid} x {grid}", attrs=[Color.BRIGHT_GREEN])
            choice = input(f"niveau > ")
            try:
                self.level = int(choice)
                if q_level >= self.level > 0:
                    choice_level = True
                    # test
                    self.msg_ok("C'est partie !")
                    self.msg_info("Pour information")
                else:
                    self.msg_warning(f"Le niveau doit être compris entre 1 et {q_level}")
            except:
                self.msg_warning('Doit être un nombre !')