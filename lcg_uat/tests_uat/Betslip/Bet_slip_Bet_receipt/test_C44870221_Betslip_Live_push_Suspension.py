import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - This script is executed only for QA2 as we cannot suspend any event from our end in prod or beta
@pytest.mark.medium
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C44870221_Betslip_Live_push_Suspension(BaseBetSlipTest):
    """
    TR_ID: C44870221
    NAME: Betslip Live push /Suspension
    """
    keep_browser_open = True
    prices = '1/2'
    increased_price = '1/4'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Sports should be available in inplay
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True, lp_prices=self.prices,
                                                                          default_market_name='|Draw No Bet|')
        event2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True, lp_prices=self.prices,
                                                                           default_market_name='|Draw No Bet|')
        self.__class__.selection_id_1 = event.selection_ids[event.team1]
        self.__class__.selection_id_2 = event2.selection_ids[event2.team2]
        event_params = self.ob_config.add_tennis_event_to_autotest_trophy(is_live=True, lp_prices=self.prices)
        self.__class__.selection_id_3 = list(event_params.selection_ids.values())[0]

    def test_001_launch_the_app_enter_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the app enter with valid credentials
        EXPECTED: Application launched successfully and User should be logged in successfully
        """
        self.site.login()

    def test_002_go_to_in_play_steaming_from_home_page(self):
        """
        DESCRIPTION: Go to 'In-play &steaming' from home page
        EXPECTED: User should be on in-play page
        """
        if self.device_type == 'mobile':
            modules = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(modules, msg='No tabs found in the homepage')
            for item_name, item in modules.items():
                if item_name == vec.bma.IN_PLAY.upper():
                    item.click()
                    self.assertEqual(item_name, vec.bma.IN_PLAY.upper(), msg=f'Actual Title "{item_name}" is not same as '
                                                                             f'Expected title "{vec.bma.IN_PLAY.upper()}"')
        else:
            inplay_livestream_section = self.site.home.desktop_modules.inplay_live_stream_module
            self.assertTrue(inplay_livestream_section.is_displayed(),
                            msg=f'"{vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME}" section is not displayed')
            self.assertEqual(inplay_livestream_section.name, vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME,
                             msg=f'Actual title "{inplay_livestream_section.name}" '
                                 f'is not as same as Expected title "{vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME}"')

    def test_003_add_some_selections_from_any_in_play_events_from_any_market_for_different_sports_and_verify_the_bet_slip_with_live_push_when_price_changes(self):
        """
        DESCRIPTION: Add some selections from any in-play events from any market for different sports And Verify the bet slip with Live Push when price changes
        EXPECTED: User must be presented with all the selection from different markets to the Bet slip and User must presented with the top message in the Bet slip
        EXPECTED: Price change notification
        EXPECTED: "Some of your prices have changed"
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_3))
        singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, self.stake))
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(timeout=1.5), msg='Place Bet button is not enabled')
        self.assertEqual(bet_now_button.name, vec.quickbet.BUTTONS.place_bet.upper(),
                         msg=f'Found "{bet_now_button.name}" button name,'
                             f' expected "{vec.quickbet.BUTTONS.place_bet.upper()}"')
        self.ob_config.change_price(selection_id=self.selection_id_1, price=self.increased_price)
        if self.brand == 'bma':
            price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection_id_1,
                                                                     price=self.increased_price)
            self.assertTrue(price_update, msg=f'Price update for selection "{self.team1}" '
                                              f'with id "{self.selection_id_1}" is not received')
            general_error_msg = self.get_betslip_content().wait_for_warning_message()
            self.assertEqual(general_error_msg, vec.betslip.PRICE_CHANGE_BANNER_MSG,
                             msg=f'Actual error message: "{general_error_msg}" '
                             f'is not equal to expected: "{vec.betslip.PRICE_CHANGE_BANNER_MSG}"')
        else:
            # TODO BMA-55571
            # The above JIRA mentions issue with the price change and the messages "Some of the prices have changed"
            # and price updation cannot be verified in QA2 ladbrokes
            pass

    def test_004_verify_the_bet_slip_with_live_push_when_price_changes_for_the_added_selections(self):
        """
        DESCRIPTION: Verify the bet slip with Live Push when price changes for the added selections
        EXPECTED: User must be presented with the message just above the selection in the Bet slip like
        EXPECTED: 'Price changed from x/x to x/x' for all the changed prices
        """
        # Skipped verification of this error message in ladbrokes due to the Issue mentioned above
        if self.brand == 'bma':
            error = self.stake.error_message
            expected_error = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(
                old=self.prices, new=self.increased_price)
            self.assertEqual(error, expected_error,
                             msg=f'Received error "{error}" is not the same as expected "{expected_error}"')

    def test_005_verify_the_place_bet_button_text_update(self):
        """
        DESCRIPTION: Verify the 'Place Bet' button text update
        EXPECTED: User must be presented with the replaced of 'Place Bet' button with 'Accept & Continue' button
        """
        bet_now_button = self.get_betslip_content().bet_now_button
        if self.brand == 'bma':
            self.assertEqual(bet_now_button.name, vec.betslip.ACCEPT_BET,
                             msg=f'Found "{bet_now_button.name}" button name,expected "{vec.betslip.ACCEPT_BET}"')
        self.assertTrue(wait_for_result(lambda: bet_now_button.is_enabled(expected_result=True), timeout=15),
                        msg=f'"{vec.quickbet.BUTTONS.place_bet}" button is disabled')
        bet_now_button.click()
        self.site.wait_content_state_changed()
        if self.brand == 'ladbrokes':
            # Added this additional verification as we seeing the change of button after clicking on "PLACE BET"button
            bet_now_button = self.get_betslip_content().bet_now_button
            self.assertEqual(bet_now_button.name, vec.betslip.ACCEPT_BET,
                             msg=f'Found "{bet_now_button.name}" button name, '
                                 f'expected "{vec.betslip.ACCEPT_BET}"')
            bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_006_verify_when_user_clicks_on_any_sports_or_races_virtual(self):
        """
        DESCRIPTION: Verify when user clicks on any sports or races (Virtual)
        EXPECTED: User must be on particular page page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')

    def test_007_add_selections_to_bet_slip(self):
        """
        DESCRIPTION: Add selections to bet slip
        EXPECTED: Selection should have been added in to bet slip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id_2)

    def test_008_verify_when_the_event_starts__suspension_displayed_in_bet_slip(self):
        """
        DESCRIPTION: Verify when the event starts , suspension displayed in bet slip
        EXPECTED: Suspension must be displayed in bet slip and user must not be able to place bet.
        """
        self.ob_config.change_selection_state(self.selection_id_2, displayed=True, active=False)
        if self.brand == 'ladbrokes':
            # Added this code as the suspension is not reflecting in ladbrokes until the page is being refreshed
            # The automatic updation of selections are not happening due to above mentioned JIRA issue
            self.device.refresh_page()
            self.site.open_betslip()
            result = wait_for_result(lambda: self.get_betslip_content().error == vec.betslip.SELECTION_DISABLED,
                                     name='Betslip error to change', timeout=5)
            self.assertTrue(result, msg=f'Bet Now section warning "{self.get_betslip_content().error}" '
                                        f'is not the same as expected: "{vec.betslip.SELECTION_DISABLED}"')
        else:
            result = wait_for_result(lambda: self.get_betslip_content().error == vec.betslip.SINGLE_DISABLED,
                                     name='Betslip error to change', timeout=5)
            self.assertTrue(result, msg=f'Bet Now section warning "{self.get_betslip_content().error}" '
                                        f'is not the same as expected: "{vec.betslip.SINGLE_DISABLED}"')
        betnow_button = self.get_betslip_content().bet_now_button
        self.assertFalse(betnow_button.is_enabled(), msg='Bet Now button is enabled and able to place bet')
