import pytest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't change the status of selections
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C9346554_TO_BE_EDITED_Verify_the_flow_when_the_game_result_LOSE(BaseBetSlipTest):
    """
    TR_ID: C9346554
    NAME: [TO BE EDITED] Verify the flow when the game result LOSE
    DESCRIPTION: This test case verifies that the flow for EMA edit mode when game result LOSE
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place a bet on TREBLE or more (All selections in the placed bet are active and open)
    PRECONDITIONS: Go To My Bets>Cash OUt / Open Bets
    PRECONDITIONS: Tap 'EDIT MY ACCA' button for placed bet
    PRECONDITIONS: Test case should be run on Cash out tab and on Open Bets tab
    PRECONDITIONS: NOTE: LOSE result should be set to the appropriate selection in the bet
    """
    keep_browser_open = True
    bet_type = 'TREBLE'

    @classmethod
    def custom_setUp(cls):
        acca_section_status = cls.get_initial_data_system_configuration().get('EMA', {})
        if not acca_section_status:
            acca_section_status = cls.get_cms_config().get_system_configuration_item('EMA')
        if not acca_section_status.get('enabled'):
            raise CmsClientException('My ACCA section is disabled in CMS')

    def get_bets(self):
        self.site.open_my_bets_open_bets()
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=self.bet_type,
            selection_ids=self.selection_ids)

    def test_000_preconditions(self):
        """
        event creation
        """
        edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
        if not edit_my_acca_status:
            self.cms_config.set_my_acca_section_cms_status(ema_status=True)
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in CMS')
        upcoming = self.get_date_time_formatted_string(hours=2)
        event = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        event2 = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        event3 = self.ob_config.add_autotest_premier_league_football_event(start_time=upcoming)
        self.selection_ids = [event.selection_ids[event.team1],
                              event2.selection_ids[event2.team1],
                              event3.selection_ids[event3.team1]]

        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        self.__class__.event_id = event.event_id
        self.__class__.market_id = self.ob_config.market_ids[event.event_id][market_short_name]
        self.__class__.selection_id = event.selection_ids[event.team1]
        self.site.login()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        if self.device_type == "mobile":
            self.site.bet_receipt.footer.click_done()

    def test_001_go_to_ti_and_set_lose_result_for_any_event_in_the_placed_betverify_that_selection_removal_button_is_not_shown_for_resulted_event_and_error_message_is_displayed_your_acca_is_no_longer_active(
            self):
        """
        DESCRIPTION: Go to TI and set 'LOSE' result for any event in the placed bet
        DESCRIPTION: Verify that 'Selection Removal' button is not shown for resulted event and error message is displayed "Your Acca is no longer active"
        EXPECTED: Edit mode is opened with appropriate elements:
        EXPECTED: - 'LOST' label (red cross icon) is shown for resulted event
        EXPECTED: - 'Selection Removal' button is NOT shown for resulted event
        EXPECTED: - 'Selection Removal' button is NOT shown for other events
        EXPECTED: - Error message is displayed "Your Acca is no longer active"
        EXPECTED: - 'CANCEL EDITING' button is shown and clickable
        EXPECTED: - 'CONFIRM' button is shown and NOT clickable
        EXPECTED: NOTE: On Cash Out tab the bet will disappear after setting result
        """
        self.get_bets()
        returns_before_settlement = self.bet.est_returns.value
        EMB_button = wait_for_result(lambda: self.bet.edit_my_acca_button,
                                     name=f'"{vec.ema.EDIT_MY_BET}" button will be displayed')
        self.assertTrue(EMB_button, msg=f'"{vec.ema.EDIT_MY_BET}" is not displayed')
        self.bet.edit_my_acca_button.click()
        self.ob_config.update_selection_result(event_id=self.event_id, market_id=self.market_id,
                                               selection_id=self.selection_id, result='L')
        self.device.refresh_page()
        self.get_bets()
        sleep(7)
        self.bet.edit_my_acca_button.click()
        selection = list(self.bet.items_as_ordered_dict.values())[0]
        self.site.wait_splash_to_hide(5)
        self.assertTrue(selection.icon.is_displayed(),
                        msg=f'LOST label (red cross icon) "{vec.betslip.CANCELLED_STAKE.title()}" is not displayed')
        for selection in list(self.bet.items_as_ordered_dict.values())[1:]:
            self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                             msg='"Selection removal icon(X)" is displayed for resulted and other events')
        self.assertFalse(selection.has_edit_my_acca_remove_icon(expected_result=False),
                         msg='"Selection removal icon(X)" is displayed')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.ema.CANCEL.upper()}" button is not enabled')
        self.assertFalse(self.bet.confirm_button.is_enabled(expected_result=False),
                         msg=f'"{vec.ema.CONFIRM_EDIT}" button is enabled')
        returns_after_settlement = self.bet.est_returns.value
        self.assertNotEqual(returns_after_settlement, returns_before_settlement,
                            msg=f'Returns after settlement "{returns_after_settlement}" is still same as Returns before settlement "{returns_before_settlement}"')
        self.assertFalse(self.bet.confirm_button.is_enabled(),
                         msg=f'"{vec.ema.CONFIRM_EDIT}" button is  clickable')
