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
class Test_C2989783_Ladbrokes_Verify_Greyhounds_Specials_EDP_view(BaseRacing):
    """
    TR_ID: C2989783
    NAME: [Ladbrokes] Verify Greyhounds Specials EDP view
    DESCRIPTION: This test case verifies Navigation and View of Greyhounds Specials EDP page
    PRECONDITIONS: To retrieve an information from the Site Server (tst2) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/*X.XX */EventToOutcomeForClass/227?translationLang=LL
    PRECONDITIONS: Where X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Class id = *id* for Racing Specials class ('Specials' checkbox should be checked in Flags on Type and Class level)
    PRECONDITIONS: **The full request to check data:**
    PRECONDITIONS: Ladbrokes
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T14:17:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: Coral
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-26T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-08-27T00:00:00.000Z&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T13:35:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
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
            event_params = self.get_event_details(specials=True)
            event_id = event_params.event_id
            self.assertTrue(event_id, msg='No events found in grayhounds Racing')

    def test_001_navigate_to_greyhounds__specials_tab(self):
        """
        DESCRIPTION: Navigate to Greyhounds > Specials tab
        EXPECTED:
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('greyhoundracing')
        specials = vec.racing.RACING_SPECIALS_TAB_NAME
        self.site.greyhound.tabs_menu.click_button(specials)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(specials).is_selected(),
                        msg='Specials tab is not present')

    def test_002_click_on_some_event_in_specials_accordion(self):
        """
        DESCRIPTION: Click on some event in Specials accordion
        EXPECTED: User is navigated to Specials EDP
        """
        sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found on Specials tab')
        first_section_name, first_section = list(sections.items())[0]
        first_section.expand()
        first_section_events = self.site.greyhound.special_races.items_as_ordered_dict
        self.assertTrue(first_section_events, msg='Special tab has no events')
        self.__class__.event_name, event = list(first_section_events.items())[0]
        event.click()
        current = self.device.get_current_url()
        expected_value = 'greyhounds-specials'
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
        event_title = self.site.greyhound_event_details.tab_content.race_details.event_title.strip()
        self.assertEquals(event_title, self.event_name,
                          msg=f'Actual Event title "{event_title}" '
                          f'is not same as Expected event title "{self.event_name}"')

        race_time = self.site.greyhound_event_details.tab_content.race_details.race_time
        self.assertTrue(race_time, msg='Event time is not displayed')
        format_pattern = self.get_time_format_pattern_for_desktop(race_time)
        result = validate_time(actual_time=race_time, format_pattern=format_pattern + ' %Y')
        self.assertTrue(result, msg=f'Actual time pattern "{race_time}" '
                                    f'is not same as Expected time pattern "{format_pattern}"')

        race_market = self.site.greyhound_event_details.tab_content.event_markets_list.market_name
        self.assertTrue(race_market, msg='Header with Market name is not present')
        race_market.click()
        is_header_expanded = self.site.greyhound_event_details.tab_content.event_markets_list.is_expanded(expected_result=False)
        self.assertFalse(is_header_expanded, msg='Header with Market name is not collapsed')
        race_market.click()
        is_header_expanded = self.site.greyhound_event_details.tab_content.event_markets_list.is_expanded()
        self.assertTrue(is_header_expanded, msg='Header with Market name is not expanded')

        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets with outcomes found')
        for market_name, market in markets.items():
            outcomes = market.items_as_ordered_dict
            self.assertTrue(outcomes, msg=f'No outcomes found for "{market_name}"')
            for outcome_name, outcome in outcomes.items():
                self.assertFalse(outcome.has_silks, msg=f'Silk icon is displayed for outcome: "{outcome_name}"')
                self.assertFalse(outcome.runner_number, msg=f'Runner numbers is displayed for outcome: "{outcome_name}"')
                self.assertTrue(outcome.bet_button, msg=f'Bet Button is not displayed for outcome: "{outcome_name}"')
