from time import sleep

import pytest
import tests
from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


# @pytest.mark.prod
@pytest.mark.stg2
@pytest.mark.tst2
@vtest
class Test_PAT_003(BasePerformanceTest):
    """    PAT-003: Gaming History
    """

    def test_000_login_user(self):
        """
        Login User and navigate away from the Oxy
        """
        self.device.open_url(url=tests.HOSTNAME)
        self.site.login(username=tests.settings.recently_played_games_user)
        self.device.open_url(url='http://www.mithrilandmages.com/utilities/CityNamesServer.php?count=1')
        sleep(3)

    def test_001_load_gaming_history(self):
        """ Load Gaming History page
        """

        self.proxy.new_har(
            ref='Gaming History [%s]' % self.env,
            options={
                'captureHeaders': True,
                'captureContent': True,
                'captureBinaryContent': True
            }
        )
        # proxy.new_page(ref='Homepage')
        self.device.navigate_to(url='%s/#/gaming-history' % tests.HOSTNAME)
        # site.splash.wait_to_hide(poll_interval=0.2, timeout=180)
        har = self.proxy.har
        self.post_har(har=har)

        sleep(3)
        self.device.open_url(url='http://www.mithrilandmages.com/utilities/CityNamesServer.php?count=1')
        sleep(3)
        self.proxy.new_har(
            ref='Gaming History Cached [%s]' % self.env,
            options={
                'captureHeaders': True,
                'captureContent': True,
                'captureBinaryContent': True
            }
        )
        # proxy.new_page(ref='Homepage')
        self.device.navigate_to(url='%s/#/gaming-history' % tests.HOSTNAME)
        # site.splash.wait_to_hide(poll_interval=0.2, timeout=180)
        har = self.proxy.har
        self.proxy.close()
        self.post_har(har=har)

        self.site._driver.quit()
