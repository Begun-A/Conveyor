import unittest
from unittest.case import TestCase
import mock

from conveyor import Conveyor, Minion, Bomb


class MinionTest(TestCase):
    """
    Test minions work
    """

    def setUp(self):
        self.minion = Minion(1, (6, 3, 1), MockWorkbookManager('test', 'Bombs'))

    @mock.patch('conveyor.Minion.generate_decision')
    def test_check_bomb(self, mock_generate_decision):
        # test check_bomb minion method

        # bomb is not broken, minions skip bomb
        bomb = Bomb(1, 0)
        mock_generate_decision.return_value = None
        self.minion.check_bomb(bomb)
        self.assertDictEqual(bomb.minions_stickers, {self.minion: None})

        # bomb is broken, minions skip bomb
        bomb = Bomb(1, 1)
        mock_generate_decision.return_value = None
        self.minion.check_bomb(bomb)
        self.assertDictEqual(bomb.minions_stickers, {self.minion: None})

        # bomb is not broken, minion answered true => 'yes'
        bomb = Bomb(1, 0)
        mock_generate_decision.return_value = True
        self.minion.check_bomb(bomb)
        self.assertDictEqual(bomb.minions_stickers, {self.minion: 'yes'})

        # bomb is broken, minion answered true => 'no'
        bomb = Bomb(1, 1)
        mock_generate_decision.return_value = True
        self.minion.check_bomb(bomb)
        self.assertDictEqual(bomb.minions_stickers, {self.minion: 'no'})

        # bomb is not broken, minion answered false => 'no'
        bomb = Bomb(1, 0)
        mock_generate_decision.return_value = False
        self.minion.check_bomb(bomb)
        self.assertDictEqual(bomb.minions_stickers, {self.minion: 'no'})

        # bomb is broken, minion answered false => 'yes'
        bomb = Bomb(1, 1)
        mock_generate_decision.return_value = False
        self.minion.check_bomb(bomb)
        self.assertDictEqual(bomb.minions_stickers, {self.minion: 'yes'})


class TestConveyor(TestCase):
    """
    Test functionality of conveyor
    """

    @mock.patch('conveyor.WorkbookManager')
    def test_run_conveyor(self, mock_wb_manager):
        # test run_conveyor method
        mock_wb_manager.side_effect = MockWorkbookManager
        conveyor = Conveyor(7, (6, 3, 1), 3, 'test.xlsx', 'Bombs')
        conveyor.run_conveyor()
        is_broken_cnt = 0
        for bomb in conveyor.bombs:
            is_broken_cnt += 1 if bomb.is_broken else 0
            # each bomb should be checked by different minions 3 times
            self.assertEqual(len(set(bomb.minions_stickers.keys())), 3)
        self.assertEqual(is_broken_cnt, 5)

    @mock.patch('conveyor.WorkbookManager')
    def test_generate_reports_and_salary(self, mock_wb_manager):
        # test generate_report_and_salary method
        mock_wb_manager.side_effect = MockWorkbookManager
        conveyor = Conveyor(3, (6, 3, 1), 3, 'test.xlsx', 'Bombs')
        # bomb is not broken
        empty_bomb = Bomb(1, 0)
        percents = []
        # 9 bombs with stikers
        for bomb in generate_minions_stikers(conveyor, empty_bomb):
            conveyor.bombs = [bomb]
            conveyor.motivation_report = []
            conveyor.generate_reports_and_salary()
            percents.append(conveyor.percentage_correct)
        number_is_broken = list(zip(*conveyor.qa_report)[1]).count(1)
        self.assertEqual(number_is_broken, 6)
        self.assertEqual(percents.count(100), 3)
        self.assertListEqual(conveyor.motivation_report,
                             [(1, 6, 2, 1), (2, 6, 0, 3), (3, 3, 1, 5)])
        # bomb is broken
        conveyor = Conveyor(3, (6, 3, 1), 3, 'test.xlsx', 'Bombs')
        empty_bomb = Bomb(1, 1)
        percents = []
        # 9 bombs with stickers
        for bomb in generate_minions_stikers(conveyor, empty_bomb):
            conveyor.bombs = [bomb]
            conveyor.motivation_report = []
            conveyor.generate_reports_and_salary()
            percents.append(conveyor.percentage_correct)
        number_is_broken = list(zip(*conveyor.qa_report)[1]).count(1)
        self.assertEqual(number_is_broken, 6)
        self.assertEqual(percents.count(100), 6)
        self.assertListEqual(conveyor.motivation_report,
                             [(1, 6, 2, 1), (2, 6, 0, 3), (3, 3, 1, 5)])


class MockWorkbookManager:
    def __init__(self, *args):
        return

    def minions_log(self, *args):
        pass

    def get_bombs_data(self):
        for id in range(1, 11):
            is_broken = 0 if id <= 5 else 1
            yield [id, is_broken]


def generate_minions_stikers(conveyor, bomb):
    # function generate minions stikers with different combinations
    answers = ['yes', 'no', None]
    for comb in [[3, 0, 0], [2, 1, 0], [1, 2, 0]]:
        for move in range(3):
            decisions = []
            for i in range(len(answers)):
                decisions.extend([answers[i]] * comb[i])
            comb = comb[2:] + comb[:2]
            bomb.minions_stickers = dict(
                zip(conveyor.minions[:],
                    decisions))
            yield bomb


if __name__ == '__main__':
    unittest.main()
