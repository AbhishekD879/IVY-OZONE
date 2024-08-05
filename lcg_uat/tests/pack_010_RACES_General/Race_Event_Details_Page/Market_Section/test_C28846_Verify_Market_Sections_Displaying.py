import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events with diff markets
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28846_Verify_Market_Sections_Displaying(Common):
    """
    TR_ID: C28846
    NAME: Verify Market Sections Displaying
    DESCRIPTION: Verify market sections displaying on event details page
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-6586 - Racecard Layout Update - Markets and Selections area
    DESCRIPTION: Applies to mpobile, tablet & desktop
    """
    keep_browser_open = True

    def markets_tabs_verification(self):
        self.__class__.markets = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.__class__.market_tabs = self.markets.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found')
        for market in self.expected_tabs:
            self.assertIn(market, self.market_tabs.keys(),
                          msg=f'"{market}" tab was not found in the tabs list "{self.market_tabs.keys()}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event in OB TI
        """
        # four or more markets
        markets = [
            ('betting_without',),
            ('to_finish_second',),
            ('win_only',)
        ]
        event_params1 = self.ob_config.add_UK_racing_event(markets=markets)
        self._logger.info('*** Created Horse racing event with parameters {}'.format(event_params1))
        self.__class__.eventID1 = event_params1.event_id
        # Three markets
        event_params2 = self.ob_config.add_UK_racing_event(markets=[('to_finish_second',), ('win_only',)])
        self._logger.info('*** Created Horse racing event with parameters {}'.format(event_params2))
        self.__class__.eventID2 = event_params2.event_id
        # Two markets
        event_params3 = self.ob_config.add_UK_racing_event(markets=[('to_finish_second',)])
        self._logger.info('*** Created Horse racing event with parameters {}'.format(event_params3))
        self.__class__.eventID3 = event_params3.event_id
        # One market
        event_params4 = self.ob_config.add_UK_racing_event()
        self._logger.info('*** Created Horse racing event with parameters {}'.format(event_params4))
        self.__class__.eventID4 = event_params4.event_id

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Home')

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the Sports Menu Ribbon
        EXPECTED: <Race> landing page is opened
        """
        self.navigate_to_edp(event_id=self.eventID1, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')

    def test_003_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        # covered in above step

    def test_004_verify_market_section(self):
        """
        DESCRIPTION: Verify market section
        EXPECTED: *   Available markets are displayed as tabs labeled as a market name
        EXPECTED: *   'Win or E/W' tab is selected and highlighted by default
        """
        # Win or E/w is no longer default market
        self.__class__.expected_tabs = [vec.sb.WIN_OR_EACH_WAY.upper(),
                                        vec.sb.BETTING_WITHOUT.upper() if self.brand == 'bma' else vec.racing.RACING_EDP_BETTING_WITHOUT.upper(),
                                        vec.sb.TO_FINISH_MARKETS.upper(),
                                        vec.betslip.WIN_ONLY.upper()]
        self.markets_tabs_verification()
        self.markets.open_tab(list(self.market_tabs.keys())[1])
        current_tab_name = self.markets.current
        self.assertEqual(current_tab_name, list(self.market_tabs.keys())[1],
                         msg=f'"{current_tab_name}" tab was not selected "{list(self.market_tabs.keys())[1]}"')
        market = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict[list(self.market_tabs.keys())[1]]
        status = wait_for_result(lambda: int(market.css_property_value('font-weight')) == 700, timeout=40)
        self.assertTrue(status,
                        msg=f'{list(self.market_tabs.keys())[1]} is not highlighted according to the selected page')

    def test_005_navigate_between_tabs(self):
        """
        DESCRIPTION: Navigate between tabs
        EXPECTED: *   User is redirected to next tab
        EXPECTED: *   Tab is selected and highlighted
        """
        # covered in above step

    def test_006_verify_markets_tab_when_four_and_more_market_typesare_available(self):
        """
        DESCRIPTION: Verify markets tab when four and more market types are available
        EXPECTED: Four market tabs are displayed filling all available width
        """
        # covered in above step

    def test_007_verify_markets_tab_when_three_market_types_are_available(self):
        """
        DESCRIPTION: Verify markets tab when three market types are available
        EXPECTED: Three market tabs are displayed filling all available width
        """
        self.navigate_to_edp(event_id=self.eventID2, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')
        self.__class__.expected_tabs = [vec.sb.WIN_OR_EACH_WAY.upper(),
                                        vec.sb.TO_FINISH_MARKETS.upper(), vec.betslip.WIN_ONLY.upper()]
        self.markets_tabs_verification()

    def test_008_verify_markets_tab_when_two_market_types_are_available(self):
        """
        DESCRIPTION: Verify markets tab when two market types are available
        EXPECTED: Two market tabs are displayed filling all available width
        """
        self.navigate_to_edp(event_id=self.eventID3, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')
        self.__class__.expected_tabs = [vec.sb.WIN_OR_EACH_WAY.upper(),
                                        vec.sb.TO_FINISH_MARKETS.upper()]
        self.markets_tabs_verification()

    def test_009_verify_markets_tab_when_one_market_type_is_available(self):
        """
        DESCRIPTION: Verify markets tab when one market type is available
        EXPECTED: One market tab is displayed filling all available width
        """
        self.navigate_to_edp(event_id=self.eventID4, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')
        self.__class__.expected_tabs = [vec.sb.WIN_OR_EACH_WAY.upper()]
        self.markets_tabs_verification()
