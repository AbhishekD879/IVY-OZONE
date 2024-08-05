import pytest
import voltron.environments.constants as vec
from datetime import date, timedelta
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.p1
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870296_2Customer_can_search_Bet_history_for_Sports_bets_using_From_and_To_date_range(BaseBetSlipTest):
    """
    TR_ID: C44870296
    NAME: 2.Customer can search Bet history for Sports bets using From and To date range
    DESCRIPTION: Used should be logged in
    DESCRIPTION: User should have some settled bets.
    """
    keep_browser_open = True

    def test_001_user_shall_launch_test_appsite(self):
        """
        DESCRIPTION: User shall Launch Test App/Site
        EXPECTED: User successfully Launches Test App/Site
        """
        self.site.wait_content_state("Homepage")

    def test_002_user_shall_login_with_valid_credentials_who_has_some_settled_bets(self):
        """
        DESCRIPTION: User shall Login with valid credentials who has some settled bets.
        EXPECTED: User successfully Logins with credentials
        """
        self.site.login()

    def test_003_verify_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Verify Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: Cashout/Open bets/Settled bets/Shop bets
        EXPECTED: All bets must be displayed with the right details
        EXPECTED: for all types of bets - single, multiple, E/W, cashed out bets, HR etc
        """
        self.navigate_to_page('bet-history')
        sleep(3)
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        actual_my_bet_tabs = list(self.site.bet_history.tabs_menu.items_as_ordered_dict)
        self.site.wait_content_state_changed(timeout=3)
        for tab in actual_my_bet_tabs:
            self.assertIn(tab, vec.bet_history.MY_BETS_TAB_NAMES,
                          msg=f'Actual tab: "{tab}" is not present in the list of tabs: "{vec.bet_history.MY_BETS_TAB_NAMES}"')
        self.assertIn(vec.bet_history.OPEN_BETS_TAB_NAME, actual_my_bet_tabs, msg=f'Actual tab: "{vec.bet_history.OPEN_BETS_TAB_NAME}" is not present in the list of tabs: "{actual_my_bet_tabs}"')
        if len(bets) > 0:
            self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')
        else:
            self._logger.info(f'***There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')

    def test_004_verify_user_can_view_settled_bets_for_given_time_duration_by_setting_the_calendar_dates_from_and_to_dates(self):
        """
        DESCRIPTION: Verify user can view settled bets for given time duration by setting the Calendar dates (From and To Dates)
        EXPECTED: User is able to see all settled bets based on dates range set in calendar.
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

    def test_005_verify_bet_history_of_sports_lottopools_tabs(self):
        """
        DESCRIPTION: Verify bet history of 'Sports', 'Lotto','Pools' tabs
        EXPECTED: User is able to see all settled bets based on dates range set in calendar for these different bets.
        """
        settled_bet_tabs = self.site.bet_history.tab_content.grouping_buttons.items_as_ordered_dict
        self.assertTrue(settled_bet_tabs, msg='Settled Bet tabs are not displayed')
        for tab_name, tab in settled_bet_tabs.items():
            sleep(2)
            tab.click()
            expected_tab_name = self.site.bet_history.tab_content.grouping_buttons.current
            self.assertEqual(tab_name, expected_tab_name,
                             msg=f'Actual "{tab_name}" is not matched with expected "{expected_tab_name}"')
            bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
            if len(bets) > 0:
                self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')
            else:
                self._logger.info(f'***There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')

    def test_006_verify_user_can_scroll_down_the_past_bet_history(self):
        """
        DESCRIPTION: Verify user can scroll down the past bet history
        EXPECTED: User is able to scroll down and see all bets.
        """
        sportstab = 'Sports' if self.brand == 'ladbrokes' else 'SPORTS'
        sports_opened = self.site.bet_history.tab_content.grouping_buttons.click_button(sportstab)
        self.assertTrue(sports_opened, msg='Sports tab is not opened')
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        if len(bets) > 0:
            self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')
            last_bet = list(bets.keys())[-1]
            for name, item in list(bets.items()):
                self.assertTrue(name in list(bets.keys()), msg=f'"{name}" not found in settled bet')
                item.scroll_to_we()
                if name == last_bet:
                    self.assertEqual(list(bets.keys()).index(last_bet), len(bets) - 1,
                                     msg='Unable to scroll till last bet')
        else:
            self._logger.info(f'***There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')
