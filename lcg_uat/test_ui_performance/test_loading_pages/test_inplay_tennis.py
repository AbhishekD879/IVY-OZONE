# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_InPlayTennisPage(BasePerformanceTest):
    """
    NAME: 'In-Play' tennis page performance
    """
    def test_load_inplay_tennis_page(self):
        """
        DESCRIPTION: Load 'In-Play' tennis page
        EXPECTED: 'In-Play' tennis page is loaded
        """
        self.navigate_to_url(url='%s/in-play/tennis' % self.test_hostname)
        self.post_to_influxdb()
