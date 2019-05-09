from random import SystemRandom


def random(nfrom, nto):
    secure_rand_gen = SystemRandom()
    return secure_rand_gen.randint(nfrom, nto)

