class virtualMemory:
    memory = {}

    @classmethod
    def get(cls):
        return cls.memory

    @classmethod
    def reset(cls):
        cls.memory