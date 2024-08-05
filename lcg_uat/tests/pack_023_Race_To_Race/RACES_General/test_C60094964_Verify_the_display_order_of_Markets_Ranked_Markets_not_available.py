import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from tenacity import retry, wait_fixed, retry_if_exception_type, stop_after_attempt
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # events can't be created on Prod/Beta
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.greyhounds
@pytest.mark.slow
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094964_Verify_the_display_order_of_Markets_Ranked_Markets_not_available(Common):
    """
    TR_ID: C60094964
    NAME: Verify the display order of Markets- Ranked Markets not available
    DESCRIPTION: Verify that if a Market is ranked but unavailable next ranked market will take the position and unavailable market will not be displayed in EDP
    PRECONDITIONS: 1: Horse Racing and Grey Hound racing events should be available
    PRECONDITIONS: 2: Markets order should be configured in CMS
    PRECONDITIONS: 3: Few Markets which are configured in CMS should not be available in EDP
    """
    keep_browser_open = True
    markets = [('win_only',),
               ('betting_without',),
               ('top_2_finish',)]

    @retry(stop=stop_after_attempt(10), retry=retry_if_exception_type(VoltronException), wait=wait_fixed(wait=2),
           reraise=True)
    def wait_for_markets_to_reflect(self, sport=None):
        if not self.cms_config.get_system_configuration_structure()['RacingEDPMarketsDescription']['enabled']:
            self.cms_config.update_system_configuration_structure(config_item='RacingEDPMarketsDescription',
                                                                  field_name='enabled',
                                                                  field_value=True)
        win_ew = self.cms_config.create_and_update_markets_with_description(name='Win or Each Way', description='This description of Win or Each Way market is for testing purpose.')
        win_only = self.cms_config.create_and_update_markets_with_description(name='Win Only', description='This description of Win Only market is for testing purpose.')
        to_finish = self.cms_config.create_and_update_markets_with_description(name='To Finish Second', description='This description of To Finish Second market is for testing purpose')
        betting_without = self.cms_config.create_and_update_markets_with_description(name='Betting Without', description='This description of Betting Without market is for testing purpose')
        if sport:
            self.__class__.cms_order = [win_ew['name'].replace('Each Way', 'E/W').upper(), win_only['name'].upper(),
                                        to_finish['name'].upper(), betting_without['name'].upper()]
            self.device.refresh_page()
            if sport == 'Horse Racing':
                self.market_tabs = list(self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.
                                        items_as_ordered_dict.keys())
            else:
                self.market_tabs = list(self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.
                                        items_as_ordered_dict.keys())
            self.assertListEqual(self.market_tabs[:2], self.cms_order[:2],
                                 msg=f'Actual market tabs order(FE): "{self.market_tabs[:2]}" is not same as Expected market tabs order(CMS): "{self.cms_order[:2]}"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1: Horse Racing and Grey Hound racing events should be available
        PRECONDITIONS: 2: Markets order should be configured in CMS
        PRECONDITIONS: 3: Few Markets which are configured in CMS should not be available in EDP
        """
        self.wait_for_markets_to_reflect()
        self.__class__.hr_event = self.ob_config.add_UK_racing_event(markets=self.markets, number_of_runners=1)
        self.__class__.gh_event = self.ob_config.add_UK_greyhound_racing_event(markets=self.markets, number_of_runners=1)

    def test_001_1launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: 1:Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_2_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: 2: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_events_which_does_not_have_all_markets_configured_in_cms(self):
        """
        DESCRIPTION: Click on any events which does not have all markets configured in CMS
        EXPECTED: User should be navigated to EDP
        """
        self.navigate_to_edp(event_id=self.hr_event.event_id, sport_name='horse-racing')
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_004_validate_the_display_order_of_markets(self, actual_market_tabs=None, sport='Horse Racing'):
        """
        DESCRIPTION: Validate the display order of Markets
        EXPECTED: 1: Market tabs should be displayed as per CMS ranking
        EXPECTED: 2: The market is ranked in CMS but unavailable should not be displayed
        EXPECTED: 3: The Next ranked market should take the position
        EXPECTED: Example: 1:Win or Each Way, 2:Win Only, 3:Betting without are configured in CMS
        EXPECTED: Win Only is not available in EDP for an event then the order should be displayed as Win or Each way, Betting without
        """
        if actual_market_tabs:
            self.market_tabs = actual_market_tabs
        else:
            self.market_tabs = list(self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.
                                    items_as_ordered_dict.keys())
        self.wait_for_markets_to_reflect(sport=sport)
        self.assertNotIn(vec.racing.RACING_EDP_MARKET_TABS.to_finish, self.market_tabs,
                         msg=f'Market tab: "{vec.racing.RACING_EDP_MARKET_TABS.to_finish}" is displayed in FE which is not expected')
        self.assertIn(vec.racing.RACING_EDP_MARKET_TABS.betting_wo if self.brand == 'bma' else vec.racing.RACING_EDP_MARKET_TABS.betting_without, self.market_tabs[2:],
                      msg=f'Market tab: "{vec.racing.RACING_EDP_MARKET_TABS.betting_wo if self.brand == "bma" else vec.racing.RACING_EDP_MARKET_TABS.betting_without}" '
                          f'has not taken the expected position in the list of markets: "{self.market_tabs[2:]}"')

    def test_005_navigate_to_grey_hounds_and_validate_the_same(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Validate the same
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing')
        self.navigate_to_edp(event_id=self.gh_event.event_id, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')
        self.market_tabs = list(self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.
                                items_as_ordered_dict.keys())
        self.test_004_validate_the_display_order_of_markets(actual_market_tabs=self.market_tabs, sport='Greyhounds')
