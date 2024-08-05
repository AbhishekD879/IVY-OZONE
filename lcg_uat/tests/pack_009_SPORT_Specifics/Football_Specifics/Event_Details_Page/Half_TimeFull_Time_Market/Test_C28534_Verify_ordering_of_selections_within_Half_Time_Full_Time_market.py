import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28534_Verify_ordering_of_selections_within_Half_Time_Full_Time_market(BaseSportTest):
    """
    TR_ID: C28534
    NAME: Verify ordering of selections within 'Half Time/Full Time' market
    DESCRIPTION: This test case verifies ordering of selections within 'Half Time/Full Time' market
    DESCRIPTION: Test case needs to be run on Mobile/Tablet/Desktop.
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
            PRECONDITIONS: Create a event
        """
        self.__class__.market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.half_time_full_time

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)

            for event in events:
                for market in event['event']['children']:
                    if market.get('market').get('templateMarketName') == self.market_name:
                        self.__class__.eventID = market.get('market').get('eventId')
                        self.__class__.team1, self.__class__.team2 = event.get('event').get('name').split('v')[0].strip(), \
                                                                     event.get('event').get('name').split('v')[1].strip()
                        break
            if self.eventID is None:
                raise SiteServeException('There are no available market with Half-time/Full-time market')
        else:
            markets_params = [('half_time_full_time', {'cashout': True})]
            event = self.ob_config.add_autotest_premier_league_football_event(markets=markets_params)
            self.__class__.eventID = event.event_id
            self.__class__.team1, self.__class__.team2 = event.team1, event.team2

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(self.eventID, timeout=60)
        self.site.wait_content_state(state_name='EventDetails', timeout=60)

        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(self.markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)

        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

    def test_003_verify_order_within_market_section(self):
        """
        DESCRIPTION: Verify order within market section
        EXPECTED: Section is ordered in following way:
        EXPECTED: * <Home/Home>
        EXPECTED: * < Home/Draw>
        EXPECTED: * <Home/Away>
        EXPECTED: * <Draw/Home>
        EXPECTED: * <Draw/Draw>
        EXPECTED: * <Draw/Away>
        EXPECTED: * <Away/Home>
        EXPECTED: * <Away/Draw>
        EXPECTED: * <Away/Away>
        """
        if self.brand == 'ladbrokes':
            market = 'Half Time / Full Time' if tests.settings.backend_env == 'prod' else 'Half time/ Full Time Result Market'
        else:
            market = 'HALF TIME/ FULL TIME RESULT MARKET' if self.device_type == 'mobile' else 'Half Time/ Full Time Result Market'

        self.__class__.half_time_full_time = self.markets_list.get(market)

        self.half_time_full_time.expand()
        self.assertTrue(self.half_time_full_time.is_expanded(),
                        msg=f'"{market}" section is not expanded')

        outcomes = self.markets_list[market].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')

        ui_outcome_name = []
        for outcome_name, outcome in outcomes.items():
            ui_outcome_name.append(outcome_name)

        expected_outcome_name = ['%s/%s' % (self.team1, self.team1),
                                 '%s/Draw' % self.team1,
                                 '%s/%s' % (self.team1, self.team2),
                                 'Draw/%s' % self.team1,
                                 'Draw/Draw',
                                 'Draw/%s' % self.team2,
                                 '%s/%s' % (self.team2, self.team1),
                                 '%s/Draw' % self.team2,
                                 '%s/%s' % (self.team2, self.team2)]

        self.assertListEqual(ui_outcome_name, expected_outcome_name,
                             msg=f'Section ordering in UI "{ui_outcome_name}" is not same as expected section "{expected_outcome_name}"')
