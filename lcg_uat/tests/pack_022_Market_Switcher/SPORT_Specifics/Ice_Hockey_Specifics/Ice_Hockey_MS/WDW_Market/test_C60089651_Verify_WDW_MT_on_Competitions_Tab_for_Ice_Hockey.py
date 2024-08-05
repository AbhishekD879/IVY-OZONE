import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result
from time import sleep
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.market_switcher
@pytest.mark.desktop
@vtest
class Test_C60089651_Verify_WDW_MT_on_Competitions_Tab_for_Ice_Hockey(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089651
    NAME: Verify 'WDW’ MT on Competitions Tab for Ice Hockey
    DESCRIPTION: This test case verifies displaying of ‘WDW market’ Template is displaying for Ice Hockey Competition page under Market Selector Dropdown
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |60 Minutes Betting|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Ice Hockey Landing Page -> 'Click on Competition Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: *|60 Minutes Betting (WDW)|- "60 Minutes Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    preplay_list = []
    inplay_list = []
    event_markets = [('sixty_minutes_betting',)]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Ice Hockey event with required markets
        EXPECTED: Event is successfully created
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='icehockey',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='"Market Switcher" is disabled for IceHockey sport')
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.ice_hockey.category_id,
            disp_sort_names='HH,WH,MR,HL',
            primary_markets='|Money Line|,|Total Goals 2-way|,|Puck Line|,|60 Minutes Betting|')
        self.ob_config.add_ice_hockey_event_to_ice_hockey_usa(markets=self.event_markets)
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.navigate_to_page(name='sport/ice-hockey')
        self.site.wait_content_state(state_name='IceHockey')
        self.site.ice_hockey.tabs_menu.click_button(self.expected_sport_tabs.competitions)
        current_tab_name = self.site.ice_hockey.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.competitions,
                         msg=f'Expected tab: "{current_tab_name}", Actual Tab: "{self.expected_sport_tabs.competitions}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • '60 Minutes Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '60 Minutes Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to '60 Minutes Betting' in 'Market selector' Coral
        """
        self.__class__.ice_hockey_tab_content = self.site.ice_hockey.tab_content
        self.assertTrue(self.ice_hockey_tab_content.has_dropdown_market_selector(timeout=20),
                        msg='"Market Selector" drop-down is not displayed on IceHockey landing page')
        market_selector_default_value = self.market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.market_selector_default_value
        self.assertEqual(self.ice_hockey_tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{self.ice_hockey_tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')
        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        self.dropdown.click()
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing upwards')
        if self.brand == 'bma' and self.device_type == 'desktop':
            self.assertTrue(self.dropdown.has_up_arrow, msg='Market selector up arrow is not displayed')
            self.assertTrue(self.dropdown.has_down_arrow, msg='Market selector down arrow is not displayed')
        elif self.device_type == 'mobile' or self.brand == 'ladbrokes':
            # sleep provided as it takes some time to close the market switcher dropdown
            sleep(2)
            self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')

    def test_002_verify_text_of_the_labels_for_60_minutes_betting(self):
        """
        DESCRIPTION: Verify text of the labels for '60 Minutes Betting'
        EXPECTED: • The events for the '60 Minutes Betting' market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' , 'Tie' & '2' and corresponding Odds are present under Label 1 , tie and 2.
        """
        expected_market = '60 MINUTES BETTING' if self.brand == 'ladbrokes' and self.device_type == 'desktop' else '60 Minutes Betting'
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get('60 Minutes Betting').click()
        result = wait_for_result(lambda: self.ice_hockey_tab_content.dropdown_market_selector.
                                 selected_market_selector_item == expected_market,
                                 name='"60 Minutes Betting" market to be selected',
                                 timeout=10)
        self.assertTrue(result, msg='Selected market is not "60 Minutes Betting"')
        sections = wait_for_result(
            lambda: self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict,
            timeout=5,
            name='Events to appear')
        self.assertTrue(sections, msg='No sections are present on page')
        tab_name = vec.sb.TABS_NAME_TODAY.title() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else vec.sb.TABS_NAME_TODAY
        time_segment_name, time_segment = \
            next(((segment_name, segment) for (segment_name, segment) in sections.items() if tab_name in segment_name),
                 ('', None))
        events = time_segment.items_as_ordered_dict.values()
        default_fixture_value = list(time_segment.fixture_header.items_as_ordered_dict.keys())
        expected_format = ['1', 'TIE', '2']
        self.assertEqual(default_fixture_value, expected_format,
                         msg=f'Actual fixture header "{default_fixture_value}" does not '
                             f'equal to expected "{expected_format}"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, 3,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "3"')
        name, odds_from_page = list(time_segment.items_as_ordered_dict.items())[0]
        default_odds = odds_from_page.template.items_names
        for index in range(len(default_odds)):
            self.check_odds_format(odds=default_odds[index], expected_odds_format="fraction")

    def test_003_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: •Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: •Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        leagues = list(
            self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(leagues, msg='Leagues not found')

        for league in leagues:
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                is_live = event_template.is_live_now_event
                self.inplay_list.append(is_live) if is_live else self.preplay_list.append(is_live)
                odds = list(event_template.items_as_ordered_dict.values())
                for odd in odds:
                    self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                self.assertTrue(event_template.event_name,
                                msg=' "Event Name" not displayed')
                if is_live:
                    self._logger.info(f'{event_template.event_name} is live event')
                else:
                    self.assertTrue(event_template.event_time,
                                    msg=' "Event time" not displayed')
                if event_template.has_markets():
                    self._logger.info(f'{event_template.event_name} has more markets')
                else:
                    self._logger.info(f'{event_template.event_name} has no more markets')

        if len(self.inplay_list) > 0 and len(self.preplay_list) == 0:
            self._logger.info(msg=f'Only "In-Play" events are available ')
        elif len(self.inplay_list) == 0 and len(self.preplay_list) > 0:
            self._logger.info(msg=f'Only "Pre-Play" events are available ')
        else:
            self._logger.info(msg=f'Both "In-Play" and "Pre-play" events are available ')

    def test_004_verify_displaying_of_preplay_and_inplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay and Inplay events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • 60 Minutes Betting (Preplay and Inplay market)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        # Covered in step 3

    def test_005_verify_ga_tracking_for_the_60_minutes_betting(self):
        """
        DESCRIPTION: Verify GA Tracking for the '60 Minutes Betting'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "60 Minutes Betting"
        EXPECTED: categoryID: "22"
        EXPECTED: })
        """
        self.dropdown.scroll_to()
        options = self.ice_hockey_tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get('60 Minutes Betting').click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='60 Minutes Betting')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': '60 Minutes Betting',
                             'categoryID': '22',
                             }
        self.compare_json_response(actual_response, expected_response)
