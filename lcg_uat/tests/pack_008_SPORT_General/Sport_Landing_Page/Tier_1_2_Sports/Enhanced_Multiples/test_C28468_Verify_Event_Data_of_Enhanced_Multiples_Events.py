import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events cannot be created on prod & beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C28468_Verify_Event_Data_of_Enhanced_Multiples_Events(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28468
    NAME: Verify Event Data of Enhanced Multiples Events
    DESCRIPTION: This test case verifies Event Data of Enhanced Multiples Events.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: **NOTE: Make sure you have  Enhanced Multiples events on Some sports (Sport events with typeName="Enhanced Multiples").**
    PRECONDITIONS: In order to check particular event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: Make sure you have <Sport> Enhanced Multiples events (events with **drilldownTagNames="EVFLAG_ES**")
    """
    keep_browser_open = True
    selection_type = "all to win in 90 Mins"

    def verify_price_odd_format(self, format=None):
        self.get_price_button_values()
        if self.device_type == 'desktop':
            if format == 'fractional':
                self.assertRegexpMatches(self.price_buttons, self.fractional_pattern,
                                         msg=f'Stake odds value "{self.price_buttons}" not match decimal pattern: "{self.fractional_pattern}"')
            else:
                if format == 'decimal':
                    self.assertRegexpMatches(self.price_buttons, self.decimal_pattern,
                                             msg=f'Stake odds value "{self.price_buttons}"not match decimal pattern: "{self.decimal_pattern}"')
        else:
            for selection_name, price_button in self.price_buttons:
                if price_button is not None:
                    if format == 'fractional':
                        self.assertRegexpMatches(price_button.name, self.fractional_pattern,
                                                 msg=f'Stake odds value "{price_button.name}" not match decimal pattern: "{self.fractional_pattern}"')
                    else:
                        if format == 'decimal':
                            self.assertRegexpMatches(price_button.name, self.decimal_pattern,
                                                     msg=f'Stake odds value "{price_button.name}"not match decimal pattern: "{self.decimal_pattern}"')

    def get_price_button_values(self):

        event_name = self.event_params.team1 + ' v ' + self.event_params.team2
        league_name = self.get_accordion_name_for_event_from_ss(event=self.event_resp[0])
        if self.device_type == 'mobile':
            event = self.site.sports_page.tab_content.accordions_list.get_event_from_league_by_event_id(league=league_name,
                                                                                                        event_id=self.event_id)
            self.assertTrue(event, msg=f'Event with name "{event_name}" not found')
            self.__class__.price_buttons = list(event.get_all_prices().items())
            self.assertTrue(self.price_buttons, msg='Price buttons are not displayed')
        else:
            event = list(self.site.football.sport_enhanced_multiples_carousel.items_as_ordered_dict.values())[0]
            self.assertTrue(event, msg=f'Event not found')
            self.__class__.price_buttons = event.bet_button.name
            self.assertTrue(self.price_buttons, msg='Price buttons are not displayed')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football enhanced multiples event
        """
        self.__class__.event_params = self.ob_config.add_football_event_enhanced_multiples()
        team1, team2, self.__class__.selection_ids = \
            self.event_params.team1, self.event_params.team2, self.event_params.selection_ids
        self.__class__.event_id = self.event_params.event_id
        self.__class__.selection_name = f'{team1}, {team2} {self.selection_type}'
        self.__class__.type_id = self.ob_config.football_config.specials.enhanced_multiples.type_id
        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id,
                                                                              query_builder=self.ss_query_builder)

        event_params_1 = self.ob_config.add_football_event_enhanced_multiples()
        self.__class__.eventID2 = event_params_1.event_id

        self.__class__.events_filter = self.basic_active_events_filter().add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_NAME, OPERATORS.EQUALS, "|Enhanced Multiples|"))

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.site.wait_content_state('homepage')

    def test_002_navigate_to_any_sports_page_where_enhanced_multiples_events_are_present(self, tab='today'):
        """
        DESCRIPTION: Navigate to any <Sports> page where Enhanced Multiples events are present
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        current_tab_name = self.site.football.tabs_menu.current
        expected_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is not "{expected_tab_name}", it is "{current_tab_name}"')
        if self.device_type == 'desktop':
            if tab == "today":
                actual_date_tab_name = self.site.football.date_tab.current_date_tab
                self.assertEqual(actual_date_tab_name, vec.sb.SPORT_DAY_TABS.today,
                                 msg=f'Actual date tab is "{actual_date_tab_name}" not "{vec.sb.SPORT_DAY_TABS.today}"')
            elif tab == "tomorrow":
                self.site.sports_page.date_tab.tomorrow.click()
                self.assertEqual(self.site.sports_page.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.tomorrow,
                                 msg=f'Current active tab: "{self.site.sports_page.date_tab.current_date_tab}", '
                                     f'expected: "{vec.sb.SPORT_DAY_TABS.tomorrow}"')
            else:
                self.site.sports_page.date_tab.future.click()
                self.assertEqual(self.site.sports_page.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.future,
                                 msg=f'Current active tab: "{self.site.sports_page.date_tab.current_date_tab}", '
                                     f'expected: "{vec.sb.SPORT_DAY_TABS.future}"')

    def test_003_go_to_outcome_section_of_em_event(self):
        """
        DESCRIPTION: Go to outcome section of EM event
        EXPECTED: Enhanced Multiples outcome is shown
        """
        if self.device_type == 'mobile':
            sections = self.site.football.tab_content.accordions_list.get_items(name=vec.racing.ENHANCED_MULTIPLES_NAME)
            self.assertTrue(sections, msg='No event sections are present on page')
            self.assertIn(vec.racing.ENHANCED_MULTIPLES_NAME, sections,
                          msg='No "ENHANCED MULTIPLES" section found in list')
            section = sections[vec.racing.ENHANCED_MULTIPLES_NAME]
            section.click()
            section_items = section.items_as_ordered_dict
            self.assertTrue(section_items, msg=f'No events found in event section: "{vec.racing.ENHANCED_MULTIPLES_NAME}"')
            event = section_items.get(self.selection_name)
            self.assertTrue(event, msg=f'Event "{self.selection_name}" not found in {list(section_items.keys())}')
            self.verify_event_time_is_present(event)
            self._verify_event_name(event)
            all_prices = event.get_active_prices()
            self.assertTrue(all_prices, msg=f'Event "{self.selection_name}" does not have active selections')
            self.assertEqual(event.template.event_name, self.selection_name,
                             msg=f'"{self.selection_name}" event name is clickable')
        else:
            aem_banner_section = self.site.football.aem_banner_section
            self.assertTrue(aem_banner_section, msg='AEM banner section is not present')
            enhanced_section_name = self.site.football.sport_enhanced_multiples_carousel.section_header.text
            self.assertEqual(enhanced_section_name, 'ENHANCED',
                             msg=f'Actual is "{enhanced_section_name}" not "ENHANCED"')
            enhanced_section = list(self.site.football.sport_enhanced_multiples_carousel.items_as_ordered_dict.values())
            self.assertTrue(enhanced_section, msg='No event sections are present on page')
            for event in enhanced_section:
                self.assertTrue(event.start_time, msg='Event start time is not present')

    def test_004_verify_selection_name(self):
        """
        DESCRIPTION: Verify Selection name
        EXPECTED: Selection name corresponds to **name** attribute on Outcome level
        """
        # step covered into step 3

    def test_005_verify_outcome_start_time_for_mobiletablet(self):
        """
        DESCRIPTION: Verify Outcome Start Time for **Mobile/Tablet**
        EXPECTED: *   Outcome start time corresponds to **startTime** attribute of event it belongs to
        EXPECTED: *   Outcome Start Time is shown below Outcome name
        EXPECTED: *   For outcomes that occur Today date format is 24 hours: **HH:MM, Today** (e.g. "14:00 or 05:00, Today")
        EXPECTED: *   For outcomes that occur in the future (including tomorrow) date format is 24 hours: **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        # step covered into step 3

    def test_006_verify_outcome_start_time_for_desktop(self):
        """
        DESCRIPTION: Verify Outcome Start Time for **Desktop**
        EXPECTED: *   Outcome start time corresponds to **startTime** attribute of event it belongs to
        EXPECTED: *   Outcome Start Time is shown after Outcome name in the same row
        EXPECTED: *   For outcomes that occur Today date format is 24 hours: **HH:MM, Today** (e.g. 14:00 or 05:00)
        EXPECTED: *   For outcomes that occur in the future (including tomorrow) date format is 24 hours: **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        # step covered into step 3

    def test_007_clicktap_onanywhere_on_outcome_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Click/Tap on anywhere on Outcome section (except for price buttons)
        EXPECTED: Outcome section is not clickable
        """
        # step covered into step 3

    def test_008_verify_data_of_priceodds_button_for_verified_outcome_in_fraction_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button for verified outcome in fraction format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen ** if **eventStatusCode="A"**
        EXPECTED: *   Disabled 'Price/Odds' button is displayed and corresponds to the **priceNum/priceDen ** if **eventStatusCode="S"**
        """
        self.verify_price_odd_format(format='fractional')

    def test_009_verify_data_of_priceodds_for_verified_outcome_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified outcome in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec ** if **eventStatusCode="A"**
        EXPECTED: *   Disabled 'Price/Odds' button is displayed and corresponds to the **priceNum/priceDen ** if **eventStatusCode="S"**
        """
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(result, msg='Odds format is not changed to Decimal')

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('FOOTBALL')
        self.verify_price_odd_format(format='decimal')

    def test_010_navigate_to_tomorrowfuture_tab_on_desktoptablet_where_enhanced_multiples_events_are_present(self):
        """
        DESCRIPTION: Navigate to Tomorrow/Future tab on Desktop/Tablet where Enhanced Multiples events are present
        EXPECTED: * Enhanced Multiples section for **Mobile/Tablet**
        EXPECTED: * The EM carousel is still displaying with all available outcomes for **Desktop**
        EXPECTED: * The EM carousel is not reloaded during navigation between days (Today/Tomorrow/Future) for **Desktop**
        """
        self.test_002_navigate_to_any_sports_page_where_enhanced_multiples_events_are_present(tab='tomorrow')

    def test_011_repeat_steps_3_8(self):
        """
        DESCRIPTION: Repeat steps 3-8
        EXPECTED:
        """
        self.test_003_go_to_outcome_section_of_em_event()

    def test_012_clicktap_on_enhanced_multiples_tab_from_module_selector_ribbon(self):
        """
        DESCRIPTION: Click/Tap on 'Enhanced Multiples' tab from Module Selector Ribbon
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   'Enhanced Multiples' tab is opened
        EXPECTED: *   All sections are collapsed by default
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel below banner area
        """
        # step covered into step 3

    def test_013_repeat_steps_3_9(self):
        """
        DESCRIPTION: Repeat steps №3-9
        EXPECTED:
        """
        # step covered into step 3

    def test_014_for_desktoprepeat_steps_3_9_on_sports_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 3-9 on <Sports> Event Details Page but only for Pre-match events
        EXPECTED:
        """
        # step covered into step 3
