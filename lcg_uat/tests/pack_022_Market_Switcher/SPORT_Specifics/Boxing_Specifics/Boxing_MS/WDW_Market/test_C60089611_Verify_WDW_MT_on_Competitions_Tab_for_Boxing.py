import pytest
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from time import sleep
from voltron.environments import constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089611_Verify_WDW_MT_on_Competitions_Tab_for_Boxing(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089611
    NAME: Verify 'WDW’ MT on Competitions Tab for Boxing
    DESCRIPTION: This test case verifies the behavior of ‘WDW market’ Template in  Competition Landing page for Boxing
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Boxing -> 'Click on Competition Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Below market should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Fight Betting(WDW)| - "Fight Betting"
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

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Boxing -> 'Click on Competition Tab'
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='boxing',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Boxing sport')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.boxing_config.category_id,
                                                       disp_sort_names='MR',
                                                       primary_markets='|Fight Betting|')
        self.ob_config.add_autotest_boxing_event()
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.boxing_config.category_id)
        self.navigate_to_page(name='sport/boxing')
        self.site.wait_content_state_changed()
        sport_title = self.site.boxing.header_line.page_title.text
        self.assertEqual(sport_title.upper(), vec.sb.BOXING.upper(),
                         msg=f'Actual page is "{sport_title}",instead of "{vec.sb.BOXING}"')
        self.site.boxing.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.boxing.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')
        self.__class__.boxing = self.site.competition_league.tab_content

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Fight Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Fight Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Fight Betting' in 'Market selector' Coral
        """
        has_market_selector = self.boxing.has_dropdown_market_selector()
        self.assertTrue(has_market_selector,
                        msg=' "Market Selector" drop-down is not displayed on Fights tab in boxing')
        selected_value = self.boxing.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.title(), vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.title(),
                         msg=f'Actual selected value: "{selected_value.title()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.title()}"')
        self.__class__.dropdown = self.boxing.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                sleep(2)
                self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')

    def test_002_select_fight_betting_from_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Select 'Fight Betting' from the Market Selector dropdown
        EXPECTED: 'Fight Betting' should be selected and respective events with odds will be displayed
        """
        options = self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        try:
            options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting).click()
        except Exception:
            self.site.contents.scroll_to_top()
            options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting).click()
        selected_value = self.boxing.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.upper()}"')

    def test_003_verify_displaying_of_preplay_and_inplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay and Inplay events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: Fight Betting (Preplay and Inplay)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        self.__class__.leagues = list(
            self.boxing.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')

        for league in self.leagues:
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

    def test_004_verify_text_of_the_labels_for_fight_betting(self):
        """
        DESCRIPTION: Verify text of the labels for 'Fight Betting'
        EXPECTED: • The events for the Fight Betting market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'Home' 'Draw' 'Away' and corresponding Odds are present under Label Home Draw Away
        """
        sections = wait_for_result(
            lambda: self.boxing.accordions_list.items_as_ordered_dict,
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
        self.assertEqual(default_fixture_value, [vec.sb.HOME, vec.sb.DRAW, vec.sb.AWAY],
                         msg=f'Actual fixture header "{default_fixture_value}" does not '
                             f'equal to expected "{[vec.sb.HOME, vec.sb.DRAW, vec.sb.AWAY]}"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, 3,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "3"')
        name, odds_from_page = list(time_segment.items_as_ordered_dict.items())[0]
        default_odds = odds_from_page.template.items_names
        for index in range(len(default_odds)):
            self.check_odds_format(odds=default_odds[index], expected_odds_format="fraction")

    def test_005_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: • Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        # Covered in step 3

    def test_006_verify_ga_tracking_for_the_fight_betting(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Fight Betting'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Fight Betting"
        EXPECTED: categoryID: "9"
        EXPECTED: })
        """
        options = self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        try:
            options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting).click()
        except Exception:
            self.site.contents.scroll_to_top()
            options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Fight Betting')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': 'Fight Betting',
                             'categoryID': '9',
                             }
        self.compare_json_response(actual_response, expected_response)
