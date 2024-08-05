import pytest
import tests
import voltron.environments.constants as vec
from datetime import datetime
from datetime import timedelta
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # as we can not grant the freebet and odd boost tokens in prod
# @pytest.mark.hl
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870271_Verify_user_can_not_place_boosted_bet_with_freebet_token__Verify_the_error_message_pop_up_accept_and_cancel_features(BaseBetSlipTest, BaseSportTest, BaseUserAccountTest):
    """
    TR_ID: C44870271
    NAME: "Verify user can not place boosted bet with freebet token. - Verify the error message pop up accept and cancel features."
    DESCRIPTION:
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add Selection with Odds Boost available to the Betslip
    """
    keep_browser_open = True
    username = tests.settings.odds_boost_user

    def test_000_preconditions(self):
        """
        DESCRIPTION: Log in as a user from preconditions
        """
        cms_status = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if cms_status is None:
            self.cms_config.update_odds_boost_config(enabled=False)

        selection_ids = self.ob_config.add_autotest_premier_league_football_event(
            default_market_name='|Draw|').selection_ids
        self.__class__.home_team, self.__class__.home_team_selection_id = list(selection_ids.items())[0]
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.home_team_selection_id)
        exp_date = datetime.now() + timedelta(hours=1)
        self.ob_config.grant_freebet(username=self.username, level='selection',
                                     id=self.home_team_selection_id,
                                     expiration_date=exp_date)
        self.site.login(username=self.username)
        self.site.close_all_dialogs()

    def test_001_navigate_to_betslip_and_tap_boost_button(self):
        """
        DESCRIPTION: Navigate to Betslip and Tap 'BOOST' button
        EXPECTED: BOOST' button is changed to 'BOOSTED' with animation
        EXPECTED: Boosted odds is shown
        EXPECTED: Original odds is shown as crossed out
        """
        self.open_betslip_with_selections(selection_ids=self.home_team_selection_id)
        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header, msg='Odds boost header is not available')
        odds_boost_header.boost_button.click()
        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        if self.brand == 'bma':
            self.assertTrue(odds_boost_header.boost_button.has_boost_indicator,
                            msg='Boost button does not have boost indicator')
        else:
            self.assertIn('enabled', odds_boost_header.boost_button.boost_indicator,
                          msg='Boost-meter did not animate during odds boosting')

        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.home_team, self.singles_section, msg=f'"{self.home_team}" stake is not available')
        stake = self.singles_section[self.home_team]
        self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.check_odds_format(odds=stake.boosted_odds_container.price_value)
        self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')

    def test_002_choose_one_of_the_available_free_betsverify_that_information_popup_is_displayed(self):
        """
        DESCRIPTION: Choose one of the available free bets
        DESCRIPTION: Verify that information popup is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: Hardcoded text: "Continue with Free Bet? Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?"
        EXPECTED: 'NO THANKS' button
        EXPECTED: 'YES PLEASE' button
        """
        stake_name, stake = list(self.singles_section.items())[0]
        self.assertTrue(stake.has_use_free_bet_link(), msg=f'{vec.betslip.USE_FREE_BET} link was not found')
        stake.use_free_bet_link.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5,
                                                          verify_name=False)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not shown')
        self.assertTrue(self.dialog.items_as_ordered_dict,
                        msg=f'No freebets found in "{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" pop up')
        self.dialog.select_first_free_bet()
        self.assertTrue(self.dialog.wait_dialog_closed(), msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" '
                                                              f'dialog is not closed')
        self.__class__.dialog2 = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_CONTINUE_WITH_FREE_BET,
                                                           timeout=5,
                                                           verify_name=False)
        if self.brand == 'ladbrokes':
            self.assertEqual(self.dialog2.title, vec.odds_boost.BETSLIP_DIALOG.continue_with_freebet,
                             msg=f'"{vec.odds_boost.BETSLIP_DIALOG.continue_with_freebet}" '
                                 f'information is not shown on pop up')
            self.assertTrue(self.dialog2.no_thanks_button,
                            msg=f'"{vec.odds_boost.BETSLIP_DIALOG.no_thanks}" button is not on pop up')
            self.assertTrue(self.dialog2.yes_please_button,
                            msg=f'"{vec.odds_boost.BETSLIP_DIALOG.yes_please}" button is not on pop up')
        else:
            self.assertEqual(self.dialog2.title, vec.odds_boost.BETSLIP_DIALOG.continue_with_freebet.upper(),
                             msg=f'"{vec.odds_boost.BETSLIP_DIALOG.continue_with_freebet.upper()}" '
                                 f'information is not shown on pop up')
            self.assertTrue(self.dialog2.no_thanks_button,
                            msg=f'"{vec.odds_boost.BETSLIP_DIALOG.no_thanks.upper()}" button is not on pop up')
            self.assertTrue(self.dialog2.yes_please_button,
                            msg=f'"{vec.odds_boost.BETSLIP_DIALOG.yes_please.upper()}" button is not on pop up')
        self.assertEqual(self.dialog2.description, vec.odds_boost.BETSLIP_DIALOG.cancel_boost_price_message,
                         msg=f'"{vec.odds_boost.BETSLIP_DIALOG.cancel_boost_price_message}"'
                             f' button is not shown on pop up')

    def test_003_tap_no_thanks_buttonverify_that_popup_is_closed_and_odds_boost_remains_selected(self):
        """
        DESCRIPTION: Tap 'NO THANKS' button
        DESCRIPTION: Verify that popup is closed and odds  boost remains selected
        EXPECTED: Popup is closed
        EXPECTED: Odds Boost button remains selected (show as BOOSTED)
        EXPECTED: Odds is shown in boosted state
        EXPECTED: Original odds remains cross out
        EXPECTED: The free bet is deselected (removed)
        """
        self.dialog2.no_thanks_button.click()
        self.assertTrue(self.dialog.wait_dialog_closed(),
                        msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_CONTINUE_WITH_FREE_BET}" '
                            f'dialog is not closed')
        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        self.assertIn(self.home_team, self.singles_section, msg=f'"{self.home_team}" stake is not available')
        stake = self.singles_section[self.home_team]
        self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.check_odds_format(odds=stake.boosted_odds_container.price_value)
        self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')
        self.assertTrue(stake.has_use_free_bet_link(), msg='"Has Use Free Bet" link was not found')

    def test_004_choose_one_of_the_available_free_bets_one_more_timeverify_that_information_popup_is_displayed(self):
        """
        DESCRIPTION: Choose one of the available free bets one more time
        DESCRIPTION: Verify that information popup is displayed
        EXPECTED: nformation popup is displayed with the following items:
        EXPECTED: Hardcoded text: "Continue with Free Bet? Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?"
        EXPECTED: 'NO THANKS' button
        EXPECTED: 'YES PLEASE' button
        """
        self.__class__.singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(self.singles_section.items())[0]
        self.assertTrue(self.stake.has_use_free_bet_link(), msg=f'"Has Use Free Bet" link was not found')
        self.stake.use_free_bet_link.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5,
                                                          verify_name=False)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not shown')
        self.assertTrue(self.dialog.items_as_ordered_dict,
                        msg=f'No freebets found in "{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" pop up')
        self.dialog.select_first_free_bet()
        self.assertTrue(self.dialog.wait_dialog_closed(), msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" '
                                                              f'dialog is not closed')
        self.__class__.dialog2 = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_CONTINUE_WITH_FREE_BET,
                                                           timeout=5,
                                                           verify_name=False)
        self.assertTrue(self.dialog2.yes_please_button.is_displayed(),
                        msg=f'"YES PLEASE" button not displayed on"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE} pop up')
        self.assertTrue(self.dialog2.no_thanks_button.is_displayed(),
                        msg=f'"NO THANKS" button not displayed on "{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE} pop up')

    def test_005_tap_yes_please_buttonverify_that_popup_is_closed_and_freebet_remains_selected(self):
        """
        DESCRIPTION: Tap 'YES PLEASE' button
        DESCRIPTION: Verify that popup is closed and Freebet remains selected
        EXPECTED: Popup is closed
        EXPECTED: The selected free bet remains selected
        EXPECTED: The odds boost button is rolled back to an unboosted state (show as BOOST)
        EXPECTED: Odds of is rolled back to an unboosted state
        """

        self.dialog2.yes_please_button.click()
        self.assertTrue(self.dialog.wait_dialog_closed(),
                        msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_CONTINUE_WITH_FREE_BET}" '
                            f'dialog is not closed')
        self.site.close_all_dialogs()
        self.assertTrue(self.stake.remove_free_bet_link, msg=f'"{vec.betslip.REMOVE_FREE_BET}" link was not found')
        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
                                 name='"BOOSTED" button to become "BOOST" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOSTED" button did not change to "BOOST" button')
