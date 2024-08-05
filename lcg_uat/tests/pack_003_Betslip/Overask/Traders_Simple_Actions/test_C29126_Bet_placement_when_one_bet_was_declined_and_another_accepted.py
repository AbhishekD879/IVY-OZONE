import pytest
import voltron.environments.constants as vec
from collections import defaultdict
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # overask cant be triggered for prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C29126_Bet_placement_when_one_bet_was_declined_and_another_accepted(BaseBetSlipTest):
    """
    TR_ID: C29126
    NAME: Bet placement when one bet was declined and another accepted
    DESCRIPTION: This test case verifies Bet Slip functionality and UI when one bet was accepted and another rejected
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
    keep_browser_open = True
    selection_ids = []
    event_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create events
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        self.__class__.max_mult_bet = self.max_bet + 0.1
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(
                default_market_name='|Draw No Bet|',
                max_bet=self.max_bet,
                max_mult_bet=self.max_mult_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        self.site.login()

    def test_002_add_two_selections_and_go_to_betslip_singles_section(self):
        """
        DESCRIPTION: Add two selections and go to Betslip, 'Singles' section
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_ids[0], self.selection_ids[1]])

    def test_003_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_two_selections_and_click__tap__place_bet_button(self, bet_type='Single'):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for two selections and click / tap  'Place bet' button
        EXPECTED: The bet is sent to Openbet system for review
        """
        if bet_type == 'Single':
            section = self.get_betslip_sections().Singles
            self.assertTrue(section.items(), msg='*** No stakes found')
            stake_name1, stake1 = list(section.items())[0]
            stake_name2, stake2 = list(section.items())[1]
        else:
            single, double = self.get_betslip_sections(multiples=True)
            stake_name1, stake1 = list(single.items())[0]
            stake_name2, stake2 = list(double.items())[0]

        if bet_type == 'Single':
            stake_bet_amounts1 = {stake_name1: self.max_bet + 0.01}
            stake_bet_amounts2 = {stake_name2: self.max_bet + 0.01}
        else:
            stake_bet_amounts1 = {stake_name1: self.max_mult_bet + 0.01}
            stake_bet_amounts2 = {stake_name2: self.max_mult_bet + 0.01}
        self.enter_stake_amount(stake=(stake_name1, stake1), stake_bet_amounts=stake_bet_amounts1)
        self.enter_stake_amount(stake=(stake_name2, stake2), stake_bet_amounts=stake_bet_amounts2)
        sleep(3)
        self.get_betslip_content().bet_now_button.click()

    def test_004_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask excedds message is not shown')
        overask_offer_message = self.get_betslip_content().overask.overask_offer.is_displayed()
        self.assertTrue(overask_offer_message, msg='Overask bottom message is not shown')

        overask_spinner = self.get_betslip_content().overask.overask_spinner.is_displayed()
        self.assertTrue(overask_spinner, msg='Overask spinner is not shown')

        has_overask_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(has_overask_message, msg='Overask message closed after click on background')

    def test_005____trigger_rejecting_the_first_bet_by_a_trader_in_openbet_system___trigger_accepting_the_second_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: *   Trigger rejecting the first bet by a trader in OpenBet system
        DESCRIPTION: *   Trigger accepting the second bet by a trader in OpenBet system
        EXPECTED: *   First bet is rejected in OpenBet, Second bet is accepted.
        EXPECTED: *   Confirmation and the reason of rejecting are sent and received in Oxygen app
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.event_ids)
        acct_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        flag_single = True
        flag_dbl = True
        data = defaultdict(dict)

        for bet_id, bet_type in bets_details.items():
            if bet_type == 'SGL' and flag_single:
                data['bet1']['id'] = bet_id
                data['bet1']['action'] = 'A'
                data['bet1']['bettype'] = bet_type
                flag_single = False
            elif bet_type == 'SGL' and not flag_single:
                data['bet3']['id'] = bet_id
                data['bet3']['action'] = 'D'
                data['bet3']['bettype'] = bet_type

            elif bet_type == 'DBL' and flag_dbl:
                data['bet2']['id'] = bet_id
                data['bet2']['action'] = 'D'
                data['bet2']['bettype'] = bet_type

        self.bet_intercept.multiple_actions_bets(acct_id=acct_id, betslip_id=betslip_id, bets_details=data)

    def test_006_verify_betslip(self, bet_type='Single'):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * Accepted Bet has a message saying '(X) Bet Placed Successfully' within a bet receipt
        EXPECTED: * 'This bet has not been accepted by traders!' message is displayed for declined bet
        EXPECTED: * 'Go Betting' button is present and enabled ('Reuse Selections' button is absent)
        EXPECTED: ![](index.php?/attachments/get/33995) ![](index.php?/attachments/get/33994)
        """
        self.check_bet_receipt_is_displayed()
        self.assertEqual(self.site.bet_receipt.receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{self.site.bet_receipt.receipt_header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        self.assertTrue(self.site.bet_receipt.footer.done_button.is_displayed(),
                        msg='"Go betting" button isn\'t present')

        self.assertFalse(self.site.bet_receipt.footer.has_reuse_selections_button(expected_result=False),
                         msg='"Re-use selection" button isn\'t disabled')
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        if bet_type == 'Single':
            _, section = list(betreceipt_sections.items())[0]
            overask_warning_message = section.declined_bet.stake_content.stake_message
        else:
            _, section = list(betreceipt_sections.items())[1]
            overask_warning_message = section.multiple_declined_bet.stake_message

        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual overask warning message: "{overask_warning_message}" is not equal '
                             f'to expected: "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')

    def test_007_click__tap_continuego_betting_from_ox_99_button(self):
        """
        DESCRIPTION: Click / tap 'Continue'/'Go Betting' (From OX 99) button
        EXPECTED: * Betslip is closed
        EXPECTED: * User is redirected to the Home page (?)
        """
        self.site.bet_receipt.footer.done_button.click()
        self.site.wait_content_state('Home')

    def test_008_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        """
        self.test_002_add_two_selections_and_go_to_betslip_singles_section()

    def test_009_repeat_steps__3_7_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-7 for Multiple bet
        """
        self.test_003_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_two_selections_and_click__tap__place_bet_button(bet_type='Double')
        self.test_004_verify_betslip()
        self.test_005____trigger_rejecting_the_first_bet_by_a_trader_in_openbet_system___trigger_accepting_the_second_bet_by_a_trader_in_openbet_system()
        self.test_006_verify_betslip(bet_type='Double')
        self.test_007_click__tap_continuego_betting_from_ox_99_button()

    def test_010_add_a_few_selections_from_the_same_race_event_and_go_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and go Betslip, 'Forecasts/Tricasts' section
        """
        self.selection_ids.clear()
        self.event_ids.clear()
        for i in range(2):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=4, forecast=True,
                                                              max_bet=self.max_bet, max_mult_bet=self.max_mult_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)
        self.test_002_add_two_selections_and_go_to_betslip_singles_section()

    def test_011_repeat_steps__3_6_for_forecaststricastsbet(self):
        """
        DESCRIPTION: Repeat steps № 3-6 for Forecasts/Tricasts bet
        """
        self.test_003_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_two_selections_and_click__tap__place_bet_button()
        self.test_004_verify_betslip()
        self.test_005____trigger_rejecting_the_first_bet_by_a_trader_in_openbet_system___trigger_accepting_the_second_bet_by_a_trader_in_openbet_system()
        self.test_006_verify_betslip()
        self.test_007_click__tap_continuego_betting_from_ox_99_button()
