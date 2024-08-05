import pytest
import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #cannot create events with private market offers
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C2538041_Your_Enhanced_Markets__Desktop_View(BasePrivateMarketsTest):
    """
    TR_ID: C2538041
    NAME: Your Enhanced Markets - Desktop View
    DESCRIPTION:
    PRECONDITIONS: User should be eligible for one or more private enhanced market offers
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_001_login_with_user_eligible_for_one_or_more_private_enhanced_market_offers(self):
        """
        DESCRIPTION: Login with user eligible for one or more private enhanced market offers
        EXPECTED: *  Homepage is opened
        EXPECTED: *  'Your Enhanced Markets' section is present at the top of the page below Hero Header
        """
        self.__class__.user = tests.settings.betplacement_user
        self.site.login(username=self.user)
        self.site.wait_content_state(state_name='Homepage')
        self.trigger_private_market_appearance(user=self.user,
                                               expected_market_name=self.private_market_name)
        sleep(3)
        self.__class__.tab_name = self.expected_sport_tabs.private_market
        private_market_tab_content = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
        markets = private_market_tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No Markets found')

        for market in markets.values():
            self.assertTrue(market.is_displayed(),
                            msg='Private markets and associated selections are expected to be shown')
            self.assertTrue(market.is_expanded(),
                            msg='Markets are not expanded by default')

    def test_002_log_out_from_app_and_verify_your_enhanced_markets_section(self):
        """
        DESCRIPTION: Log out from app and verify 'Your Enhanced Markets' section
        EXPECTED: * 'Your Enhanced Markets' section is disappeared
        EXPECTED: * 'In-Play & Live Stream' section is displayed at the top
        """
        self.site.logout()
        self.site.wait_content_state('Home')
        tabs = self.site.home.desktop_modules.items_names
        self.assertNotIn(self.tab_name, tabs,
                         msg=f'Tab "{self.tab_name}" is not displayed for the user which is '
                             f'"{tests.settings.user_with_private_market}"')
