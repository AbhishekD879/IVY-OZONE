import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.p2
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870328_Place_a_multiple_bet_with_in_play_and_preplay_events(BaseBetSlipTest):
    """
    TR_ID: C44870328
    NAME: Place a multiple bet with in play and preplay events
    DESCRIPTION: This test case verifies placing a Multiples on inplay and preplay events
    """
    keep_browser_open = True
    number_of_stakes = 1

    def test_001_load_httpsbeta_sportscoralcouklogin_with_user_with_positive_balance(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk/
        DESCRIPTION: Login with user with positive balance
        EXPECTED: Homepage opened
        EXPECTED: user is logged in
        """
        self.site.login()

    def test_002_add_several_selections_from_different_inplay_and_preplay_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections from different inplay and preplay events to the betslip
        EXPECTED: Selections are displayed
        """
        # TODO: Add inplay events when actual match start
        football_pre_play_selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
        football_pre_play_selection_ids2 = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
        football_selection_ids3 = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
        self.__class__.selection_ids = (list(football_pre_play_selection_ids.values())[0], list(football_pre_play_selection_ids2.values())[0],
                                        list(football_selection_ids3.values())[0])

    def test_003_open_betslip_and_scroll_down_to_multiples_section(self):
        """
        DESCRIPTION: Open Betslip and scroll down to 'Multiples' section
        EXPECTED: Multiples are displayed
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.multiple_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(self.multiple_section, msg='"Betslip Multiple" section is not displayed.')

    def test_004_enter_stake_for_one_of_available_multiples(self):
        """
        DESCRIPTION: Enter Stake for one of available Multiples
        EXPECTED: Est. Returns, Total Stake and Total Est. Returns fields are calculated
        """
        self.__class__.user_balance = self.get_balance_by_page('betslip')
        self.__class__.betslip_info = self.place_and_validate_multiple_bet(number_of_stakes=self.number_of_stakes)

    def test_005_tap_on_place_bet(self):
        """
        DESCRIPTION: Tap on 'Place Bet'
        EXPECTED: Multiple Bet is placed successfully (the one which had entered Stake, the rest Multiples are ignored)
        EXPECTED: User balance is decreased by Total Stake
        EXPECTED: Bet Receipt page is shown with the correct information about placed bet
        """
        self.check_bet_receipt_is_displayed()
        self.check_bet_receipt(self.betslip_info)
        betreceipt_section = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_section, msg='There is no "Bet Receipt"')
        self.verify_user_balance(expected_user_balance=self.user_balance - self.bet_amount * self.number_of_stakes)

    def test_006_tap_reuse_selection_or_go_betting(self):
        """
        DESCRIPTION: Tap 'Reuse selection' or 'Go betting'
        EXPECTED: On clicking
        EXPECTED: Reuse selection > User is navigated to the betslip with the same selections
        EXPECTED: Go betting > User is navigated to the Previous page.
        """
        reuse_selection_button = self.site.bet_receipt.footer.has_reuse_selections_button()
        self.assertTrue(reuse_selection_button, msg='There is no "Reuse Selection" button on Bet receipt')
        reuse_selection_button.click()
        self.assertTrue(self.multiple_section, msg='Betslip Multiple section is not displayed.')
        self.place_and_validate_multiple_bet()
        self.site.bet_receipt.footer.done_button.click()
        self.assertFalse(self.site.is_bet_receipt_displayed(expected_result=False), msg='"Bet Slip" is not closed yet')
