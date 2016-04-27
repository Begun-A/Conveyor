from openpyxl import load_workbook
from random import random

ANSWERS = [True, False, None]
WEIGHTS = [6, 3, 1]
NUBER_MINIONS = 102
INSPERCTIONS = 10
BOMBS = []
MINIONS = []
LOG = []
MOTIVATION_REPORT = []
QA_REPORT = []


class Bomb:
    def __init__(self, id, is_broken):
        self.id = id
        self.is_broken = is_broken
        self.minions_stikers = []


class Minion:
    def __init__(self, id):
        self.id = id
    #asynchronous
    def check_bomb(self, bomb):
        decision = generate_decision(ANSWERS, WEIGHTS)
        if decision == None:
            bomb.minions_stikers.append({self.id: None})
            return
        if decision:
            answer = bomb.is_broken and 'yes' or 'no'
            bomb.minions_stikers.append({self.id: answer})
            LOG.append((self.id, bomb.id, answer))
        else:
            answer = bomb.is_broken and 'no' or 'yes'
            bomb.minions_stikers.append({self.id: answer})
            LOG.append((self.id, bomb.id, answer))

def generate_decision(self, container, weights):
    total_weight = float(sum(weights))
    rel_weight = [w / total_weight for w in weights]

    # Probability for each element
    probs = [sum(rel_weight[:i + 1]) for i in range(len(rel_weight))]

    for (i, element) in enumerate(container):
        if random() <= probs[i]:
            break

    return element


def run_conveyor():
    count = 0
    while count <= len(BOMBS) / NUBER_MINIONS:
        tape = BOMBS[NUBER_MINIONS * count:NUBER_MINIONS * (count + 1)]
        for check in xrange(INSPERCTIONS):
            for i in xrange(len(tape)):
                MINIONS[i - check].check_bomb(tape[i])
        count += 1


def create_minions():
    for i in range(NUBER_MINIONS):
        MINIONS.append(Minion(i))


def get_bombs():
    pass


def generate_reports():
    pass

def write_xlsx():
    pass


if __name__ == '__main__':
    create_minions()
    get_bombs()
    run_conveyor()
    generate_reports()
    write_xlsx()
