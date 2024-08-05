import pytest
from tests.base_test import vtest
import tests
from random import choice
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.utils.helpers import normalize_name
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.navigation
@pytest.mark.trending_bets
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@vtest
class Test_C65972769_Verify_GA_Tracking_When_user_gets_carousel_in_the_betslip(BaseDataLayerTest):
    """
    TR_ID: C65972769
    NAME: Verify GA Tracking When user gets carousel in the betslip
    DESCRIPTION: This test case is to verify GA Tracking when user gets carousel in the betslip
    PRECONDITIONS: Should have Football events
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        DESCRIPTION: Find / create event for test
        EXPECTED: User is logged in
        EXPECTED: Event is found / created
        """
        get_trending_carousel_status = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('active')
        if not get_trending_carousel_status:
            self.cms_config.update_most_popular_or_trending_bets_bet_slip_config(active=True)
        if tests.settings.backend_env == 'prod':
            additional_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)
            event = self.get_active_events_for_category(
                category_id=self.ob_config.football_config.category_id, additional_filters=additional_filter)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.event_id = event['event']['id']
            self.__class__.league = self.get_accordion_name_for_event_from_ss(event=event)
            self._logger.info(f'*** Found Football event "{self.event_name}" with ID "{self.event_id}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = f'{event.team1} v {event.team2}'
            self.__class__.event_id = event.event_id
            self.__class__.league = tests.settings.football_autotest_league
            self._logger.info(f'*** Created Football event "{self.event_name}" with ID "{self.event_id}"')

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: User should launch the Application Successfully
        """
        self.site.login()

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

    def test_003_add_any_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add any selection to the Betslip
        EXPECTED: Able to add the selection to the Betslip
        """
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for event "{self.event_name}"')
        selection = choice(list(output_prices.keys()))
        bet_button = output_prices.get(selection)
        self.assertTrue(bet_button, msg=f'Bet button for "{selection}" was not found')
        bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip(timeout=3)

    def test_004_navigate_to_betslip_page_and_verify_the_trending_bets_carousel(self):
        """
        DESCRIPTION: Navigate to Betslip Page and verify the trending bets carousel
        EXPECTED: Able to navigate to the Betslip and can see the trending bets carousel
        """
        self.site.open_betslip()
        self.assertTrue(self.site.betslip.has_trending_bet_carousel(), msg=f'Trending Bets Carousel section is not available')
        wait_for_haul(10)

    def test_005_verify_ga_tracking_in_console(self):
        """
        DESCRIPTION: Verify GA tracking in console
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'contentView',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'upsell',
        EXPECTED: component.LabelEvent: 'sports upsell',
        EXPECTED: component.ActionEvent: 'load',
        EXPECTED: component.PositionEvent: 'not applicable',
        EXPECTED: component.LocationEvent: 'betslip',
        EXPECTED: component.EventDetails: 'trending upsell module',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        expected_resp = {
         'event': 'contentView',
         'component.CategoryEvent': 'upsell',
         'component.LabelEvent': 'sports upsell',
         'component.ActionEvent': 'load',
         'component.PositionEvent': 'not applicable',
         'component.LocationEvent': 'betslip',
         'component.EventDetails': 'trending upsell module',
         'component.URLClicked': 'not applicable'
        }
        actual_resp = self.get_data_layer_specific_object(object_key='component.EventDetails', object_value='trending upsell module')
        self.compare_json_response(actual_resp, expected_resp)


