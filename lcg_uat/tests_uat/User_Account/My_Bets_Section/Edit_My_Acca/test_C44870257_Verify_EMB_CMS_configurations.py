import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.cms
# @pytest.mark.prod it cann't be run on Production as it is related to CMS
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870257_Verify_EMB_CMS_configurations(BaseBetSlipTest):
    """
    TR_ID: C44870257
    NAME: Verify EMB CMS configurations
    PRECONDITIONS: User logged in
    PRECONDITIONS: User have accumulator bets
    """
    keep_browser_open = True
    bet_amount = 5
    selection_ids = []

    def test_001_enabled_emb_checkbox_in_cms(self, ema_status=True, expected_betslip_counter_value=0):
        """
        DESCRIPTION: Enabled EMB checkbox in cms
        EXPECTED: EMB is displayed in front end
        EXPECTED: Note: when place a accumulator bet EMB should be displayed on MY Bets area.
        """
        # Preconditions are covered in this step
        if self.site.wait_logged_out():
            self.site.login()

        self.cms_config.set_my_acca_section_cms_status(ema_status)

        event = self.ob_config.add_autotest_premier_league_football_event()
        event2 = self.ob_config.add_autotest_premier_league_football_event()
        event3 = self.ob_config.add_autotest_premier_league_football_event()
        event4 = self.ob_config.add_autotest_premier_league_football_event()
        self.selection_ids = [event.selection_ids[event.team1], event2.selection_ids[event2.team1],
                              event3.selection_ids[event3.team1], event4.selection_ids[event4.team1]]

        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state(state_name='HomePage')
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.bet = list(bets.values())[0]

        if ema_status:
            self.assertTrue(self.bet.has_edit_my_acca_button(),
                            msg='"Edit my bet" button is not displayed')

    def test_002_disabled_emb_checkbox_in_cms(self):
        """
        DESCRIPTION: Disabled EMB checkbox in cms
        EXPECTED: EMB should not displayed in front end.
        EXPECTED: Note: when place a accumulator bet EMB should not displayed on MY Bets area.
        """
        try:
            self.test_001_enabled_emb_checkbox_in_cms(ema_status=False)
            self.assertFalse(self.bet.has_edit_my_acca_button(),
                             msg='"Edit my bet" button is displayed')
        finally:
            # Reverting the EMA status as I have modified it in the script
            self.cms_config.set_my_acca_section_cms_status(ema_status=True)
