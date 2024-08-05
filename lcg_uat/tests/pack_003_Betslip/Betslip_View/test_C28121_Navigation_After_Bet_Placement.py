import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.bet_placement
@pytest.mark.bet_receipt
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.login
@vtest
class Test_C28121_Navigation_After_Bet_Placement(BaseBetSlipTest):
    """
    TR_ID: C28121
    NAME: Navigation After Bet Placement
    DESCRIPTION: This test case verifies REUSE SELECTION and DONE buttons on the Betslip
    PRECONDITIONS: User account with positive balance
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: create test event
        """
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        number_of_events=1)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException('No Home team found')
            self._logger.info(f'*** Found Football event id "{event["event"]["id"]}" with selection ids "{self.selection_ids}" and team "{self.team1}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1 = event_params.team1
            self.__class__.selection_ids = event_params.selection_ids

        self.__class__.selection_id = self.selection_ids[self.team1]

    def test_001_log_in_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Log in with User account with positive balance
        EXPECTED: - User is Logged In
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.balance = self.site.header.user_balance

    def test_002_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: - Selection are displayed in Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

        singles_section = self.get_betslip_sections().Singles
        selections_count = self.get_betslip_content().selections_count
        self.assertEqual(selections_count, '1',
                         msg=f'Singles selection count "%s" is not the same as expected "%s"' %
                             (selections_count, '1'))
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'"{self.team1}" stake was not found on the Betslip')

    def test_003_enter_value_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and tap 'Bet Now' button
        EXPECTED: -   Bet is placed
        EXPECTED: -   User`s balance is decreased by value entered in 'Stake' field
        EXPECTED: -   Bet Receipt is present with 'REUSE SELECTION' and 'DONE' buttons
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(self.balance - self.bet_amount, timeout=5)

        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='"Reuse Selections" button is not shown, Bet was not placed')
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(),
                        msg='"Done" button is not shown, Bet was not placed')

    def test_004_tap_reuse_selection_button(self):
        """
        DESCRIPTION: Tap 'REUSE SELECTION' button
        EXPECTED: -   User is navigated to 'Betslip' tab
        EXPECTED: -   Betslip contains all selection that user placed stake on
        """
        self.site.bet_receipt.footer.reuse_selection_button.click()

        singles_section = self.get_betslip_sections().Singles
        selections_count = self.get_betslip_content().selections_count
        self.assertEqual(selections_count, '1',
                         msg='Singles selection count "%s" is not the same as expected "%s"' %
                             (selections_count, '1'))
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'"{self.team1}" stake was not found on the Betslip')

    def test_005_enter_value_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and tap 'Bet Now' button
        EXPECTED: -   Bet is placed
        EXPECTED: -   User`s balance is decreased by value entered in 'Stake' field
        EXPECTED: -   Bet Receipt is present with 'REUSE SELECTION' and 'DONE' buttons
        """
        self.place_single_bet()
        self.verify_user_balance(self.balance - self.bet_amount * 2, timeout=5, delta=0.1)

        self.check_bet_receipt_is_displayed()

        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='"Reuse Selections" button is not shown, Bet was not placed')
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(),
                        msg='"Done" button is not shown, Bet was not placed')

    def test_006_tap_done_button(self):
        """
        DESCRIPTION: Tap 'DONE' button
        EXPECTED: Tablet/Desktop: 'You have no selections in this slip' message is present on the Betslip
        EXPECTED: Mobile: Betslip is closed
        """
        self.site.bet_receipt.footer.done_button.click()

        if self.is_mobile:
            self.assertFalse(self.site.has_betslip_opened(), msg='Bet Slip is not closed')
        else:
            self.device.refresh_page()
            self.site.wait_content_state('homepage')
            self.assertFalse(self.site.is_bet_receipt_displayed(expected_result=False), msg='Bet Receipt is not closed')
            betslip_name = self.get_betslip_content().name
            self.assertEqual(betslip_name, self.cms_config.constants.BETSLIP_WIDGET_NAME,
                             msg=f'Current tab is not the same as expected. '
                                 f'Actual: {betslip_name}. '
                                 f'Expected: {self.cms_config.constants.BETSLIP_WIDGET_NAME}')
            result = wait_for_result(lambda: self.get_betslip_content().no_selections_title,
                                     name='Betslip to be cleared',
                                     timeout=2)
            self.assertTrue(result, msg='BetSlip was not cleared')
            self.assertEqual(self.get_betslip_content().no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                             msg='BetSlip was not cleared')
