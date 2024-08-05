import datetime
import pytest
import voltron.environments.constants as vec
import tests
from datetime import date
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@pytest.mark.p1
@vtest
class Test_C44870364_C44870296__verify_user_can_navigates_to_bet_history_page_by_clicking_on_My_Account(BaseBetSlipTest):
    """
    TR_ID: C44870364
    TR_ID: C44870296
    NAME: "- verify user can navigates to bet history page by clicking on My Account.
    DESCRIPTION: It is verify Bet History and its contents.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Used should be logged in
        PRECONDITIONS: User must have some single, double, each way and accumulator bets placed.
        PRECONDITIONS: User should have some settled bets.
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.navigate_to_page('bet-history')
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        if len(bets) > 0:
            self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')
        else:
            self._logger.info(f'***There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')

    def test_001_verify_user_can_navigates_to_bet_history_page_by_clicking_on_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: verify user can navigates to bet history page by clicking on History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: User is able to see My Bets with OPEN BETS and SETTLED BETS tabs.
        """
        tabs = self.site.bet_history.tabs_menu.items_as_ordered_dict
        for tab_name in tabs:
            self.site.bet_history.tabs_menu.items_as_ordered_dict.get(tab_name).click()
            if tab_name in vec.bet_history.SETTLED_BETS_TAB_NAME:
                self.assertTrue(tab_name, msg=f'Tab "{tab_name}" is found in "{vec.bet_history.SETTLED_BETS_TAB_NAME}"')
            elif tab_name in vec.bet_history.MY_BETS_TAB_NAMES:
                self.assertTrue(tab_name, msg=f'Tab "{tab_name}" is found in "{vec.bet_history.MY_BETS_TAB_NAMES}"')
                if self.device_type == 'mobile':
                    wait_for_result(lambda: self.site.back_button,
                                    name='Back Button is Available',
                                    timeout=2)
                    self.site.back_button.click()
                else:
                    self.device.go_back()
            else:
                self._logger.info(f'***Tab "{tab_name}" is not found')

    def test_002___verify_user_can_view_settled_bets_for_given_time_duration_by_setting_the_calender_dates__from_and_to_dates(self):
        """
        DESCRIPTION: - Verify user can view settled bets for given time duration by setting the Calender dates  (From and To Dates)
        EXPECTED: User is able to see all settled bets based on dates range set in calender.
        """
        if self.brand == 'bma':
            self.__class__.sports = vec.bma.SPORTS.upper()
        else:
            self.__class__.sports = vec.bma.SPORTS
        actual_past_date = date.today().__format__('%d/%m/%Y')
        self.site.bet_history.tab_content.accordions_list.date_picker.date_from.date_picker_value = actual_past_date
        expected_past_date = self.site.bet_history.tab_content.accordions_list.date_picker.date_from.text
        self.assertEqual(expected_past_date, actual_past_date,
                         msg=f'"{expected_past_date}" and "{actual_past_date}" are not same')
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        if (len(bets)) is 0:
            self._logger.info(f'***There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}"')
        else:
            self.site.bet_history.tab_content.grouping_buttons.click_button(self.sports)
            bet_headers = (self.site.bet_history.bet_types)[:5]
            for bet_type in bet_headers:
                if any(subheader in bet_type for subheader in vec.betslip.BETSLIP_BETTYPES):
                    _, bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=bet_type)
                    self.assertTrue(bet.date, msg=f'Bet date is not shown for bet type "{bet_type}"')
                    if bet.date == 'FT':
                        bet_date = datetime.datetime.strptime(bet.date_without_timer_label, '%H:%M - %d %b').strftime('%d/%m')
                    elif bet.date.find(','):
                        bet_date = datetime.datetime.strptime(bet.date, '%H:%M, %d %b').strftime('%d/%m')
                    else:
                        bet_date = datetime.datetime.strptime(bet.date, '%H:%M - %d %b').strftime('%d/%m')
                    from_date = date.today().__format__('%d/%m')
                    to_date = date.today().__format__('%d/%m')
                    if from_date <= bet_date <= to_date:
                        self.assertTrue(bet_date, msg=f' Bet is in dates range "{bet.bet_type}"')
                    else:
                        self._logger.info(f'*** Bet is not in dates range "{bet.bet_type}"')

    def test_003___verify_bet_history_of__sports__lotto_pools_tabs(self):
        """
        DESCRIPTION: - Verify bet history of  'Sports' , 'Lotto', 'Pools' tabs
        EXPECTED: User is able to see all settled bets based on dates range set in calender for these different bets.
        """
        settled_bet_tabs = self.site.bet_history.tab_content.grouping_buttons.items_as_ordered_dict
        self.assertTrue(settled_bet_tabs, msg='Settled Bet tabs are not displayed')
        for tab_name, tab in settled_bet_tabs.items():
            tab.click()
            expected_tab_name = self.site.bet_history.tab_content.grouping_buttons.current
            self.assertEqual(tab_name, expected_tab_name,
                             msg=f'"Actual {tab_name}" is not matched with expected "{expected_tab_name}"')
            bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
            if (len(bets)) is 0:
                self._logger.info(f'***There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}"')
            else:
                self.site.bet_history.tab_content.grouping_buttons.click_button(tab_name)
                bet_headers = (self.site.bet_history.bet_types)[:5]
                for bet_type in bet_headers:
                    if bet_type in vec.betslip.BETSLIP_BETTYPES:
                        _, bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=bet_type)
                        self.assertEqual(bet.bet_type, bet_type,
                                         msg=f'Bet type: "{bet.bet_type}" is not as expected: "{bet_type}"')
                        self.assertTrue(bet.date, msg=f'Bet date is not shown for bet type "{bet_type}"')

    def test_004___verify_user_can_scroll_down_the_past_bet_history(self):
        """
        DESCRIPTION: - Verify user can scroll down the past bet history
        EXPECTED: User is able to scroll down and see all bets.
        """
        sports_opened = self.site.bet_history.tab_content.grouping_buttons.click_button(self.sports)
        self.assertTrue(sports_opened, msg='Sports tab is not opened')
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        if (len(bets)) is 0:
            self._logger.info(f'***There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}"')
        else:
            last_bet = list(bets.keys())[-1]
            for name, item in list(bets.items()):
                self.assertTrue(name in list(bets.keys()), msg=f'{name} not found in settled bet')
                item.scroll_to_we()
                if name == last_bet:
                    self.assertEqual(list(bets.keys()).index(last_bet), len(bets) - 1,
                                     msg='Unable to scroll till last bet')
