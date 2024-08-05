import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.overask
@pytest.mark.uat
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898516_Verify_selection_is_removed_from_betslip_if_user_kills_the_app_browser_after_triggering_OA(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C59898516
    NAME: Verify selection is removed from betslip if user kills the app/browser after triggering OA.
    """
    keep_browser_open = True
    max_bet = 1
    prices = {0: '1/12'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices,
                                                          max_bet=self.max_bet)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user

    def test_001_login_add_selection_and_trigger_oa(self):
        """
        DESCRIPTION: Login, Add selection and trigger OA
        EXPECTED: OA is triggered
        """
        self.site.login(self.username)
        self.site.close_all_dialogs()
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_kill_appbrowser(self):
        """
        DESCRIPTION: Kill app/browser
        EXPECTED: User is logged out and betslip is empty
        """
        self.logout_in_new_tab()
        self.verify_logged_out_state()
        self.site.open_betslip()
        message = self.site.betslip.no_selections_title
        self.assertEqual(message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'"{message}" is not same as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

    def test_003_log_back_in(self):
        """
        DESCRIPTION: Log back in
        EXPECTED: Uses logs in and betslip should be empty
        """
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_content_state('HomePage')
        self.site.login(self.username)
        self.site.close_all_dialogs()
        self.site.open_betslip()
        message = self.site.betslip.no_selections_title
        self.assertEqual(message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'"{message}" is not same as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
