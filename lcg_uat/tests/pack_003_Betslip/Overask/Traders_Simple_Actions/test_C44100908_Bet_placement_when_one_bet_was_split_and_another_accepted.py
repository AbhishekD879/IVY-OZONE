import pytest
import tests
import voltron.environments.constants as vec
from collections import defaultdict
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create events on PROD
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C44100908_Bet_placement_when_one_bet_was_split_and_another_accepted(BaseBetSlipTest):
    """
    TR_ID: C44100908
    NAME: Bet placement when one bet was split and another accepted
    DESCRIPTION: This test case verifies bet placement when one bet was split and another accepted
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in to the app
    PRECONDITIONS: 3. Overask functionality is enabled for the user
    PRECONDITIONS: 4. Go to CMS >'System-configuration' section > Config' tab > find 'Overask' config
    PRECONDITIONS: 5. Initial Data' checkbox is present within 'Overask' config and unchecked by default
    PRECONDITIONS: 6. The Initial response of the config contains 'The initialDataConfig: false'
    PRECONDITIONS: 7. The Initial Data response on homepage is absent
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Overask:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    PRECONDITIONS: ![](index.php?/attachments/get/109045765)
    """
    prices = [{0: '1/12', 1: '1/10', 2: '1/9'},
              {0: '1/13', 1: '1/11', 2: '1/11'}]
    new_price = '1.5'
    selection_ids = []
    event_ids = []
    event_names = []

    def test_000_pre_conditions(self):
        """
        Create an event
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(
                default_market_name='|Draw No Bet|', lp=self.prices[i],
                max_bet=self.max_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)
            self.event_names.append(f'{event_params.team1} v {event_params.team2}')
        self.site.login(username=tests.settings.betplacement_user)

    def test_001_add_two_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add two selections to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.__class__.sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(self.sections, msg=f'"{self.sections}" is not added to the betslip')

    def test_002__enter_stake_value_which_is_higher_then_maximum_limit_for_each_added_selection_tap_place_bet_button(self):
        """
        DESCRIPTION: * Enter stake value which is higher then maximum limit for each added selection
        DESCRIPTION: * Tap 'Place bet' button
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown to the User
        """
        singles_section = self.sections.Singles
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=2).items():
            self.enter_stake_amount(stake=stake)

        self.__class__.est_returns_before = self.get_betslip_content().total_estimate_returns
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(), msg=f'"{bet_now_button.name}" button is disabled')
        bet_now_button.click()
        overask = self.get_betslip_content().wait_for_overask_panel()
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_003__trigger_accepting_the_bet_by_trader_for_the_first_bet_trigger_split_action_by_a_trader_in_openbet_system_for_the_second_bet(self):
        """
        DESCRIPTION: * Trigger accepting the bet by Trader for the first bet
        DESCRIPTION: * Trigger split action by a trader in OpenBet system for the second bet
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative'
        EXPECTED: * message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * 'i' icon is displayed on the left side of the message
        EXPECTED: * The accepted bet is shown to the user on the Betslip and NOT highlighted in yellow color
        EXPECTED: * The split bets are shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.event_ids)
        acct_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        flag = False
        data = defaultdict(dict)

        for bet_id, bet_type in bets_details.items():
            if not flag:
                data['bet1']['id'] = bet_id
                data['bet1']['action'] = 'A'
                data['bet1']['bettype'] = bet_type
                flag = True
            else:
                data['bet2']['bettype'] = bet_type
                data['bet2']['split'] = True
                data['bet2']['id'] = bet_id
                data['bet2']['action'] = 'O'
                data['bet2']['event_id'] = self.eventID
                data['bet2']['stake_part1'] = '0.6'
                data['bet2']['price_part1'] = '1/3'
                data['bet2']['stake_part2'] = '0.9'
                data['bet2']['price_part2'] = '1/3'
                data['bet2']['stake_part3'] = '0.9'
                data['bet2']['price_part3'] = '1/3'
        self.bet_intercept.multiple_actions_bets(acct_id=acct_id, betslip_id=betslip_id, bets_details=data)
        wait_for_result(lambda: self.get_betslip_content().overask_trader_section.trader_offer_info_icon.is_displayed(),
                        name='Waiting for the icon to be displayed',
                        timeout=20)
        self.assertTrue(self.get_betslip_content().overask_trader_section.trader_offer_info_icon,
                        msg='"i" icon is not displayed')
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for "{stake_name}" is highlighted in '
                             f'yellow "{stake.offered_stake.background_color_value}"')
        est_returns_after = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(est_returns_after, self.est_returns_before,
                            msg=f'Est returns before:"{self.est_returns_before}" and '
                                f'Est returns after:"{est_returns_after}" are equal')
        self.assertTrue(self.get_betslip_content().has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='"Place Bet" button is not enabled')

    def test_004_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: * The bets are placed as per normal process
        EXPECTED: * Bet receipts are displayed
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()

    def test_005_repeat_steps_1_3_and_press_cancel_button(self):
        """
        DESCRIPTION: Repeat steps 1-3 and press 'Cancel' button
        EXPECTED: * Offer is not accepted
        EXPECTED: * None of the bets are placed (including accepted bets)
        """
        self.__class__.expected_betslip_counter_value = 0
        self.test_001_add_two_selections_to_the_betslip()
        self.test_002__enter_stake_value_which_is_higher_then_maximum_limit_for_each_added_selection_tap_place_bet_button()
        self.test_003__trigger_accepting_the_bet_by_trader_for_the_first_bet_trigger_split_action_by_a_trader_in_openbet_system_for_the_second_bet()
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        if self.device_type != 'desktop':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=5),
                             msg='Betslip widget was not closed')
