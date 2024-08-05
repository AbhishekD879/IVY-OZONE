import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from random import choice
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C10397562_Added_for_OX98_Verify_that_Forecast_Tricast_Sections_are_added_to_the_Betslip(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C10397562
    NAME: [Added for OX98] Verify that Forecast/Tricast Sections are added to the Betslip
    DESCRIPTION: This test case verifies that Forecast/Tricast Sections are added to the Betslip (No Quick Bet )
    PRECONDITIONS: Login into Application
    PRECONDITIONS: Navigate to 'HR/Greyhounds' page
    PRECONDITIONS: Choose event -> see that Ferecast/Tricast Tab is available
    PRECONDITIONS: Navigate to Ferecast/Tricast Tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event and login
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.horseracing_config.category_id
            class_ids = self.get_class_ids_for_category(category_id=category_id)

            events_filter = self.ss_query_builder \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(
                    LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'SF,CF,RF,'))) \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(
                    LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CT,TC,'))) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE))

            ss_req = SiteServeRequests(env=tests.settings.backend_env, class_id=class_ids, brand=self.brand)
            resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
            events = [event for event in resp if event.get('event') and event['event'] and event['event'].get('children')]

            if not events:
                raise SiteServeException(f'Cannot find active Forecast/Tricast Racing events')

            event = choice(events)
            self.__class__.event_name = f'{event["event"]["name"]}'
            self.__class__.event_id = event['event']['id']
            self._logger.info(f'*** Found Horse Racing Forecast/Tricast event "{self.event_name}" with id "{self.event_id}"')
        else:
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=5,
                                                              forecast_available=True,
                                                              tricast_available=True)
            self.__class__.event_id = event_params.event_id
        self.site.login()

    def test_001___select_two_selections_in_forecast_tab_and_tap_add_to_bet_slip_button__verify_that_sections_are_added_to_the_betslip(self):
        """
        DESCRIPTION: - Select two Selections in Forecast Tab and tap "Add to bet slip" button.
        DESCRIPTION: - Verify that Sections are added to the Betslip
        EXPECTED: Sections are added to the Betslip (No Quick Bet)
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        self.place_forecast_tricast_bet_from_event_details_page(forecast=True)
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.ordered_collection.values())[0]
        self.assertEqual(stake.market_name, 'Forecast',
                         msg=f'Actual Market name "{stake.market_name}" is not the same as expected "{"Forecast"}"')

    def test_002___select_three_selections_in_tricast_tab_and_tap_add_to_bet_slip_button__verify_that_sections_are_added_to_the_betslip(self):
        """
        DESCRIPTION: - Select three Selections in Tricast Tab and tap "Add to bet slip" button.
        DESCRIPTION: - Verify that Sections are added to the Betslip
        EXPECTED: Sections are added to the Betslip (No Quick Bet)
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        self.place_forecast_tricast_bet_from_event_details_page(tricast=True)
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.ordered_collection.values())[1]
        self.assertEqual(stake.market_name, 'Tricast',
                         msg=f'Actual Market name "{stake.market_name}" is not the same as expected "{"Tricast"}"')
