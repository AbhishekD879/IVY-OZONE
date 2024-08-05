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
@pytest.mark.trending_bets
@pytest.mark.adhoc_suite
@pytest.mark.navigation
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65972773_Verify_GA_Tracking_When_user_adds_the_bet_from_the_carousel_in_the_betreceipt(BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C65972773
    NAME: Verify GA Tracking When user adds the bet from the carousel in the betreceipt
    DESCRIPTION: This test case is to verify GA Tracking When user adds the bet from the carousel in the betreceipt
    PRECONDITIONS: Should have Football events
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    bet_amount = 0.1
    headers = {'Content-Type': 'application/json'}

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
        trending_bet = list(self.site.betslip.trending_bets_section.items_as_ordered_dict.values())[1]
        trending_bet.scroll_to()
        self.__class__.trending_bet_name = trending_bet.name
        self.__class__.trending_bet_event_name = re.sub(r'^\d{2}:\d{2}\s', '', trending_bet.event_name)
        self.__class__.trending_bet_market_name = trending_bet.market_name
        trending_bet.odd.click()
        # trending bets verification in betslip
        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in singles_section.items():
            self._logger.debug(f'*** Verifying stake "{stake.outcome_name}"')
            if self.trending_bet_name == stake_name:
                betslip_trending_name = stake.outcome_name
                self.assertEqual(betslip_trending_name, self.trending_bet_name,
                                 msg=f'betslip trending name {betslip_trending_name} is not equal to trending bet name {self.trending_bet_name}')
                betslip_trending_event_name = stake.event_name
                self.assertEqual(betslip_trending_event_name, self.trending_bet_event_name,
                                 msg=f'betslip trending event name {betslip_trending_event_name} is not equal to trending bet  event name {self.trending_bet_event_name}')
                betslip_trending_market_name = stake.market_name
                self.assertEqual(betslip_trending_market_name, self.trending_bet_market_name,
                                 msg=f'betslip trending market name {betslip_trending_market_name} is not equal to trending bet market name {self.trending_bet_market_name}')
                stake.amount_form.input.click()
                betslip_content = self.get_betslip_content()
                self.assertTrue(
                    betslip_content.keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                    msg='Betslip keyboard is not shown')
                betnow_btn = betslip_content.bet_now_button
                self.assertFalse(betnow_btn.is_enabled(expected_result= False,timeout=1), msg='Bet Now button is not disabled or enabled')
                if self.device_type == 'mobile' and tests.use_browser_stack:
                    keyboard = self.get_betslip_content().keyboard
                    keyboard.enter_amount_using_keyboard(value='0')
                    keyboard.enter_amount_using_keyboard(value='.')
                    keyboard.enter_amount_using_keyboard(value='0')
                    keyboard.enter_amount_using_keyboard(value='1')
                else:
                    self.enter_stake_amount(stake=(stake_name, stake))
                betnow_btn = betslip_content.bet_now_button
                self.assertTrue(betnow_btn.is_enabled(timeout=2), msg='Bet Now button is not enabled')
                betnow_btn.click()

    def test_006_verify_the_betreceipt(self):
        """
        DESCRIPTION: Verify the Betreceipt
        EXPECTED: Able to see the trending bets carousel in Betreceipt
        """
        self.check_bet_receipt_is_displayed(timeout=3)
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
                        self.assertEqual(betreceipt_event_name, self.trending_bet_event_name,
                                         msg=f'bet-receipt trending name {betreceipt_event_name} is not equal to trending bet name {self.trending_bet_event_name}')

    def test_008_add_any_bet_from_the_carousel_in_the_betreceipt(self):
        """
        DESCRIPTION: Add any bet from the carousel in the betreceipt
        EXPECTED: Able to add the bet
        """
        betreceipt_trending_bet = list(self.site.bet_receipt.trending_bets_section.items_as_ordered_dict.values())[0]
        betreceipt_trending_bet.scroll_to()
        self.__class__.betreceipt_trending_bet = betreceipt_trending_bet.name
        self.__class__.betreceipt_trending_bet_event_name = re.sub(r'^\d{2}:\d{2}\s', '', betreceipt_trending_bet.event_name)
        self.__class__.betreceipt_trending_bet_market_name = betreceipt_trending_bet.market_name
        betreceipt_trending_bet.odd.click()
        wait_for_haul(10)
        # Here we are taking category id,selection id etc...from build bet call
        outcome_details = self.get_outcome_details()
        for outcome in outcome_details:
            if self.betreceipt_trending_bet == outcome['name']:
                self.__class__.trending_bet_event_id = outcome['eventId']
                self.__class__.trending_bet_type_id = outcome['typeId']
                self.__class__.trending_bet_category_id = outcome['categoryId']
                self.__class__.tending_bet_selection_id = outcome['id']
                self.__class__.trending_bet_event_name = outcome['eventDesc']
                break
        singles_section = self.get_betslip_sections().Singles
        for selection_name, selection in singles_section.items():
            self._logger.debug(f'*** Verifying stake "{selection.outcome_name}"')
            # verifying trending bet in betslip where we click on trending bets from bet receipt
            if self.betreceipt_trending_bet == selection_name:
                selection.outcome.click()
                self.__class__.dialog = self.site.wait_for_dialog(
                    dialog_name=vec.dialogs.DIALOG_MANAGER_SELECTION_INFORMATION, timeout=10, verify_name=False)
                self.assertTrue(self.dialog,
                                msg=f'"{vec.dialogs.DIALOG_MANAGER_SELECTION_INFORMATION}" dialog is not displayed')
                if selection_name.upper() == self.dialog.name.upper():
                    self.dialog.selection_content.click()
                    if self.site.wait_for_stream_and_bet_overlay(timeout=10):
                        self.site.stream_and_bet_overlay.close_button.click()

                    self.site.open_betslip()

    def test_009_verify_ga_tracking_in_console(self):
        """
        DESCRIPTION: Verify GA tracking in console
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: [{
        EXPECTED: eventCategory: "betslip",
        EXPECTED: eventAction: "add to betslip",
        EXPECTED: eventLabel: "success",
        EXPECTED: ecommerce: {
        EXPECTED: add: {
        EXPECTED: products: [
        EXPECTED: {
        EXPECTED: dimension86: 0,
        EXPECTED: dimension87: 0,
        EXPECTED: dimension88: null,
        EXPECTED: quantity: 1,
        EXPECTED: name: "{event name}",//ex:Kenta Miyoshi v Cash Hanzlik
        EXPECTED: category: "{category id}",//ex:34
        EXPECTED: variant: "{variant}",//ex:50119
        EXPECTED: brand: "{brand}",//ex:Outright
        EXPECTED: dimension60: "{Bet - event ID}",
        EXPECTED: dimension61: "{Bet - selection ID}",
        EXPECTED: dimension62: 0,
        EXPECTED: dimension63: 0,
        EXPECTED: dimension64: "{bet receipt/ quick bet receipt}",//ex:if user adds bet from quick bet receipt then dimension64=quick bet receipt, if user adds from normal bet receipt then dimension64-bet receipt
        EXPECTED: dimension65: "{popular upsell module/trending upsell module}",
        EXPECTED: dimension177: "No show",
        EXPECTED: dimension180: "normal"
        EXPECTED: }]
        EXPECTED: }}
        EXPECTED: }]
        EXPECTED: });
        """
        self.verify_ga_tracking_record(brand=self.betreceipt_trending_bet_market_name,
                                       category=self.trending_bet_category_id,
                                       event_id=self.trending_bet_event_id,
                                       selection_id=self.tending_bet_selection_id,
                                       inplay_status=0, customer_built=0,
                                       location='bet receipt',
                                       module='trending upsell module',
                                       name=self.trending_bet_event_name,
                                       variant=self.trending_bet_type_id,
                                       event='trackEvent',
                                       event_action='add to betslip',
                                       event_category='betslip',
                                       event_label='success',
                                       stream_active=False,
                                       stream_ID=None,
                                       dimension86=0,
                                       dimension87=0,
                                       dimension88=None,
                                       dimension177="No show",
                                       dimension64="bet receipt",
                                       dimension65="trending upsell module",
                                       dimension180="normal",
                                       dimension166="normal",
                                       quantity=1)

    def test_010_verify_the_newly_added_parameters_dimension64_and_dimension65(self):
        """
        DESCRIPTION: Verify the newly added parameters dimension64 and dimension65
        EXPECTED: 
        """
        # covered in above step

