import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Events with specific markets cannot be created in Prod/Beta
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.market_switcher
@pytest.mark.desktop
@vtest
class Test_C60089610_Verify_pre_selected_WDW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Boxing(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089610
    NAME: Verify pre selected ‘WDW’ MT is saved when switching b/w T/T/F on Matches Tab for Boxing
    DESCRIPTION: This test case verifies that previously selected ‘WDW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Boxing Landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Boxing Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
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
    device_name = tests.desktop_default

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
        items = list(self.boxing.accordions_list.items_as_ordered_dict.values())[0]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        self.assertEqual(event.header1, header1,
                         msg=f'Actual fixture header "{event.header1}" does not equal to'
                             f'Expected "{header1}"')
        if header2:
            self.assertEqual(event.header2, header2,
                             msg=f'Actual fixture header "{event.header2}" does not equal to'
                                 f'Expected "{header2}"')
        self.assertEqual(event.header3, header3,
                         msg=f'Actual fixture header "{event.header2}" does not equal to'
                             f'Expected "{header3}"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')
        section_name = 'BOXING - AUTO TEST BOXING'
        sections = self.site.boxing.tab_content.accordions_list.items_as_ordered_dict
        boxing_section = sections.get(section_name)

        name, odds_from_page = list(boxing_section.items_as_ordered_dict.items())[0]
        default_odds = odds_from_page.template.items_names
        for index in range(len(default_odds)):
            self.check_odds_format(odds=default_odds[index],
                                   expected_odds_format="fraction")

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Boxing Landing page -> 'Fights' tab
        PRECONDITIONS: 3. Select the 'Today' tab
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='boxing',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Boxing sport')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.boxing_config.category_id,
                                                       disp_sort_names='MR',
                                                       primary_markets='|Fight Betting|')
        # Today event
        self.ob_config.add_autotest_boxing_event()
        # Tomorrow event
        tomorrow = self.get_date_time_formatted_string(days=1)
        self.ob_config.add_autotest_boxing_event(start_time=tomorrow)
        # Future event
        future = self.get_date_time_formatted_string(days=7)
        self.ob_config.add_autotest_boxing_event(start_time=future)

        self.navigate_to_page(name='sport/boxing/matches')
        self.site.wait_content_state_changed()
        current_tab_name = self.site.boxing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.sb.TABS_NAME_FIGHTS.upper(),
                         msg=f'Default tab is "{current_tab_name}",instead of "{vec.sb.TABS_NAME_FIGHTS}"')
        grouping_buttons = self.site.boxing.tab_content.grouping_buttons
        current_tab = grouping_buttons.current
        self.assertEqual(current_tab.upper(), vec.sb.TABS_NAME_TODAY.upper(),
                         msg=f'Actual tab: "{current_tab.upper()}" is not same as'
                             f'Expected tab: "{vec.sb.TABS_NAME_TODAY.upper()}".')
        self.__class__.boxing = self.site.boxing.tab_content

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Fight Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Fight Betting' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Fight Betting' in 'Market selector' **Coral**
        """
        has_market_selector = self.boxing.has_dropdown_market_selector()
        self.assertTrue(has_market_selector,
                        msg=' "Market Selector" drop-down is not displayed on Fights tab in boxing')
        selected_value = self.boxing.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.title(), vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.title(),
                         msg=f'Actual selected value: "{selected_value.title()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.title()}"')
        dropdown = self.boxing.dropdown_market_selector
        if self.brand == 'bma':
            dropdown.click()
            sleep(1)
            self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
            self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
        else:
            dropdown.click()
            sleep(1)
            self.assertFalse(dropdown.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')

    def test_002_verify_displaying_of_preplay_events_for_fight_betting(self):
        """
        DESCRIPTION: Verify displaying of Preplay events for 'Fight Betting'
        EXPECTED: Preplay events are displayed
        """
        leagues = list(self.boxing.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(leagues, msg='Leagues not found')

        for league in leagues:
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                odds = list(event_template.items_as_ordered_dict.values())
                for odd in odds:
                    self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                self.assertFalse(event_template.is_live_now_event,
                                 msg=f'Event: "{event}" is an "In-Play" Event')
                self.assertTrue(event_template.event_name,
                                msg=' "Event Name" not displayed')
                self.assertTrue(event_template.event_time,
                                msg=' "Event time and date " are not displayed')
                if event_template.has_markets():
                    self._logger.info(f'"{event_template.event_name}" has more markets')
                else:
                    self._logger.info(f'"{event_template.event_name}" has no more markets')

    def test_003_verify_text_of_the_labels_for_fight_betting(self):
        """
        DESCRIPTION: Verify text of the labels for 'Fight Betting'
        EXPECTED: • The events for the Fight Betting market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Home' 'Draw' 'Away' and corresponding Odds are present under Label Home Draw Away respectively
        """
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME, header2=vec.sb.DRAW,
                                                          header3=vec.sb.AWAY)

    def test_004_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Fight Betting)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Home' 'Draw' 'Away'and corresponding Odds are present under Label Home Draw Away respectively
        EXPECTED: Note: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        self.site.boxing.date_tab.tomorrow.click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME, header2=vec.sb.DRAW,
                                                          header3=vec.sb.AWAY)

    def test_005_repeat_steps_4_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 4 for the 'Future' tab
        """
        self.site.boxing.date_tab.future.click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME, header2=vec.sb.DRAW,
                                                          header3=vec.sb.AWAY)

    def test_006_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Home ''Draw' 'Away' and corresponding Odds are present under Label Home Draw Away respectively
        """
        self.site.boxing.date_tab.today.click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME, header2=vec.sb.DRAW,
                                                          header3=vec.sb.AWAY)

    def test_007_verify_ga_tracking_for_the_fight_betting(self):
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
        if not self.boxing.dropdown_market_selector.is_expanded():
            self.boxing.dropdown_market_selector.expand()
        options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Fight Betting')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': 'Fight Betting',
                             'categoryID': 9,
                             }
        self.compare_json_response(actual_response, expected_response)
