import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl  # we cannot trigger price change on prod
# @pytest.mark.prod  # we cannot trigger price change on prod
@pytest.mark.betslip
@pytest.mark.in_play
@pytest.mark.acca
@pytest.mark.bet_placement
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-53302')
@vtest
class Test_C3233950_Verify_price_change_displaying_for_In_Play_events_in_front_end_at_once_appropriate_update_is_received_in_Websockets(BaseBetSlipTest, BaseUserAccountTest, BaseRacing):
    """
    TR_ID: C3233950
    NAME: Verify price change displaying for In-Play events in front-end at once appropriate update is received in Websockets
    DESCRIPTION: This test case verifies price change displaying for Multiples in front-end at once appropriate update is received in Websockets
    PRECONDITIONS: User is logged in to application and has positive balance
    PRECONDITIONS: In-Play sport events are available in application
    """
    keep_browser_open = True
    new_price = ['3/4', '4/5', '5/6']
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create In-Play test events from different sports
        DESCRIPTION: Log in to application with user which has positive balance
        """
        for item in range(0, 2):
            football_event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.selection_ids.append(list(football_event_params.selection_ids.values())[0])

            basketball_event_params = self.ob_config.add_basketball_event_to_autotest_league(is_live=True)
            self.selection_ids.append(list(basketball_event_params.selection_ids.values())[0])

            racing_event_params = self.ob_config.add_UK_racing_event(is_live=True, number_of_runners=2)
            self.selection_ids.append(list(racing_event_params.selection_ids.values())[0])

        self.site.login(async_close_dialogs=False)

    def test_001_add_at_least_3_selections_from_different_sport_events(self):
        """
        DESCRIPTION: Add at least 3 selections from different sport events
        EXPECTED: Selections are added to Betslip
        EXPECTED: 'Place your Acca' section is displayed with Treble bet available
        EXPECTED: Multiples section is displayed with all multiples created based on added selections
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[:3])

        sections = self.get_betslip_sections(multiples=True)
        multiples_section = sections.Multiples
        self.assertTrue(multiples_section.items(), msg='*** No stakes found')

        treble_stake = multiples_section.get(vec.betslip.TBL)
        self.assertTrue(treble_stake, msg=f'Acca stake "{vec.betslip.TBL}" cannot be found')

        if self.device_type == 'mobile' and self.brand == 'ladbrokes':
            multiples = [vec.betslip.TBL,
                         vec.betslip.DBL,
                         vec.betslip.TRX,
                         vec.betslip.PAT,
                         vec.betslip.ROB]
        else:
            multiples = [vec.betslip.TBL,
                         vec.betslip.DBL,
                         vec.betslip.TRX,
                         vec.betslip.PAT,
                         vec.betslip.SS3,
                         vec.betslip.ROB]

        multiples_section = multiples_section.items()
        for item in range(0, len(multiples_section)):
            stake_name, _ = list(multiples_section)[item]
            self.assertEqual(stake_name, multiples[item],
                             msg=f'Actual {item + 1} section name: "{stake_name}" '
                             f'is not as expected: "{multiples[item]}"')

    def test_002_in_ti_tool_trigger_price_update_for_both_selections_added_to_the_betslip(self, new_price='4/6'):
        """
        DESCRIPTION: In TI tool trigger price update for both selections added to the Betslip
        EXPECTED: Price updates are received in WS from Openbet TI tool
        EXPECTED: Price updates are displayed in application AT ONCE after they were received in WS:
        EXPECTED: Notification banner appears above Betslip footer section on the yellow background:
        EXPECTED: "Please beware that <number of bets with changed price> of your selections had a price change."
        EXPECTED: 'Bet Now' button is changed to 'Accept & Bet (<number of selections with price change>)'
        EXPECTED: 'Clear Betslip' and 'Accept & Bet (<number of selections with price change>)' buttons are enabled
        """
        singles_section = self.get_betslip_sections().Singles

        stake_name, stake = singles_section.items()[0]
        old_odds = stake.odds

        self.ob_config.change_price(selection_id=self.selection_ids[0], price=new_price)
        self.ob_config.change_price(selection_id=self.selection_ids[1], price=new_price)

        result = self.wait_for_price_update_from_live_serv(selection_id=self.selection_ids[0], price=new_price, preserve=False)
        self.assertTrue(result, msg='WS response has not been received')

        for stake in singles_section.values()[:2]:
            expected_message = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(old=old_odds, new=new_price)
            general_error_msg = stake.wait_for_error_message(timeout=5)
            result = wait_for_result(lambda: expected_message == general_error_msg,
                                     name='Price change message to appear',
                                     timeout=5)
            self.assertTrue(result, msg=f'Actual message: "{general_error_msg}" '
                                        f'does not match expected "{expected_message}"')

        actual_error_betslip_msg = self.get_betslip_content().wait_for_warning_message()
        self.assertEqual(actual_error_betslip_msg, vec.betslip.PRICE_CHANGE_BANNER_MSG,
                         msg=f'Actual BetSlip error message "{actual_error_betslip_msg}" != '
                         f'Expected "{vec.betslip.PRICE_CHANGE_BANNER_MSG}" ')

        expected_betnow_button_name = vec.betslip.ACCEPT_BET
        betnow_button = self.get_betslip_content().bet_now_button
        self.assertEqual(betnow_button.name, expected_betnow_button_name,
                         msg=f'Actual "{betnow_button.name}" button name, '
                         f'is not as expected "{expected_betnow_button_name}"')
        self.assertFalse(betnow_button.is_enabled(expected_result=False),
                         msg=f'"{expected_betnow_button_name}" button is disabled')

        remove_all_button = self.get_betslip_content().remove_all_button
        self.assertTrue(remove_all_button.is_enabled(), msg=f'"{remove_all_button.name}" button is disabled')

    def test_003_place_bet_at_once_after_price_updates_are_received_and_displayed_in_application(self):
        """
        DESCRIPTION: Place bet AT ONCE after price updates are received and displayed in application
        EXPECTED: Bet is placed successfully
        """
        self.place_single_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

        self.__class__.expected_betslip_counter_value = 0

    def test_004_repeat_steps_2_3_for_acca_4_acca_5_acca_6_multiples_available_in_place_your_acca_section(self):
        """
        DESCRIPTION: Repeat steps 2-3 for Accumulator (4), Accumulator (5), Accumulator (6) multiples available in 'Place your acca' section
        """
        acca_template = '{0} Fold Acca'
        for item in range(0, 3):
            acca_name = acca_template.format(item + 4)
            self._logger.debug(f'*** Repeating verifications for "{acca_name}"')
            self.open_betslip_with_selections(selection_ids=self.selection_ids[:item + 4])

            sections = self.get_betslip_sections(multiples=True)
            multiples_section = sections.Multiples

            treble_stake = multiples_section.get(acca_name)
            self.assertTrue(treble_stake, msg=f'Acca stake "{acca_name}" cannot be found')

            self.test_002_in_ti_tool_trigger_price_update_for_both_selections_added_to_the_betslip(new_price=self.new_price[item])
            self.test_003_place_bet_at_once_after_price_updates_are_received_and_displayed_in_application()
