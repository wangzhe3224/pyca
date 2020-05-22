class Util(object):
    notes = ['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#'] * 2
    notes = [note.upper() for note in notes]

    def chroma(self, x):
        return [i for i in self.notes[self.notes.index(x):] + self.notes[:self.notes.index(x)]] + [x]

    def major(self, x):
        return (self.chroma(x)[:5] + [self.chroma(x)[5]] + self.chroma(x)[5:12])[::2] + [x]

    def major_penta(self, x):
        return [i for idx, i in enumerate(self.major(x)) if idx not in (3, 6)]

    def minor_penta(self, x):
        return (self.major_penta(self.notes[self.notes.index(x) + 3])[:-1] * 2)[-6:]
