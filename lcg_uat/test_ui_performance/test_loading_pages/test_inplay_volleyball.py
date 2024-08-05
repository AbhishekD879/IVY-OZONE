# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_InPlayVolleyballPage(BasePerformanceTest):
    """
    NAME: 'In-Play' volleyball page performance
    """
    def test_load_inplay_volleyball_page(self):
        """
        DESCRIPTION: Load 'In-Play' volleyball page
        EXPECTED: 'In-Play' volleyball page is loaded
        """
        self.navigate_to_url(url='%s/in-play/volleyball' % self.test_hostname)
        self.post_to_influxdb()
