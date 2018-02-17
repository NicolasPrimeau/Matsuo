

def compute_haiku_coherence(haiku):
    return 0


class Haiku:

    def __init__(self, lines):
        if len(lines) != 3:
            raise ValueError('Not a haiku')
        self.lines = lines
        self._coherence_score = None

    def __repr__(self):
        return str(self)

    def __str__(self):
        return'\n'.join(self.lines)
