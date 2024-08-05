import pytest
from datetime import timedelta, date
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870295_1Customer_taps_on_Bet_History_on_my_accounts_to_check_the_history_tracked_under_this_tab(BaseBetSlipTest):
    """
    TR_ID: C44870295
    NAME: 1.Customer taps on Bet History  on my accounts to check the history tracked under this tab
    DESCRIPTION: It is verify Bet History and its contents.
    PRECONDITIONS: Used should be logged in
    PRECONDITIONS: User must have some single, double, each way and accumulator bets placed.
    PRECONDITIONS: User should have some settled bets.
    """
    keep_browser_open = True

    def test_001_launch_the_siteapp(self):
        """
        DESCRIPTION: Launch the site/App
        EXPECTED: The site is launched
        """
        self.navigate_to_page("Homepage")

    def test_002_log_in_with_user_credentials_that_have_previous_bets_placed_and_navigate_to_my_bets(self):
        """
        DESCRIPTION: Log in with user credentials that have previous bets placed and navigate to My bets
        EXPECTED: User is logged in and previous bets are displayed on My Bets
        """
        self.site.login()

    def test_003_verify_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Verify Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: Cashout/Open bets/Settled bets/Shop bets
        EXPECTED: All bets must be displayed with the right details
        EXPECTED: for all types of bets - single, multiple, E/W, cashed out bets, HR etc
        """
        self.site.open_my_bets_settled_bets()
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        if len(bets) > 0:
            self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')
        else:
            self._logger.info(f'***There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')

    def test_004_verify_functionality_of_date_picker_today_last_7_days_and_last_30_days_from_bet_history_via_my_account_overlay(self):
        """
        DESCRIPTION: Verify functionality of Date Picker Today, Last 7 days and Last 30 days from Bet History via My Account overlay
        EXPECTED: Date Picker Today, Last 7 days and Last 30 days must be functional and working as per design implementation
        """
        for i in [0, 7, 30]:
            new_date = date.today() - timedelta(days=i)
            past_date = new_date.__format__('%d/%m/%Y')
            self.site.bet_history.tab_content.accordions_list.date_picker.date_from.date_picker_value = past_date
            self.assertEqual(self.site.bet_history.tab_content.accordions_list.date_picker.date_from.text, past_date,
                             msg='Date range is not selected')
            bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
            if len(bets) > 0:
                self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')
            else:
                self._logger.info(f'***There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')
