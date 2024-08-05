import pytest
from fractions import Fraction
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.liveserv_updates
@pytest.mark.ob_smoke
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C29079_Betslip_Reflection_on_Race_Price_Changed_on_Multiples(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C29079
    NAME: Betslip reflection on <Race> Price Changed on Multiples
    """
    keep_browser_open = True
    new_price_first_horse = '2/3'
    new_price_second_horse = '1/17'
    new_price2_first_horse = '5/3'
    new_price2_second_horse = '1/16'
    selection_ids_2 = None

    def test_000_create_event(self):
        """
        DESCRIPTION: Create test event
        """
        prices = {0: '1/2', 1: '1/3'}
        event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=prices, is_live=True)
        self.__class__.selection_ids = event_params1.selection_ids

        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=prices, is_live=True)
        self.__class__.selection_ids_2 = event_params2.selection_ids

    def test_001_get_event_prices_and_add_selection_to_betslip(self):
        """
        DESCRIPTION: Add selections to betslip
        """
        self.__class__.first_horse_name, self.__class__.first_horse_selection_id = list(self.selection_ids.items())[0]
        self.__class__.second_horse_name, self.__class__.second_horse_selection_id = list(self.selection_ids_2.items())[0]
        self.open_betslip_with_selections(selection_ids=[self.first_horse_selection_id, self.second_horse_selection_id])

    def test_002_trigger_price_change(self):
        """
        DESCRIPTION: Trigger the following situation for this event: change priceNum and priceDen and at the same time have Betslip page opened to watch for updates
        EXPECTED: Price Odds is changed
        """
        self.ob_config.change_price(selection_id=self.first_horse_selection_id, price=self.new_price_first_horse)
        self.ob_config.change_price(selection_id=self.second_horse_selection_id, price=self.new_price_second_horse)

    def test_003_verify_error_message_odds_indicator(self, first_new_price=new_price_first_horse,
                                                     second_new_price=new_price_second_horse, double_price='0.76/1'):
        """
        DESCRIPTION: Verify Error message, Odds indicator
        EXPECTED: the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        """
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.first_horse_selection_id)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.first_horse_name}" with id "{self.first_horse_selection_id}" is not received')

        price_update2 = self.wait_for_price_update_from_live_serv(selection_id=self.second_horse_selection_id)
        self.assertTrue(price_update2,
                        msg=f'Price update for selection "{self.second_horse_name}" with id "{self.second_horse_selection_id}" is not received')

        expected_error_message = vec.betslip.PRICE_CHANGE_BANNER_MSG
        result = self.get_betslip_content().wait_for_warning_message_text(text=expected_error_message, timeout=2)
        self.assertTrue(result, msg=f'Expected error message: "{expected_error_message}" has not appeared')

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples
        singles_stake1 = singles_section[self.first_horse_name] if self.first_horse_name in singles_section else None
        singles_stake2 = singles_section[self.second_horse_name] if self.second_horse_name in singles_section else None
        self.__class__.multiple_stake = multiples_section['Double'] if 'Double' in multiples_section else None
        self.assertTrue(singles_stake1, msg=f'No stake with name "{self.first_horse_name}" found')
        self.assertTrue(singles_stake2, msg=f'No stake with name "{self.second_horse_name}" found')
        self.assertTrue(self.multiple_stake, msg='No stake with name "Double" found')
        betslip_prices_current = self.get_price_odds_on_betslip()
        self.assertEqual(Fraction(betslip_prices_current[self.first_horse_name]), Fraction(first_new_price),
                         msg=f'Actual price of selection: "{betslip_prices_current[self.first_horse_name]}"" '
                             f'is not as expected: "{first_new_price}"')
        self.assertEqual(betslip_prices_current[self.second_horse_name], second_new_price,
                         msg=f'Actual price of selection: "{betslip_prices_current[self.second_horse_name]}"" '
                             f'is not as expected: "{second_new_price}"')
        self.assertEqual(betslip_prices_current['Double'], double_price,
                         msg=f'Actual price of Double: "{betslip_prices_current["Double"]}"'
                         f'is not as expected: "{double_price}"')

    def test_004_verify_login_and_bet_button(self):
        """
        DESCRIPTION: Enter stake and verify Bet Now button
        EXPECTED: Bet Now button should read as 'LOGIN & PLACE BET' and should be disabled
        """
        betnow_button = self.get_betslip_content().bet_now_button
        self.assertEqual(betnow_button.name,
                         vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION,
                         msg=f'Found "{betnow_button.name}" button name, expected "{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}"')

        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                         msg='Bet Now button is not disabled')

    def test_005_login(self):
        """
        DESCRIPTION: Login with user account with positive balance
        EXPECTED: User is logged in
        """
        self.site.close_betslip()
        self.site.login()

    def test_006_repeat_steps_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps for Logged In User
        EXPECTED: the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: The Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT & PLACE BET'
        EXPECTED: Coral: 'ACCEPT AND PLACE BET'
        """
        self.__class__.expected_betslip_counter_value = 0
        self.test_001_get_event_prices_and_add_selection_to_betslip()
        self.ob_config.change_price(selection_id=self.first_horse_selection_id, price=self.new_price2_first_horse)
        self.ob_config.change_price(selection_id=self.second_horse_selection_id, price=self.new_price2_second_horse)
        self.test_003_verify_error_message_odds_indicator(first_new_price=self.new_price2_first_horse,
                                                          second_new_price=self.new_price2_second_horse, double_price='1.83/1')
        betnow_button = self.get_betslip_content().bet_now_button
        self.assertEqual(betnow_button.name, vec.betslip.ACCEPT_BET,
                         msg=f'Found "{betnow_button.name}" button name, expected "{vec.betslip.ACCEPT_BET}"')
