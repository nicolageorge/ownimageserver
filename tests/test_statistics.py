import os
import unittest

from app.lib.statistics_provider import StatisticsProvider


class TestStatistics(unittest.TestCase):
    def test_get_all_info(self):
        stats_provider = StatisticsProvider()
        statistics = stats_provider.get_all_info()
        self.assertTrue('cpu' in statistics)
        self.assertTrue('disk' in statistics)
        self.assertTrue('images' in statistics)
        self.assertTrue('memory' in statistics)
        self.assertTrue('platform' in statistics)


if __name__ == '__main__':
    unittest.main()
