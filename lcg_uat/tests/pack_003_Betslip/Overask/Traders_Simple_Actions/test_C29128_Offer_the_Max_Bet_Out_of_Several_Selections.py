import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Overask cannot be triggered in prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29128_Offer_the_Max_Bet_Out_of_Several_Selections(BaseBetSlipTest):
    """
    TR_ID: C29128
    NAME: Offer the Max Bet Out of Several Selections
    DESCRIPTION: This test case verifies offering the maximum value for one bet out of several selections by a trader triggered by overask functionality
    DESCRIPTION: *   BMA-6574 Overask - Trader's Simple actions
    DESCRIPTION: *   BMA-20390 New Betslip - Overask design improvements
    PRECONDITIONS: User is logged in
    PRECONDITIONS: TO UPDATE 'Accept & Bet' button is missing
    PRECONDITIONS: https://app.zeplin.io/project/5c892a4a1f719638a3fb8b0a/screen/5c892a87988ef41982599fbf
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
        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)
        self.__class__.expected_user_balance = self.site.header.user_balance

    def test_002_add_selections_and_go_betslip_singles_section(self):
        """
        DESCRIPTION: Add selections and go Betslip, 'Singles' section
        EXPECTED: As per description
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_ids[0], self.selection_ids[1]])

    def test_003_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button(
            self, bet_type='Single'):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for one of added selections and click / tap 'Bet Now' button
        EXPECTED: The bet is sent to Openbet system for review
        """
        if bet_type == 'Single':
            section = self.get_betslip_sections().Singles
        else:
            section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(section.items(), msg='*** No stakes found')

        self.__class__.stake_name1, self.__class__.stake1 = list(section.items())[0]
        if bet_type == 'Single':
            stake_bet_amounts1 = {self.stake_name1: self.max_bet + 0.01}
        else:
            stake_bet_amounts1 = {self.stake_name1: self.max_mult_bet + 0.01}
        self.enter_stake_amount(stake=(self.stake_name1, self.stake1), stake_bet_amounts=stake_bet_amounts1)
        self.get_betslip_content().bet_now_button.click()

    def test_004_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * 'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' message is displayed on yellow background anchored to the footer of the Betslip
        EXPECTED: * Loading spinner is displayed on the green button, replacing 'Bet Now' label
        EXPECTED: * 'Stake', 'Est. Returns' fields, 'Clear Betslip' and 'Bet Now' buttons are disabled and greyed out
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

    def test_005_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger offer with the max bet by a trader in OpenBet system
        EXPECTED: Confirmation is sent and received in Oxygen app
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.event_ids[0])
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        # self.bet_intercept.accept_bet(event_id=self.event_ids[0], bet_id=bet_id, betslip_id=betslip_id)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.max_bet,
                                       price_type='S')

    def test_006_verify_betslip(self, bet_type='Single'):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   Selection with the maximum bet offer is expanded
        EXPECTED: *   The maximum bet offer for selected on step #3 bet and enabled checked checkbox are shown to user
        EXPECTED: *   Message 'Note: You're accepting this Trade Offer' appears on the grey background below the checked selection
        EXPECTED: *   The rest of selections are shown unchanged
        EXPECTED: *   'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons are present
        EXPECTED: *   'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons are enabled
        """
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)
        self.assertTrue(overask_trader_message, msg=f'Overask trader message has not appeared')

        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

        betslip_section = self.get_betslip_content()
        est_returns = betslip_section.total_estimate_returns
        self.assertEqual(est_returns, 'N/A', msg='Est returns is not equal "N/A"')

        if bet_type == 'Single':
            section = self.get_betslip_sections().Singles
        else:
            section = self.get_betslip_sections(multiples=True).Multiples
        stake_name, stake = list(section.items())[0]
        self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for "{stake_name}" is not highlighted in yellow')

        self.assertTrue(betslip_section.has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.assertTrue(betslip_section.confirm_overask_offer_button.is_enabled(),
                        msg='"Place Bet" button is not enabled')

    def test_007_click__tap_accept__bet_button(self):
        """
        DESCRIPTION: Click / tap 'Accept & Bet' button
        EXPECTED: *   Bets are placed and balance is reduced accordingly
        EXPECTED: *   Bets are listed in 'Bet History' and 'My Account' pages
        """
        # not valid step from OX 99

    def test_008_repeat_steps__2_7(self):
        """
        DESCRIPTION: Repeat steps # 2-7
        """
        # not valid step from OX 99

    def test_009_click__tap_cancel_button(self):
        """
        DESCRIPTION: Click / tap 'Cancel' button
        EXPECTED: *   Bets are NOT placed
        EXPECTED: *   Selections are still present in Betslip
        EXPECTED: *   'Stake', 'Est.Returns', 'Total Stake' and 'Total Est. Returns' fields are empty
        """
        cancel_btn = self.get_betslip_content().cancel_button
        cancel_btn.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        self.assertTrue(dialog, msg='"CANCEL OFFER?" dialog is not shown')
        dialog.cancel_offer_button.click()
        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=6),
                             msg='Betslip widget was not closed')
        else:
            result = wait_for_result(lambda: self.get_betslip_content().no_selections_title,
                                     name='Betslip to be cleared',
                                     timeout=3)
            self.assertTrue(result, msg='BetSlip was not cleared')

    def test_010_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        EXPECTED: As per description
        """
        self.test_002_add_selections_and_go_betslip_singles_section()

    def test_011_repeat_steps__3_10_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-10 for Multiple bet
        EXPECTED: As per steps
        """
        self.test_003_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button(
            bet_type='Double')
        self.test_004_verify_betslip()
        self.test_005_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system()
        self.test_006_verify_betslip(bet_type='Double')
        self.test_007_click__tap_accept__bet_button()
        self.test_008_repeat_steps__2_7()
        self.test_009_click__tap_cancel_button()

    def test_012_add_a_few_selections_from_the_same_race_event_and_go_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and go Betslip, 'Forecasts/Tricasts' section
        EXPECTED: As per description
        """
        self.selection_ids.clear()
        self.event_ids.clear()
        for i in range(2):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=4, forecast=True,
                                                              max_bet=self.max_bet, max_mult_bet=self.max_mult_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)

    def test_013_repeat_steps__3_10_for_forecaststricastsbet(self):
        """
        DESCRIPTION: Repeat steps № 3-10 for Forecasts/Tricasts bet
        EXPECTED: As per steps
        """
        self.test_002_add_selections_and_go_betslip_singles_section()
        self.test_003_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button(
            bet_type='Double')
        self.test_004_verify_betslip()
        self.test_005_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system()
        self.test_006_verify_betslip(bet_type='Double')
        self.test_007_click__tap_accept__bet_button()
        self.test_008_repeat_steps__2_7()
        self.test_009_click__tap_cancel_button()
