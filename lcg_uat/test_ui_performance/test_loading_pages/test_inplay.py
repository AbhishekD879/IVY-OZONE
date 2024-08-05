# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_InPlayPage(BasePerformanceTest):
    """
    NAME: 'In-Play' page performance
    """
    def test_load_inplay_page(self):
        """
        DESCRIPTION: Load 'In-Play' page
        EXPECTED: 'In-Play' page is loaded
        """
        self.navigate_to_url(url='%s/in-play' % self.test_hostname)
        self.post_to_influxdb()
