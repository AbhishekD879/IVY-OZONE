import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C33112139_Vanilla_Deposit_link_in_the_Betslip_header(BaseBetSlipTest):
    """
    TR_ID: C33112139
    NAME: [Vanilla] Deposit link in the Betslip header
    DESCRIPTION: This test case verifies that Deposit page is opened through Deposit link in the Betslip header
    PRECONDITIONS: User account with added credit cards and positive balance
    PRECONDITIONS: Applies for Mobile
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(
                category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'*** Found Football event with selections  "{self.selection_ids}"')
            self.__class__.team1_1 = list(self.selection_ids.keys())[0]
        else:
            event_params1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1_1, self.__class__.selection_ids = event_params1.team1, event_params1.selection_ids

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        # done in next step

    def test_002_log_in_with_user_account__from_preconditions(self):
        """
        DESCRIPTION: Log in with User account ( from Preconditions)
        EXPECTED: User is logged in
        """
        self.site.login(tests.settings.deposit_page_users)
        self.site.wait_content_state('HomePage')

    def test_003_add_a_selection_to_the_betslip___open_betslip_page(self):
        """
        DESCRIPTION: Add a selection to the Betslip -> Open Betslip page
        EXPECTED: Selection is displayed within Betslip content area
        EXPECTED: User balance is displayed in the header
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1_1])
        self.__class__.betslip_content = self.get_betslip_content()
        self.assertTrue(self.betslip_content.header.has_user_balance,
                        msg='Balance is not displayed at the top right corner')

    def test_004_tap_on_user_balance_area_in_the_betslip_header__deposit_button(self):
        """
        DESCRIPTION: Tap on User Balance area in the Betslip header > Deposit button
        EXPECTED: Deposit page is opened
        """
        self.betslip_content.quick_deposit_link.click()
        self.assertTrue(wait_for_result(lambda: self.site.deposit.deposit_title, timeout=15),
                        msg=f'User is not navigated to "{vec.bma.DEPOSIT}" page')
        actual_title = self.site.deposit.deposit_title.text.split('\n')[0]
        self.assertEqual(actual_title.upper(), vec.bma.DEPOSIT.upper(),
                         msg=f'Actual title: "{actual_title.upper()}" is not same as'
                             f'Expected title: "{vec.bma.DEPOSIT.upper()}"')

    def test_005_close_the_deposit_page_x(self):
        """
        DESCRIPTION: Close the Deposit page ('X')
        EXPECTED: Deposit page is closed. Homepage is displayed
        """
        self.site.deposit.close_button.click()
        self.assertTrue(self.site.wait_content_state('HomePage'), msg='"homepage" is not displayed')
