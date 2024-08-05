# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_FootballPage(BasePerformanceTest):
    """
    NAME: 'Football' page performance
    """
    def test_load_Football_page(self):
        """
        DESCRIPTION: Load 'Football' page
        EXPECTED: 'Football' page is loaded
        """
        self.navigate_to_url(url='%s/#/football' % self.test_hostname)
        self.post_to_influxdb()
