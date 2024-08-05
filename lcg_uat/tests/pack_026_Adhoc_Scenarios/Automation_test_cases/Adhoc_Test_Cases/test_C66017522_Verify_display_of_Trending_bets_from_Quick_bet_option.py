import json
import re
import pytest
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from random import choice
import tests
from tests.base_test import vtest
from tests.Common import Common
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
import voltron.environments.constants as vec
from voltron.utils.helpers import do_request
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.trending_bets
@pytest.mark.adhoc_suite
@pytest.mark.adhoc24thJan24
@pytest.mark.navigation
@vtest
class Test_C66017522_Verify_display_of_Trending_bets_from_Quick_bet_option(BaseBetSlipTest):
    """
    TR_ID: C66017522
    NAME: Verify display of  Trending bets from Quick bet option
    DESCRIPTION: This test case is to verifies the Trending bets from Quick bet option.
    PRECONDITIONS: 1. Trending Bets Carousel is configured in the CMS
    PRECONDITIONS: 2. Navigation to CMS -&gt; Most Popular/Trending Bets -&gt; Bet slip -&gt; Enable -&gt; Bet receipt -&gt; Enable for Bet receipt -&gt; Enable for Quick Bet receipt"
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    bet_amount = 0.1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        DESCRIPTION: Find / create event for test
        EXPECTED: User is logged in
        EXPECTED: Event is found / created
        """
        ###### verify Trending bet carousel in bet slip is enable or not in CMS ##################
        trending_carousel_betslip = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('active')
        if not trending_carousel_betslip:
            self.cms_config.update_most_popular_or_trending_bets_bet_slip_config(active=True)
        ######### verify trending bet carousal in bet receipt is enable or not in CMS #############
        trending_carousal_bet_receipt = self.cms_config.get_most_popular_or_trending_bets_bet_receipt_config().get('active')
        if not trending_carousal_bet_receipt:
            self.cms_config.update_most_popular_or_trending_bets_bet_receipt_config(active=True)
        ######## Verify Trending bet carousel in quick bet receipt is enable or not in CMS ###############
        trending_carousal_quick_bet_receipt = self.cms_config.get_most_popular_or_trending_bets_bet_receipt_config().get('isQuickBetReceiptEnabled')
        if not trending_carousal_quick_bet_receipt:
            self.cms_config.update_most_popular_or_trending_bets_bet_receipt_config(isQuickBetReceiptEnabled=True)

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

    def test_002_navigate_to_football_sport(self):
        """
        DESCRIPTION: Navigate to Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

    def test_003_add_any_football_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add any football selection to quick bet
        EXPECTED: Selection is added to quick bet page
        """
        self.__class__.event = self.get_event_from_league(event_id=self.event_id,
                                                          section_name=self.league)
        output_prices = self.event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for event "{self.event_name}"')
        selection = choice(list(output_prices.keys()))
        bet_button = output_prices.get(selection)
        self.assertTrue(bet_button, msg=f'Bet button for "{selection}" was not found')
        bet_button.click()
        quick_bet = self.site.quick_bet_panel.selection
        self.assertFalse(quick_bet.keyboard.is_displayed(name='Betslip keyboard shown',
                                                              timeout=3, expected_result=False),
                         msg='Keyboard is not collapsed by default')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='PLACE BET button is not disabled')
        quick_bet_input = quick_bet.content.amount_form.input
        quick_bet_input.click()
        if not quick_bet.keyboard.is_displayed():
            quick_bet_input.click()
        self.assertTrue(quick_bet.content.amount_form.is_active(), msg='"Stake" box is not highlighted')
        self.assertTrue(quick_bet.keyboard.is_displayed(name='Betslip keyboard shown', timeout=10),
                        msg='Numeric keyboard is not opened')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP buttons is not enabled')


    def test_004_enter_stake_and_place_bet(self):
        """
        DESCRIPTION: Enter stake and place bet
        EXPECTED: Bet is placed successfully and navigates to Bet receipt page
        """
        self.enter_value_using_keyboard(value=self.bet_amount, on_betslip=False)
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')

    def test_005_verify_the_display_of_trending_bets_carousel_in_bet_receipt_page(self):
        """
        DESCRIPTION: Verify the display of Trending bets carousel in Bet receipt page
        EXPECTED: Application should display the trending bets carousel under the 'Bet placed successfully' message section
        """
        trending_bet_sections = self.site.quick_bet_panel.bet_receipt.trending_bets_section
        self.assertTrue(trending_bet_sections, msg='Trending bets sections are not display in Quick bet receipt')
        self.assertTrue(self.site.quick_bet_panel.bet_receipt.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available')
        ######## Chevron Arrow Verification in Quick Bet Receipt ##################
        self.assertTrue(trending_bet_sections.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
        trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.quick_bet_panel.bet_receipt.trending_bets_section.is_chevron_down,
                        msg='chevron did not turned down')
        trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.quick_bet_panel.bet_receipt.trending_bets_section.is_chevron_up,
                        msg='chevron did not turned up')
        ###### adding one trending bet selection into betslip #########
        trending_bet_receipt = list(trending_bet_sections.items_as_ordered_dict.values())[0]
        trending_bet_receipt.scroll_to()
        trending_bet_name = trending_bet_receipt.name
        trending_bet_event_name = re.sub(r'^\d{2}:\d{2}\s', '', trending_bet_receipt.event_name)
        trending_bet_market_name = trending_bet_receipt.market_name
        trending_bet_receipt.odd.click()
        ############# Chevron verification in bet slip ########################
        self.assertTrue(self.site.betslip.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available')
        betslip_trending_bet_sections = self.site.betslip.trending_bets_section
        self.assertTrue(betslip_trending_bet_sections, msg='Trending bets sections are not display in Bet Slip')
        self.assertTrue(betslip_trending_bet_sections.chevron_arrow.is_displayed(),
                        msg='Chevron arrow is not displayed')
        betslip_trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.betslip.trending_bets_section.is_chevron_down, msg='chevron did not turned down')
        betslip_trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.betslip.trending_bets_section.is_chevron_up, msg='chevron did not turned up')
        ######################### Betslip verification ################
        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in singles_section.items():
            self._logger.debug(f'*** Verifying stake "{stake.outcome_name}"')
            if trending_bet_name == stake_name:
                betslip_trending_name = stake.outcome_name
                self.assertEqual(betslip_trending_name, trending_bet_name,
                                 msg=f'betslip trending name {betslip_trending_name} is not equal to trending bet name {trending_bet_name}')
                betslip_trending_event_name = stake.event_name
                if betslip_trending_event_name == trending_bet_event_name:
                    self.assertEqual(betslip_trending_event_name, trending_bet_event_name,
                                    msg=f'betslip trending event name {betslip_trending_event_name} is not equal to trending bet  event name {trending_bet_event_name}')
                else:
                    self.assertEqual(betslip_trending_event_name, trending_bet_name,
                                     msg=f'betslip trending event name {betslip_trending_event_name} is not equal to trending bet  event name {trending_bet_name}')
                betslip_trending_market_name = stake.market_name
                self.assertEqual(betslip_trending_market_name, trending_bet_market_name,
                                 msg=f'betslip trending market name {betslip_trending_market_name} is not equal to trending bet market name {trending_bet_market_name}')

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

        ############################# chevron verification in Bet receipt #######################
        self.check_bet_receipt_is_displayed()
        betreceipt_trending_bet_sections = self.site.bet_receipt.trending_bets_section
        self.assertTrue(betreceipt_trending_bet_sections, msg='Trending bets sections are not display in Bet Receipt')
        self.assertTrue(betreceipt_trending_bet_sections.chevron_arrow.is_displayed(),
                        msg='Chevron arrow is not displayed')
        betreceipt_trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.bet_receipt.trending_bets_section.is_chevron_down, msg='chevron did not turned down')
        betreceipt_trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.bet_receipt.trending_bets_section.is_chevron_up, msg='chevron did not turned up')
