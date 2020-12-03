import random


class Cromosoma:
    def __init__(self):
        pass


class BitCromosoma(Cromosoma):
    def __init__(self, length):
        self.length = length
        self.gen_rand()

    def gen_rand(self):
        self.gen = [random.randrange(2) for i in range(self.length)]

    def __str__(self):
        return ''.join([str(i) for i in self.gen])

#Esta parte es para hacer pruebas
if __name__ == '__main__':
    b = BitCromosoma(length=8)
    print(b)
