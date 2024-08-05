import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.sports
@pytest.mark.markets
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.safari
@vtest
class Test_C28446_Verify_number_of_available_markets_Markets_link(BaseSportTest):
    """
    TR_ID: C28446
    NAME: Verify '<number of available markets> Markets' link
    DESCRIPTION: This test case verifies '<number of available markets> Markets' ('+<number of available markets> Markets' for desktop) link on the Event section.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            events_with_more_than_one_market = []
            for event in events:
                if event.get('event') and event['event'].get('children'):
                    markets = event['event']['children']
                    if len(markets) > 1:
                        events_with_more_than_one_market.append(event)
                        break

            if not events_with_more_than_one_market:
                raise SiteServeException('There are no available football events with more than one market')

            event1 = events_with_more_than_one_market[0]['event']
            self.__class__.extra_markets_event1 = event1['children']

            self.__class__.eventID_two_markets = event1['id']
            self.__class__.event_with_two_markets_name = event1['name']
            self.__class__.section_name = self.get_accordion_name_for_event_from_ss(
                event=events_with_more_than_one_market[0])
        else:
            self.__class__.extra_markets_event1 = [('both_teams_to_score', {'cashout': True})]
            event_with_two_markets = self.ob_config.add_autotest_premier_league_football_event(
                markets=self.extra_markets_event1)
            self.__class__.eventID_two_markets = event_with_two_markets.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_two_markets,
                                                                   query_builder=self.ss_query_builder)
            self.__class__.event_with_two_markets_name = normalize_name(event_resp[0]['event']['name'])
            self._logger.info(f'*** Created Football event "{self.event_with_two_markets_name}"')

            event_with_one_market = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_one_market = event_with_one_market.event_id
            event_resp2 = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_one_market,
                                                                    query_builder=self.ss_query_builder)
            self.__class__.event_with_one_market_name = normalize_name(event_resp2[0]['event']['name'])
            self._logger.info(f'*** Created Football event "{self.event_with_one_market_name}"')

            self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> landing page
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

        current_tab_name = self.site.football.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.football_config.category_id)
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is "{current_tab_name}", instead of "{expected_tab_name}"')

    def test_003_verify_number_of_available_markets_markets_link_for_event_with_several_markets(self):
        """
        DESCRIPTION: Verify '<number of available markets> Markets' ('+<number of available markets> Markets' for desktop) link for event with several markets
        EXPECTED: For mobile/tablet view:
        EXPECTED: '+<number of available markets> Markets' is shown below odds buttons
        EXPECTED: For desktop view:
        EXPECTED: '<number of available markets> Markets' is shown next to odds buttons
        """
        self.__class__.event = self.get_event_from_league(event_id=self.eventID_two_markets,
                                                          section_name=self.section_name)
        more_market_link_label = self.event.get_markets_count_string()

        y_location_of_odd_button = self.event.second_player_bet_button.location['y'] + \
            self.event.second_player_bet_button.size['height']
        y_location_of_more_markets_link = self.event.more_markets_link.location['y'] + \
            self.event.more_markets_link.size['height']

        if self.device_type == 'desktop' or self.brand == 'ladbrokes':
            self.assertTrue(y_location_of_odd_button >= y_location_of_more_markets_link,
                            msg=f'"{more_market_link_label}" should not be below odds buttons')
        else:
            self.assertTrue(y_location_of_odd_button < y_location_of_more_markets_link,
                            msg=f'"{more_market_link_label}" is not below odds buttons')

    def test_004_verify_number_of_extra_markets_in_brackets(self):
        """
        DESCRIPTION: Verify number of extra markets in brackets
        EXPECTED: Number of markets corresponds to:
        EXPECTED: 'Number of all markets - **1**'
        """
        markets_count = self.event.get_markets_count()
        expected_count = len(self.extra_markets_event1) - 1 if tests.settings.backend_env == 'prod' else len(self.extra_markets_event1)
        self.assertEqual(markets_count, expected_count,
                         msg=f'Number of markets present in "MORE" link: "{markets_count}" '
                             f'is not equal to expected: "{expected_count}"')

    def test_005_tap_on_number_of_available_markets_markets_link(self):
        """
        DESCRIPTION: Tap on '<number of available markets> Markets' ('+<number of available markets> Markets' for desktop) link
        EXPECTED: Event Details page opened
        """
        self.event.more_markets_link.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_006_verify_plus_number_of_available_markets_markets_link_for_event_with_only_one_market(self):
        """
        DESCRIPTION: Verify '<number of available markets> Markets' ('+<number of available markets> Markets' for desktop) link for event with ONLY one market
        EXPECTED: Link is not shown on the Event section
        """
        if tests.settings.backend_env != 'prod':
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state(state_name='football')

            event = self.get_event_from_league(event_id=self.eventID_one_market,
                                               section_name=self.section_name)

            self.assertFalse(event.has_markets(expected_result=False),
                             msg=f'There is at least one extra market for '
                                 f'"{self.event_with_one_market_name}". It should not be.')
        else:
            self._logger.info('Not applicable for PROD, not likely event with one market will be present')
