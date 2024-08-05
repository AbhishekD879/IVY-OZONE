import pytest
from tests.base_test import vtest
from time import sleep
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from selenium.common.exceptions import WebDriverException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60089522_Verify_MS_on_Matches_Tab_for_AmFootball_SLP(BaseBetSlipTest):
    """
    TR_ID: C60089522
    NAME: Verify MS on Matches Tab for Am.Football SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on American Football Landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the American Football Landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |60 Minute Betting| - "60 Minute Betting"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    markets = [
        ('60_minute_betting', ),
        ('handicap_2_way', ),
        ('total_points', )
    ]

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
        items = list(self.site.american_football.tab_content.accordions_list.items_as_ordered_dict.values())[0]
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
                         msg=f'Actual fixture header "{event.header3}" does not equal to'
                             f'Expected "{header3}"')

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def place_bet_and_verify(self):
        sections = self.site.american_football.tab_content.accordions_list.items_as_ordered_dict.get('AMERICAN FOOTBALL - AUTO TEST LEAGUE')
        event1 = sections.items_as_ordered_dict.get(self.event_name1)
        selection1 = list(event1.template.items_as_ordered_dict.values())[0]
        selection1.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=10), msg='Quick Bet panel is not opened')
            self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(), msg='Bet Receipt is not displayed')
            self.site.quick_bet_panel.header.close_button.click()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()

        # multiple bet
        selection1.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet panel is not opened')
            self.site.quick_bet_panel.add_to_betslip_button.click()
        event2 = sections.items_as_ordered_dict.get(self.event_name2)
        selection2 = list(event2.template.items_as_ordered_dict.values())[0]
        sleep(2)
        selection2.click()
        if self.device_type == 'mobile':
            self.site.open_betslip()
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        if self.device_type == 'mobile':
            self.site.bet_receipt.close_button.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with required markets
        DESCRIPTION: Navigate to american football page
        EXPECTED: Event is successfully created
        """
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='americanfootball', status=True)
        self.assertTrue(status, msg=f'The sport "americanfootball" is not checked')
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(self.ob_config.backend.ti.american_football.category_id,
                                                       disp_sort_names='HH,WH,MR,HL',
                                                       primary_markets='|Money Line|,|Handicap 2-way|,|60 Minute Betting|,|Total Points|')
        event1 = self.ob_config.add_american_football_event_to_autotest_league(markets=self.markets)
        event2 = self.ob_config.add_american_football_event_to_autotest_league(markets=self.markets)
        self.__class__.event_name1 = event1.team2 + ' v ' + event1.team1
        self.__class__.event_name2 = event2.team2 + ' v ' + event2.team1
        self.site.login()
        self.navigate_to_page(name='sport/american-football')
        self.site.wait_content_state('american-football')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.american_football_config.category_id)
        self.site.american_football.tabs_menu.click_button(expected_tab_name)
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.american_football.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Rugby Leauge')
        dropdown = self.site.american_football.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                sleep(2)
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.american_football.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line,
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: * Money Line
        EXPECTED: * Handicap (Handicap in Lads and Spread in Coral)
        EXPECTED: * 60 Minute Betting
        EXPECTED: * Total Points
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        actual_list = list(self.site.american_football.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if self.brand == 'bma':
            self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line.title(),
                                            vec.siteserve.EXPECTED_MARKET_SECTIONS.spread.title(),
                                            vec.siteserve.EXPECTED_MARKET_SECTIONS.sixty_minute_betting.title(),
                                            vec.siteserve.EXPECTED_MARKET_SECTIONS.total_points.title()]
        else:
            self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line.title(),
                                            vec.siteserve.EXPECTED_MARKET_SECTIONS.handicap.title(),
                                            vec.siteserve.EXPECTED_MARKET_SECTIONS.sixty_minute_betting.title(),
                                            vec.siteserve.EXPECTED_MARKET_SECTIONS.total_points.title()]
        self.assertListEqual(actual_list, self.expected_list,
                             msg=f'Actual List: "{actual_list} is not same as'
                                 f'Expected List: "{self.expected_list}"')

    def test_003_select_money_line_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Money Line' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        self.site.american_football.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_list[0]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1', header3='2')
        self.place_bet_and_verify()

    def test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_and_tablet___coral_and_lads__lads__desktop(self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (Applicable for mobile and tablet - Coral and Lads & Lads- Desktop)
        EXPECTED: 'SEE All' option will be displayed when more than one event is there for that particular Tournament/League
        """
        if self.device_type == 'mobile' or self.brand == 'ladbrokes':
            try:
                sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
                section_name, self.__class__.section = list(sections.items())[0]
                has_see_all_link = self.section.group_header.has_see_all_link()
                self.assertTrue(has_see_all_link, msg=f'*** SEE ALL link not present in the section %s' % section_name)
            except WebDriverException:
                self._logger.info(f'*** No more than one event found')

    def test_005_click_on_see_all(self):
        """
        DESCRIPTION: Click on 'SEE ALL'
        EXPECTED: EXPECTED: User should be navigated to competition tab where whole list of available events(Preplay/Inplay) will be displayed for that particular Tournament/League with Market switcher dropdown
        """
        if self.device_type == 'mobile' or self.brand == 'ladbrokes':
            try:
                self.site.wait_splash_to_hide()
                self.section.group_header.see_all_link.click()
                self.site.wait_content_state('CompetitionLeaguePage')
                sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(sections, msg='No list of available events are present on competition league page')
                self.device.go_back()
            except WebDriverException:
                self._logger.info(f'*** No more than one event found')

    def test_006_repeat_steps_3_5_for_the_following_markets_money_line_handicap_handicap_in_lads_and_spread_in_coral_60_minute_betting(self):
        """
        DESCRIPTION: Repeat steps 3-5 for the following markets:
        DESCRIPTION: * Money Line
        DESCRIPTION: * Handicap (Handicap in Lads and Spread in Coral)
        DESCRIPTION: * 60 Minute Betting
        EXPECTED:
        """
        # handicap or spread
        self.site.american_football.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_list[1]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1', header3='2')
        self.place_bet_and_verify()
        self.test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_and_tablet___coral_and_lads__lads__desktop()
        self.test_005_click_on_see_all()

        # 60 minute betting
        self.site.american_football.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_list[2]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='TIE', header3='2')
        self.place_bet_and_verify()
        self.test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_and_tablet___coral_and_lads__lads__desktop()
        self.test_005_click_on_see_all()

        # total points
        self.site.american_football.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_list[3]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.SB.FIXTURE_HEADER.over, header3=vec.SB.FIXTURE_HEADER.under)
        self.place_bet_and_verify()
        self.test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_and_tablet___coral_and_lads__lads__desktop()
        self.test_005_click_on_see_all()

    def test_007_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_money_line_handicap_handicap_in_lads_and_spread_in_coral_60_minute_betting_total_points(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: * Money Line
        DESCRIPTION: * Handicap (Handicap in Lads and Spread in Coral)
        DESCRIPTION: * 60 Minute Betting
        DESCRIPTION: * Total Points
        EXPECTED: Bet should be placed successfully
        """
        # covered in step 006
