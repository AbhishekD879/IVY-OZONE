# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_InPlayAussieRulesPage(BasePerformanceTest):
    """
    NAME: 'In-Play' aussie rules page performance
    """
    def test_load_inplay_aussierules_page(self):
        """
        DESCRIPTION: Load 'In-Play' aussie rules page
        EXPECTED: 'In-Play' aussie rules page is loaded
        """
        self.navigate_to_url(url='%s/in-play/aussierules' % self.test_hostname)
        self.post_to_influxdb()
