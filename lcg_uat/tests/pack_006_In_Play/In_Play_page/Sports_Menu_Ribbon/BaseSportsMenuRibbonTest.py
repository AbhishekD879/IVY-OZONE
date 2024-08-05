from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import get_inplay_sports_ribbon, get_inplay_sports_ribbon_home_page
from voltron.utils.waiters import wait_for_result


class BaseSportsMenuRibbonTest(BaseSportTest):
    def wait_for_inplay_sports_ribbon_tabs(self):
        message = wait_for_result(lambda: get_inplay_sports_ribbon(),
                                  name='Get inplay sports ribbon tabs',
                                  timeout=15)
        if not message:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            message = wait_for_result(lambda: get_inplay_sports_ribbon(),
                                      name='Get inplay sports ribbon tabs',
                                      timeout=15)
        return message

    def wait_for_inplay_sports_ribbon_tabs_on_home_page(self):
        message = wait_for_result(lambda: get_inplay_sports_ribbon_home_page(),
                                  name='Get inplay sports ribbon tabs on home page',
                                  timeout=15)
        if not message:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            message = wait_for_result(lambda: get_inplay_sports_ribbon(),
                                      name='Get inplay sports ribbon tabs',
                                      timeout=15)
        return message
