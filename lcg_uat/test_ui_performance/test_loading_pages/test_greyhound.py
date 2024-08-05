# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_GreyhoundPage(BasePerformanceTest):
    """
    NAME: 'Greyhound' page performance
    """
    def test_load_Greyhound_page(self):
        """
        DESCRIPTION: Load 'Greyhound' page
        EXPECTED: 'Greyhound' page is loaded
        """
        self.navigate_to_url(url='%s/#/greyhound' % self.test_hostname)
        self.post_to_influxdb()
