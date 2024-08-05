import pytest

import tests
from tests.Common import Common
from tests.base_test import vtest
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.crl_hl
# @pytest.mark.crl_prod
@pytest.mark.medium
@pytest.mark.retail
@pytest.mark.football_bet_filter
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C2912144_Verify_navigation_to_Football_filter(Common):
    """
    TR_ID: C2912144
    NAME: Verify navigation to Football filter
    DESCRIPTION: This test case verifies navigation to Football Bet Filter from all possible places except Homepage -> Football -> Coupons tab (this verification is done in C2496181
    PRECONDITIONS: Make sure Football Bet Filter feature is turned on in CMS: System configuration -> Connect -> football Filter
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: Following API returns events for applying Football filters on (After navigating to Football Filter search in console: retailCoupon):
    PRECONDITIONS: **Online betting:**
    PRECONDITIONS: https://api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LAD0cc93c420eeb433aaf57a1ca299ed93c
    PRECONDITIONS: **In-Shop betting:**
    PRECONDITIONS: https://api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LADe196db0611e240d7a8ea3fc67135c37c
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check if Bet Filter is enabled in CMS
        """
        cms_config = self.get_initial_data_system_configuration().get('Connect', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('Connect')
        if not cms_config.get('footballFilter'):
            raise CmsClientException('"Football Bet Filter" is disabled')

        self.__class__.bet_filter_present = False
        self.__class__.connect_menu = self.cms_config.get_cms_menu_items('Connect Menus').get('Connect Menus')
        for item in self.connect_menu:
            if 'bet-filter' in item['targetUri'] and not item['disabled']:
                self.bet_filter_present = True

        self.__class__.bet_filter_present_on_right_menu = False
        self.__class__.connect_menu = self.cms_config.get_cms_menu_items('Right Menus').get('Right Menus')
        for item in self.connect_menu:
            if 'bet-filter' in item['targetUri'] and not item['disabled']:
                self.bet_filter_present_on_right_menu = True

    def test_001_open_connect_landing_page(self):
        """
        DESCRIPTION: Open Connect landing page
        """
        self.device.open_url(url='%s%s' % (tests.HOSTNAME, '/retail'))

    def test_002_select_football_bet_filter(self):
        """
        DESCRIPTION: Select Football Bet Filter
        EXPECTED: * Football Bet Filter Page is opened
        EXPECTED: * API for in-shop betting returns events
        """
        if self.bet_filter_present:
            self.assertTrue(self.site.connect.menu_items.is_displayed(), msg='Failed to display Connect Menu')
            self.assertIn(vec.retail.BET_FILTER, self.site.connect.menu_items.items_as_ordered_dict,
                          msg='No "Football Bet Filter" item in Connect Menu')
            self.site.connect.menu_items.items_as_ordered_dict[vec.retail.BET_FILTER].click()
            self.site.wait_content_state(state_name='FootballBetFilterPage')

    def test_003_open_right_hand_menu(self):
        """
        DESCRIPTION: Open Right-hand menu
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='/')
            self.site.login()
            self.site.header.right_menu_button.click()

    def test_004_select_football_bet_filter(self):
        """
        DESCRIPTION: Select Football Bet Filter
        EXPECTED: * Football Bet Filter Page is opened
        EXPECTED: * API for in-shop betting returns events
        """
        if self.bet_filter_present_on_right_menu and self.device_type == 'mobile':
            menu_items = self.site.right_menu.items_as_ordered_dict
            self.assertIn(vec.retail.BET_FILTER.upper(), menu_items, msg='No "Football Bet Filter" item in Right Menu')
            menu_items[vec.retail.BET_FILTER.upper()].click()
            self.site.wait_content_state(state_name='FootballBetFilterPage')

    def test_005_open_a_z_all_sports_page(self):
        """
        DESCRIPTION: Open 'A-Z' ('All sports') page
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='/')
            self.site.open_sport(name='ALL SPORTS')
        else:
            self.navigate_to_page('az-sports')

    def test_006_select_football_bet_filter(self):
        """
        DESCRIPTION: Select Football Bet Filter
        EXPECTED: * Football Bet Filter Page is opened
        EXPECTED: * API for in-shop betting returns events
        """
        if self.bet_filter_present:
            sports = self.site.all_sports.items_as_ordered_dict
            self.assertIn(vec.retail.BET_FILTER, sports, msg='No "Football Bet Filter" item on All Sports page')
            sports[vec.retail.BET_FILTER].click()
            self.site.wait_content_state(state_name='FootballBetFilterPage')
