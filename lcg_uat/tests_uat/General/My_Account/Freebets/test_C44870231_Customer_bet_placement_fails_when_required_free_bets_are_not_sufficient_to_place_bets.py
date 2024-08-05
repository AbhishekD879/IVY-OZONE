import pytest
import tests
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException


# @pytest.mark.prod # no freebets with value 0.00.  todo: it will work for prod if we have freebets users with value 0.00
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870231_Customer_bet_placement_fails_when_required_free_bets_are_not_sufficient_to_place_bets(BaseBetSlipTest):
    """
    TR_ID: C44870231
    NAME: Customer bet placement fails when required free bets are not sufficient to place bets
    PRECONDITIONS: Free bet amount 0.00
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        Description: Create event
        """
        self.__class__.selection_id = list(self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        self.site.wait_content_state('homepage')

    def test_002_login_with_above_user(self):
        """
        DESCRIPTION: Login with above user
        EXPECTED: User is logged in and free bet amount is displayed on My Account
        """
        self.site.login(tests.settings.freebet_user_with_value_0)
        self.navigate_to_page('freebets')
        freebets = self.site.freebets.freebets_content.items_as_ordered_dict
        self._logger.info(f'*** available freebets are: "{freebets}"')
        self.assertTrue(freebets, msg='No Free Bets found on page')
        for freebet in list(freebets.values()):
            if '0.0' in str(freebet.freebet_value):
                break
        else:
            raise VoltronException('Freebets not found')
        self.device.go_back()

    def test_003_verify_user_can_add_a_selection_to_betslip_and_unable_to_place_a_bet_using_freebet(self):
        """
        DESCRIPTION: Verify user can add a selection to betslip and unable to place a bet using freebet
        EXPECTED: Error message displayed
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        self.assertTrue(stake.has_use_free_bet_link(), msg=f'"Has Use Free Bet" link was not found')
        stake.freebet_tooltip.click()
        stake.use_free_bet_link.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, verify_name=False, timeout=5)
        self.assertTrue(dialog.items_as_ordered_dict,
                        msg=f'No freebets found in "{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" pop up')
        for free_bet in list(dialog.items_as_ordered_dict.keys()):
            if '£0' in free_bet:
                self.__class__.free_bet_name = free_bet
                break
        else:
            raise VoltronException('Freebets with value "0.00" not found')
        dialog.select_free_bet(free_bet_name=self.free_bet_name)
        info_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_INFORMATION, verify_name=False)
        self.assertEqual(info_dialog.description, vec.betslip.FREE_BET_CAN_NOT_BE_ADDED,
                         msg=f'Actual description: "{info_dialog.description}" is not same as '
                             f'Expected description: "{vec.betslip.FREE_BET_CAN_NOT_BE_ADDED}"')
