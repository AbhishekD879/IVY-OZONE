# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_HorseRacingPage(BasePerformanceTest):
    """
    NAME: 'Horse Racing' page performance
    """
    def test_load_horse_racing(self):
        """
        DESCRIPTION: Load 'Horse Racing' page
        EXPECTED: 'Horse Racing' page is loaded
        """
        self.navigate_to_url(url='%s/#/horse-racing' % self.test_hostname)
        self.post_to_influxdb()
