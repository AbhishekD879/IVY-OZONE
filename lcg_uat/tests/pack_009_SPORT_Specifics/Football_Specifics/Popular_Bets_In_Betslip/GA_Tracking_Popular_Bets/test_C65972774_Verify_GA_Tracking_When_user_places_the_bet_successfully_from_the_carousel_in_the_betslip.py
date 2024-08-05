import json
import re
import pytest
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from random import choice
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
import voltron.environments.constants as vec
from voltron.utils.helpers import do_request
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.navigation
@pytest.mark.trending_bets
@pytest.mark.adhoc_suite
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65972774_Verify_GA_Tracking_When_user_places_the_bet_successfully_from_the_carousel_from_bet_receipt_to_betslip(BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C65972774
    NAME: Verify GA Tracking When user places the bet successfully from the carousel from bet receipt to the betslip
    DESCRIPTION: This test case is to verify GA Tracking When user places the bet successfully from the carousel in the betslip
    PRECONDITIONS: Should have Football events
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    bet_amount = 0.1
    headers = {'Content-Type': 'application/json'}
    enable_bs_performance_log = True
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

    def verify_tracking(self, category_id, selection_id, type_id, bet_id, odds, market_name,event_name,belongs_inplay=0 ):

        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='betslip')
        event_id = actual_response[u'ecommerce'][u'purchase'][u'products'][0]['dimension60']
        self.assertTrue(re.match(r'[0-9]+', event_id),
                        msg='Event id "%s" has incorrect format.\nExpected format: "xxxxxxx"' % event_id)

        expected_response = {
            'ecommerce': {
                'purchase': {
                    'actionField': {
                        'id': bet_id+':1',
                        'revenue': self.bet_amount
                    },
                    'products': [
                        {
                            'brand': market_name,
                            'category': str(category_id),
                            'dimension60': str(event_id),
                            'dimension61': str(selection_id),
                            'dimension62': belongs_inplay,
                            'dimension63': 0,
                            'dimension64': 'bet receipt',
                            'dimension65': 'trending upsell module',
                            'dimension66': 1,
                            'dimension67': odds,
                            'dimension86': 0,
                            'dimension166': 'normal',
                            'dimension180': 'normal',
                            'dimension87': 0,
                            'dimension88': None,
                            'metric1': 0,
                            'id': bet_id,
                            'name': event_name,
                            'price': self.bet_amount,
                            'variant': int(type_id),
                            'quantity': 1
                        }
                    ]
                }
            },
            'event': 'trackEvent',
            'eventAction': 'place bet',
            'eventCategory': 'betslip',
            'eventLabel': 'success',
            'location': self.modified_url
        }
        self.compare_json_response(actual_response, expected_response)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        DESCRIPTION: Find / create event for test
        EXPECTED: User is logged in
        EXPECTED: Event is found / created
        """
        trending_carousel = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('active')
        if not trending_carousel:
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
                        msg=f'Trending Bets Carousel section is not available')

    def test_005_add_any_selection_from_the_trending_bets_carousel_and_place_a_bet(self):
        """
        DESCRIPTION: Add any selection from the trending bets carousel and place a bet
        EXPECTED: Able to add and place a bet successfully
        """
        trending_bet = list(self.site.betslip.trending_bets_section.items_as_ordered_dict.values())
        if len(trending_bet) >= 1:
            trending_bet[0].scroll_to()
            self.__class__.trending_bet_name = trending_bet[0].name
            self.__class__.trending_bet_event_name = re.sub(r'^\d{2}:\d{2}\s', '', trending_bet[0].event_name)
            self.__class__.trending_bet_market_name = trending_bet[0].market_name
            trending_bet[0].odd.click()
            # trending bets verification in betslip
            singles_section = self.get_betslip_sections().Singles
            for stake_name, stake in singles_section.items():
                self._logger.debug(f'*** Verifying stake "{stake.outcome_name}"')
                if self.trending_bet_name.upper() == stake_name.upper():
                    betslip_trending_name = stake.outcome_name
                    self.assertEqual(betslip_trending_name, self.trending_bet_name,
                                     msg=f'betslip trending name {betslip_trending_name} is not equal to trending bet name {self.trending_bet_name}')
                    betslip_trending_event_name = stake.event_name
                    if betslip_trending_event_name == self.trending_bet_event_name:
                        self.assertEqual(betslip_trending_event_name, self.trending_bet_event_name,
                                        msg=f'betslip trending event name {betslip_trending_event_name} is not equal to trending bet  event name {self.trending_bet_event_name}')
                    else:
                        self.assertEqual(betslip_trending_event_name, self.trending_bet_name,
                                         msg=f'betslip trending event name {betslip_trending_event_name} is not equal to trending bet  event name {self.trending_bet_name}')
                    betslip_trending_market_name = stake.market_name
                    self.assertEqual(betslip_trending_market_name, self.trending_bet_market_name,
                                     msg=f'betslip trending market name {betslip_trending_market_name} is not equal to trending bet market name {self.trending_bet_market_name}')
                    stake.amount_form.input.click()
                    betslip_content = self.get_betslip_content()
                    self.assertTrue(
                        betslip_content.keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                        msg='Betslip keyboard is not shown')
                    betnow_btn = betslip_content.bet_now_button
                    self.assertFalse(betnow_btn.is_enabled(expected_result=False, timeout=1),
                                    msg='Bet Now button is not disabled or enabled')
                    self.enter_stake_amount(stake=(stake_name, stake))
                    betnow_btn = betslip_content.bet_now_button
                    self.assertTrue(betnow_btn.is_enabled(timeout=2), msg='Bet Now button is not enabled')
                    betnow_btn.click()

    def test_006_verify_the_betreceipt(self):
        """
        DESCRIPTION: Verify the Betreceipt
        EXPECTED: Able to see the trending bets carousel in Betreceipt
        """
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        # Trending bets verification in bet receipt
        for section_name, section in betreceipt_sections.items():
            if section_name == vec.betslip.SINGLE:
                receipts = section.items_as_ordered_dict
                self.assertTrue(receipts, msg='No Receipt legs found')
                for receipt_name, receipt in receipts.items():
                    if self.trending_bet_name == receipt_name:
                        betreceipt_event_name = receipt.event_name
                        if betreceipt_event_name == self.trending_bet_event_name:
                            self.assertEqual(betreceipt_event_name, self.trending_bet_event_name,
                                         msg=f'bet-receipt trending name {betreceipt_event_name} is not equal to trending bet name {self.trending_bet_event_name}')
                        else:
                            self.assertEqual(betreceipt_event_name, self.trending_bet_name,
                                             msg=f'bet-receipt trending name {betreceipt_event_name} is not equal to trending bet name {self.trending_bet_name}')

    def test_007_add_any_bet_from_the_carousel_in_the_betreceipt_and_place_a_bet(self):
        """
        DESCRIPTION: Add any bet from the carousel in the betreceipt and place a bet
        EXPECTED: Able to add and place a bet successfully
        """
        betreceipt_trending_bet = list(self.site.bet_receipt.trending_bets_section.items_as_ordered_dict.values())
        if len(betreceipt_trending_bet) >= 1:
            betreceipt_trending_bet[0].scroll_to()
            self.__class__.betreceipt_trending_bet = betreceipt_trending_bet[0].name
            self.__class__.betreceipt_trending_bet_event_name = re.sub(r'^\d{2}:\d{2}\s', '',
                                                                       betreceipt_trending_bet[0].event_name)
            self.__class__.betreceipt_trending_bet_market_name = betreceipt_trending_bet[0].market_name
            betreceipt_trending_bet[0].odd.click()
            wait_for_haul(10)
            # Here we are taking category id,selection id etc...from build bet call
            outcome_details = self.get_outcome_details()
            for outcome in outcome_details:
                if self.betreceipt_trending_bet == outcome['name']:
                    self.__class__.trending_bet_type_id = outcome['typeId']
                    self.__class__.trending_bet_category_id = outcome['categoryId']
                    self.__class__.tending_bet_selection_id = outcome['id']
                    self.__class__.trending_bet_event_name = outcome['eventDesc']
                    self.__class__.trending_bet_market_name = outcome['marketDesc']
                    self.__class__.price_num = outcome['priceNum']
                    self.__class__.price_den = outcome['priceDen']
                    break
            singles_section = self.get_betslip_sections().Singles
            for selection_name, selection in singles_section.items():
                self._logger.debug(f'*** Verifying stake "{selection.outcome_name}"')
                # verifying trending bet in betslip where we click on trending bets from bet receipt
                if self.betreceipt_trending_bet == selection_name:
                    selection.click()
                    self.__class__.dialog = self.site.wait_for_dialog(
                        dialog_name=vec.dialogs.DIALOG_MANAGER_SELECTION_INFORMATION, timeout=10, verify_name=False)
                    self.assertTrue(self.dialog,
                                    msg=f'"{vec.dialogs.DIALOG_MANAGER_SELECTION_INFORMATION}" dialog is not displayed')
                    if selection_name.upper() == self.dialog.name.upper():
                        self.dialog.selection_content.click()
                        if self.site.wait_for_stream_and_bet_overlay(timeout=10):
                            self.site.stream_and_bet_overlay.close_button.click()
                        current_url = self.device.get_current_url()
                        prefix = f'https://{tests.HOSTNAME}'
                        index = current_url.find(prefix)
                        # Remove the prefix if found
                        if index != -1:
                            self.__class__.modified_url = current_url[index + len(prefix):]
                        self.site.open_betslip()
            # place bet
            for stake_name, stake in singles_section.items():
                self._logger.debug(f'*** Verifying stake "{stake.outcome_name}"')
                if self.betreceipt_trending_bet == stake_name:
                    stake.amount_form.input.click()
                    betslip_content = self.get_betslip_content()
                    self.assertTrue(
                        betslip_content.keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                        msg='Betslip keyboard is not shown')
                    betnow_btn = betslip_content.bet_now_button
                    self.assertFalse(betnow_btn.is_enabled(expected_result=False, timeout=1),
                                     msg='Bet Now button is not disabled or enabled')
                    self.enter_stake_amount(stake=(stake_name, stake))
                    betnow_btn = betslip_content.bet_now_button
                    self.assertTrue(betnow_btn.is_enabled(timeout=2), msg='Bet Now button is not enabled')
                    betnow_btn.click()

    def test_008_verify_ga_tracking_in_console(self):
        """
        DESCRIPTION: Verify GA tracking in console
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
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
        EXPECTED: dimension64: "{bet receipt/quick bet receipt}",//ex:if user adds bet from quick bet receipt then dimension64=quick bet receipt, if user adds from normal bet receipt then dimension64-bet receipt
        EXPECTED: dimension65: "{popular upsell module/trending upsell module}",
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
        bet_receipt_id = self.site.bet_receipt.bet_id
        market_name = self.site.bet_receipt.market_type[:-2]
        odds = int(self.price_num) / int(self.price_den)
        float_num = float(odds) + 1
        odds = round(float_num, 2)
        self.verify_tracking(market_name=market_name,
                             category_id=self.trending_bet_category_id,
                             selection_id=self.tending_bet_selection_id,
                             bet_id=bet_receipt_id,
                             type_id=self.trending_bet_type_id,
                             belongs_inplay=0,
                             event_name = self.trending_bet_event_name,
                             odds=odds)

    def test_009_verify_the_newly_added_parameters_dimension64_and_dimension65(self):
        """
        DESCRIPTION: Verify the newly added parameters dimension64 and dimension65
        EXPECTED: 
        """
        # covered in above steps
