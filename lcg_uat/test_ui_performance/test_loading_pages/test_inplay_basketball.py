# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_InPlayBasketballPage(BasePerformanceTest):
    """
    NAME: 'In-Play' basketball page performance
    """
    def test_load_inplay_basketball_page(self):
        """
        DESCRIPTION: Load basketball 'In-Play' page
        EXPECTED: 'In-Play' basketball page is loaded
        """
        self.navigate_to_url(url='%s/in-play/basketball' % self.test_hostname)
        self.post_to_influxdb()
