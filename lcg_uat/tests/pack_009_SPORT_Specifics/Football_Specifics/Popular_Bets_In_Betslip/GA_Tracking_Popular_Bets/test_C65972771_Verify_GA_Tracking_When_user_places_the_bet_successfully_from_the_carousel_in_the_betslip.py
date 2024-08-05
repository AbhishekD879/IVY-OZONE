import json
import pytest
from tests.base_test import vtest
import tests
from random import choice
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.utils.helpers import normalize_name, do_request
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.navigation
@pytest.mark.adhoc_suite
@pytest.mark.trending_bets
@pytest.mark.mobile_only
@vtest
class Test_C65972771_Verify_GA_Tracking_When_user_places_the_bet_successfully_from_the_carousel_in_the_betslip(BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C65972771
    NAME: Verify GA Tracking When user places the bet successfully from the carousel in the betslip
    DESCRIPTION: This test case is to verify GA Tracking When user places the bet successfully from the carousel in the betslip
    PRECONDITIONS: Should have Football events
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    headers = {'Content-Type': 'application/json'}

    def verify_tracking(self):
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='betslip')
        expected_response = {
            'ecommerce': {
                'purchase': {
                    'actionField': {
                        'id': self.bet_receipt_id + ':1',
                        'revenue': self.bet_amount
                    },
                    'products': [
                        {
                            'brand': self.market_name,
                            'category': self.category_id,
                            'dimension60': self.event_id,
                            'dimension61': self.selection_id,
                            'dimension62': 0,
                            'dimension63': 0,
                            'dimension64': 'betslip',
                            'dimension65': 'trending upsell module',
                            'dimension66': 1,
                            'dimension67': self.odds,
                            'dimension86': 0,
                            'dimension87': 0,
                            'dimension166': 'normal',
                            'dimension180': 'normal',
                            'dimension88': None,
                            'metric1': 0,
                            'id': self.bet_receipt_id,
                            'name': self.event_name,
                            'price': self.bet_amount,
                            'quantity': 1,
                            'variant': int(self.type_id)
                        }
                    ]
                }
            },
            'event': 'trackEvent',
            'eventAction': 'place bet',
            'eventCategory': 'betslip',
            'eventLabel': 'success',
            'location': '/sport/football'
        }
        self.compare_json_response(actual_response, expected_response)

    def get_outcome_details(self):
        url = f'{tests.settings.BETTINGMS}v1/buildBet'
        placebet_request = self.get_web_socket_response_by_url(url=url)
        post_data = placebet_request.get('postData')
        self.assertTrue(post_data, msg='Post Data is not found in placeBet request')
        legs = post_data.get('leg')
        self.assertTrue(legs, msg='No Legs found in placeBet request')
        for leg in legs:
            sports_leg = leg.get('sportsLeg')
            self.assertTrue(sports_leg, msg='No sportsLeg found in placeBet request')
            price = sports_leg.get('price')
            self.assertTrue(price, msg='No price found in placeBet request')
            price_type_ref = price.get('priceTypeRef')
            self.assertTrue(price_type_ref, msg='No priceTypeRef found in placeBet request')
        data = json.dumps(post_data)
        req = do_request(url=url, data=data, headers=self.headers)
        outcome_details = req['outcomeDetails']
        return outcome_details

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        DESCRIPTION: Find / create event for test
        EXPECTED: User is logged in
        EXPECTED: Event is found / created
        """
        trending_carousel_status = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('active')
        if not trending_carousel_status:
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
        self.assertTrue(self.site.betslip.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available in betslip')

    def test_005_add_any_selection_from_the_trending_bets_carousel_and_place_a_bet(self):
        """
        DESCRIPTION: Add any selection from the trending bets carousel and place a bet
        EXPECTED: Able to add and place a bet successfully
        """
        trending_bet_section = self.site.betslip.trending_bets_section
        bet_card_info = list(trending_bet_section.items_as_ordered_dict.values())[0]
        bet_card_info.scroll_to()
        self.__class__.bet_name = bet_card_info.name
        self.__class__.event_name = bet_card_info.event_name
        bet_card_info.odd.click()
        singles_section = self.get_betslip_sections().Singles
        for selection_name, selection in singles_section.items():
            self._logger.debug(f'*** Verifying stake "{selection.outcome_name}"')
            if self.bet_name == selection_name:
                selection.amount_form.input.click()
                self.assertTrue(
                    self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown',
                                                                     timeout=3),
                    msg='Betslip keyboard is not shown')
                betnow_btn = self.get_betslip_content().bet_now_button
                self.assertTrue(betnow_btn.is_displayed(), msg='Bet Now button is not disabled')
                self.enter_stake_amount(stake=(selection_name, selection))
                betnow_btn = self.get_betslip_content().bet_now_button
                self.assertTrue(betnow_btn.is_enabled(timeout=2), msg='Bet Now button is not enabled')
                self.get_betslip_content().bet_now_button.click()
                wait_for_haul(10)
                outcome_details =self.get_outcome_details()
                for outcome in outcome_details:
                    if self.bet_name == outcome['name']:
                        self.__class__.type_id = outcome['typeId']
                        self.__class__.category_id = outcome['categoryId']
                        self.__class__.selection_id = outcome['id']
                        self.__class__.event_name = outcome['eventDesc']
                        self.__class__.event_id = outcome['eventId']
                        self.__class__.price_num = outcome['priceNum']
                        self.__class__.price_den = outcome['priceDen']
                        break
                self.__class__.bet_receipt_id = self.site.bet_receipt.bet_id
                odds_value = self.site.bet_receipt.item_odds
                odds_value.split(maxsplit=1)[1] if '@' in odds_value else odds_value
                odds =int(self.price_num)/int(self.price_den)
                float_num = float(odds) + 1
                self.__class__.odds = round(float_num, 2)
                market_type = self.site.bet_receipt.market_type
                self.__class__.market_name = market_type.rstrip('/ ')

    def test_006_verify_ga_tracking_in_console(self):
        """
        DESCRIPTION: Verify GA tracking in console
        EXPECTED: dataLayer.push({
        EXPECTED: /'event': 'trackEvent',
        EXPECTED: [{
        EXPECTED: eventCategory: "betslip",
        EXPECTED: eventAction: "place bet",
        EXPECTED: eventLabel: "success",
        EXPECTED: location: "/",
        EXPECTED: ecommerce: {
        EXPECTED: purchase: {
        EXPECTED: actionField: {
        EXPECTED: id: "O/24751062/0000435",
        EXPECTED: revenue: 1
        EXPECTED: },
        EXPECTED: products: [
        EXPECTED: {
        EXPECTED: dimension64: "betslip",
        EXPECTED: dimension65: "trending upsell module",
        EXPECTED: name: "single",
        EXPECTED: id: "O/24751062/0000435",
        EXPECTED: price: 1,
        EXPECTED: category: "34",
        EXPECTED: variant: "50483",
        EXPECTED: brand: "Match Betting",
        EXPECTED: dimension60: "26955036",
        EXPECTED: dimension61: "2116937856",
        EXPECTED: dimension62: 0,
        EXPECTED: dimension63: 0,
        EXPECTED: dimension66: 1,
        EXPECTED: dimension67: 2.25,
        EXPECTED: dimension86: 0,
        EXPECTED: dimension87: 0,
        EXPECTED: dimension88: null,
        EXPECTED: metric1: 0
        EXPECTED: }
        EXPECTED: ]
        EXPECTED: }}
        EXPECTED: }]
        EXPECTED: });
        """
        self.verify_tracking()

    def test_007_verify_the_newly_added_parameters_dimension64_and_dimension65(self):
        """
        DESCRIPTION: Verify the newly added parameters dimension64 and dimension65
        EXPECTED: 
        """
        #covered in above step
