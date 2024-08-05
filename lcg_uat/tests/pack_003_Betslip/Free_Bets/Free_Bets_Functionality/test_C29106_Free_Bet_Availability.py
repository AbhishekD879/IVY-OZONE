import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot grant freebet on PROD/HL
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.freebets
@pytest.mark.login
@vtest
class Test_C29106_Free_Bet_Availability(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C29106
    TR_ID: C16706424
    NAME: Free Bet Availability
    DESCRIPTION: This test case verifies 'Free Bet' drop down
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-10318 update an error message
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User should have Free Bets available on their account
    PRECONDITIONS: 3. User should have at least one selection added to the Betslip
    PRECONDITIONS: NOTE: Contact Coral UAT for assistance with applying free bet tokens to the relevant test accounts
    """
    keep_browser_open = True
    freebet_value, freebet_value2 = 1.11, 2.22

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event and grant freebet to user
        """
        params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = params.selection_ids
        self.__class__.team1 = params.team1
        self.__class__.team2 = params.team2
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.ob_config.grant_freebet(username=username, freebet_value=self.freebet_value)
        self.ob_config.grant_freebet(username=username, freebet_value=self.freebet_value2)

    def test_001_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip is open
        """
        self.__class__.selection_id = self.selection_ids['Draw']
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_verify_use_free_bet_link_is_present_under_selection_and_press_on_it(self):
        """
        DESCRIPTION: Verify "Use Free Bet" link is present under selection and press on it
        EXPECTED: Free Bet Pop up is shown with list of Free Bets available
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.has_use_free_bet_link(), msg='"Has Use Free Bet" link was not found')
        stake.freebet_tooltip.click()
        stake.use_free_bet_link.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5, verify_name=False)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not shown')
        self.assertTrue(self.dialog.items_as_ordered_dict, msg='No freebets found in "{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" pop up')

        self.__class__.stake = stake

    def test_003_select_one_of_available_free_bets_from_free_bet_pop_up(self):
        """
        DESCRIPTION: Select one of available Free Bets from Free Bet pop up
        EXPECTED: * Selected Free Bet has check box marked as selected
        EXPECTED: * Pop up is closed (in 0.2 sec)
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        """
        self.__class__.freebet_stake = self.dialog.select_free_bet(free_bet_name=self.get_freebet_name(value=self.freebet_value))

        self.assertTrue(self.dialog.wait_dialog_closed(), msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not closed')

        self.assertTrue(self.stake.has_remove_free_bet_link(), msg='"Remove Free Bet" link was not found')

    def test_004_verify_estimated_returns_value_when_free_bet_is_selected(self):
        """
        DESCRIPTION: Verify 'Estimated Returns' value when free bet is selected
        EXPECTED: 'Estimated Returns' is calculated based on formula:
        EXPECTED: **Free Bet Value * Odds** - if odds have a fractional format
        EXPECTED: **Free Bet Value * Odds - Free Bet Value** - if odds have a decimal format
        """
        odds = self.stake.odds
        self.verify_estimated_returns(
            est_returns=float(self.stake.est_returns),
            odds=odds, bet_amount=0, freebet_amount=float(self.freebet_stake)
        )

    def test_005_press_on_remove_free_bet_link(self):
        """
        DESCRIPTION: * Press on "- Remove Free Bet" link
        EXPECTED: * "- Remove Free Bet" link is changed to "Use Free Bet" link
        EXPECTED: * 'Estimated Returns' is changed to 0.00
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        stake.remove_free_bet_link.click()
        self.assertTrue(stake.has_use_free_bet_link(timeout=5), msg='"Has Use Free Bet" link was not found')
        est_returns = stake.est_returns
        self.assertEqual(est_returns, '0.00', msg=f'Estimated Returns value "{est_returns}" is not changed to 0.00')

    def test_006_add_few_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add few more selections to the Betslip
        EXPECTED: Betslip counter is increased, added selection are present in the Betslip
        """
        self.__class__.selection_id2 = self.selection_ids[self.team1]
        self.open_betslip_with_selections(selection_ids=self.selection_id2, timeout=5)

    def test_007_go_to_selection_1_free_bet_pop_up_and_choose_one_of_available_free_bets(self):
        """
        DESCRIPTION: Go to selection #1 Free Bet pop up and choose one of available free bets
        EXPECTED: Free bet is chosen successfully
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertTrue(self.stake.has_use_free_bet_link(), msg='"Has Use Free Bet" link was not found')

        self.__class__.stake2_name, self.__class__.stake2 = list(singles_section.items())[1]
        self.stake.use_free_bet_link.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5,
                                           verify_name=False)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" pop up is not shown')
        self.assertTrue(dialog.items_as_ordered_dict,
                        msg=f'No freebets found in "{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" pop up for stake "{self.stake_name}"')

        self.__class__.freebet_stake = dialog.select_free_bet(free_bet_name=self.get_freebet_name(value=self.freebet_value))
        self.assertTrue(dialog.wait_dialog_closed(),
                        msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not closed')

    def test_008_go_to_selection_2_free_bet_pop_up_and_verify_if_free_bet_chosen_for_selection_1_is_present_in_the_list(self):
        """
        DESCRIPTION: Go to selection #2 'Free Bet pop up and verify if free bet chosen for selection #1 is present in the list
        EXPECTED: Free bet chosen for selection #1 isn't shown in the list of free bets for selection #2
        """
        self.stake2.use_free_bet_link.click()
        dialog2 = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5,
                                            verify_name=False)
        self.assertTrue(dialog2, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not shown')
        freebet_name = self.get_freebet_name(value=self.freebet_value)
        self.assertNotIn(freebet_name, dialog2.items_as_ordered_dict,
                         msg=f'Freebet "{freebet_name}" is found in "{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" '
                             f'pop up for stake "{self.stake2_name}"')
        dialog2.close_dialog()
        dialog2.wait_dialog_closed()

        self.stake.remove_free_bet_link.click()

    def test_009_add_few_more_selections_to_the_betslip_so_quantity_of_selections_is_bigger_than_quantity_of_free_bets_available_for_user(self):
        """
        DESCRIPTION: Add few more selections to the Betslip, so quantity of selections is bigger than quantity of Free Bets available for User
        EXPECTED: Betslip counter is increased, added selection are present in the Betslip
        """
        self.__class__.selection_id3 = self.selection_ids[self.team2]
        self.open_betslip_with_selections(selection_ids=self.selection_id3)

    def test_010_add_all_available_free_bets_to_selections(self):
        """
        DESCRIPTION: Add all available Free Bets to selections
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link for selections with Free Bets added
        EXPECTED: * After User has added all available Free Bets to selections, "Use Free Bet" link for other selections is greyed out and non-clickable
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        stake.use_free_bet_link.click()
        self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.freebet_value))

        stake2_name, stake2 = list(singles_section.items())[1]
        stake2.use_free_bet_link.click()
        self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.freebet_value2))

        stake3_name, stake3 = list(singles_section.items())[2]
        self.assertFalse(stake3.use_free_bet_link.is_enabled(expected_result=False, timeout=2),
                         msg=f'Stake "{stake3_name}" Use Freebet link is not greyed out')
