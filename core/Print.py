from term_printer import Color, Format, cprint


class Message:

    @staticmethod
    def title(text: str):
        cprint(f" {text} ", attrs=[Format.BOLD, Color.BG_MAGENTA])

    @staticmethod
    def warning(text: str):
        cprint(f'🚨 - {text}', attrs=[Color.BRIGHT_RED])

    @staticmethod
    def ok(text: str):
        cprint(f'✅️ - {text} ', attrs=[Color.BRIGHT_GREEN])

    @staticmethod
    def info(text: str):
        cprint(f'ℹ️ - {text} ', attrs=[Color.BRIGHT_BLUE])

    @staticmethod
    def question(text: str):
        cprint(f'{text} ', attrs=[Color.MAGENTA, Format.UNDERLINE])

    @staticmethod
    def msg(text: str):
        print(text)

    @staticmethod
    def win(text: str):
        cprint(f"{text}", attrs=[Color.BG_GREEN, Format.BOLD])
    @staticmethod
    def input():
        return input('🎤️ > ')
