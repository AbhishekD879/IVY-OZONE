import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from crlat_ob_client.utils.date_time import validate_time


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.lad_beta2
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.mobile_only
@vtest
class Test_C2989745_Ladbrokes_Verify_Horse_Racing_Specials_EDP_view(BaseRacing):
    """
    TR_ID: C2989745
    VOL_ID: C24282099
    NAME: [Ladbrokes] Verify Horse Racing Specials EDP view
    DESCRIPTION: This test case verifies Navigation and View of Horse Racing Specials EDP page
    PRECONDITIONS: To retrieve an information from the Site Server (tst2) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/*X.XX */EventToOutcomeForClass/227?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Class id = *id* for Racing Specials class
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create specials races
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_racing_specials_event(number_of_runners=2,
                                                     ew_terms=self.ew_terms, time_to_start=20)
        else:
            events_list = self.get_racing_event_with_form_details(specials=True)
            self.assertTrue(events_list, msg='No events found in Horse Racing')

    def test_001_navigate_to_horse_racing__specials_tab(self):
        """
        DESCRIPTION: Navigate to Horse Racing > Specials tab
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        specials = vec.racing.RACING_SPECIALS_TAB_NAME
        self.site.horse_racing.tabs_menu.click_button(specials)
        self.assertTrue(self.site.horse_racing.tabs_menu.items_as_ordered_dict.get(specials).is_selected(),
                        msg='Specials tab is not present')

    def test_002_click_on_some_event_in_specials_accordion(self):
        """
        DESCRIPTION: Click on some event in Specials accordion
        EXPECTED: User is navigated to Specials EDP
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found on Specials tab')
        self.__class__.first_section_name, first_section = list(sections.items())[0]
        first_section.expand()
        first_section_events = self.site.horse_racing.special_races.items_as_ordered_dict
        self.assertTrue(first_section_events, msg='Special tab has no events')
        self.__class__.event_name, event = list(first_section_events.items())[0]
        event.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
        current = self.device.get_current_url()
        expected_value = 'racing-specials'
        self.assertIn(expected_value, current, msg='User is not navigated to Specials EDP')

    def test_003_verify_specials_edp_view(self):
        """
        DESCRIPTION: Verify Specials EDP view
        EXPECTED: Header:
        EXPECTED: - Event name and time displayed. Time in Format "Day-of-the-week Date Month Year"
        EXPECTED: Market section:
        EXPECTED: - Header with Market name expandable/collapsible
        EXPECTED: - Selections with prices displayed under header. No silks or runner numbers.
        """
        event_title = self.site.racing_event_details.tab_content.race_details.event_title_name.strip()
        self.assertEquals(event_title, self.event_name,
                          msg=f'Actual Event title "{event_title}" '
                          f'is not same as Expected event title "{self.event_name}"')

        race_time = self.site.racing_event_details.tab_content.race_details.event_title_time
        self.assertTrue(race_time, msg='Event time is not displayed')
        format_pattern = self.get_time_format_pattern_for_desktop(race_time)
        result = validate_time(actual_time=race_time, format_pattern=format_pattern + ' %Y')
        self.assertTrue(result, msg=f'Actual time pattern "{race_time}" '
                                    f'is not same as Expected time pattern "{format_pattern}"')

        race_market = self.site.racing_event_details.tab_content.event_markets_list.market_name
        self.assertTrue(race_market, msg='Header with Market name is not present')
        race_market.click()
        is_header_expanded = self.site.racing_event_details.tab_content.event_markets_list.is_expanded(expected_result=False)
        self.assertFalse(is_header_expanded, msg='Header with Market name is not collapsed')
        race_market.click()
        is_header_expanded = self.site.racing_event_details.tab_content.event_markets_list.is_expanded()
        self.assertTrue(is_header_expanded, msg='Header with Market name is not expanded')

        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets with outcomes found')
        for market_name, market in markets.items():
            outcomes = market.items_as_ordered_dict
            self.assertTrue(outcomes, msg=f'No outcomes found for "{market_name}"')
            for outcome_name, outcome in outcomes.items():
                self.assertFalse(outcome.has_silks, msg=f'Silk icon is displayed for outcome: "{outcome_name}"')
                self.assertFalse(outcome.runner_number, msg=f'Runner numbers is displayed for outcome: "{outcome_name}"')
                self.assertTrue(outcome.bet_button, msg=f'Bet Button is not displayed for outcome: "{outcome_name}"')
