class Interpreter:
    def __init__(self):
        """Command interpreter/parser."""
        pass

    # --- Public Methods ---

    @staticmethod
    def is_command(msg, command_prefix):
        """Return bool based on presence of command prefix."""
        if re.search(f"^{command_prefix}", msg):
            return True
        else:
            return False

    @staticmethod
    def parse_command(msg, command_prefix, commands):
        """
        Parse command in message, return command with arguments[] as dict.
        Raise SyntaxError if command is not valid.
        """
        msg = re.sub(f"^{command_prefix}", "", msg)
        command, args = re.split(" ", msg, maxsplit=1)
        if not command in commands["commands"]:
            raise SyntaxError("Command does not exist.")
        args = re.split(" ", args)
        return {"command": command, "args": args}

