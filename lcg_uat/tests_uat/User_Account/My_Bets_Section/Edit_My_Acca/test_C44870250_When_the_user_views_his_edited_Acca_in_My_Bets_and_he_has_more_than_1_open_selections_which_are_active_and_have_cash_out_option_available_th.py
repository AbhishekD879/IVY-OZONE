import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.acca
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.open_bets
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870250_When_the_user_views_his_edited_Acca_in_My_Bets_and_he_has_more_than_1_open_selections_which_are_active_and_have_cash_out_option_available_then_the_cash_out_button_must_be_displayed_with_Cash_out_value_on_the_button_bVerify_Edit_My_Bet_button_is_n(BaseBetSlipTest):
    """
    TR_ID: C44870250
    NAME: "When the user views his edited Acca in My Bets and he has more than 1 open selections which are active and have cash out option available then the cash out button must be displayed with Cash out value on the button (b)Verify Edit My Bet button is n
    DESCRIPTION: "When the user views his edited Acca in My Bets and he has more than 1 open selections which are active and have cash out option available then the cash out button must be displayed with Cash out value on the button
    DESCRIPTION: (b)Verify Edit My Bet button is no longer displayed for the user when only one selection remains open ."
    # "This TC written on QA2 env"
    """
    keep_browser_open = True
    number_of_events = 4

    def test_000_preconditions(self):
        """
        DESCRIPTION: "User Should have Acca Bet."
        EXPECTED: "User views his Edit Acca in My Bets."
        """
        system_configuration = self.cms_config.get_system_configuration_structure()
        ema = system_configuration.get('EMA')
        edit_my_acca_status = ema.get('enabled')
        self.assertTrue(edit_my_acca_status, msg='"Edit My Acca" not enabled in CMS')

        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)

            outcomes = next(((market['market']['children']) for market in events[0]['event']['children']), None)
            outcomes2 = next(((market['market']['children']) for market in events[1]['event']['children']), None)
            outcomes3 = next(((market['market']['children']) for market in events[2]['event']['children']), None)
            outcomes4 = next(((market['market']['children']) for market in events[3]['event']['children']), None)

            event_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            event2_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes2}
            event3_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes3}
            event4_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes4}
            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            team2 = next((outcome['outcome']['name'] for outcome in outcomes2 if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            team3 = next((outcome['outcome']['name'] for outcome in outcomes3 if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            team4 = next((outcome['outcome']['name'] for outcome in outcomes4 if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            self.selection_ids = [event_selection_ids[team1], event2_selection_ids[team2],
                                  event3_selection_ids[team3], event4_selection_ids[team4]]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            event2 = self.ob_config.add_autotest_premier_league_football_event()
            event3 = self.ob_config.add_autotest_premier_league_football_event()
            event4 = self.ob_config.add_autotest_premier_league_football_event()
            self.selection_ids = [event.selection_ids[event.team1], event2.selection_ids[event2.team1],
                                  event3.selection_ids[event3.team1], event4.selection_ids[event4.team1]]

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state(state_name='HomePage')
        self.site.open_my_bets_open_bets()

    def test_001_when_the_user_views_his_edited_acca_in_my_bets_and_he_has_more_than_1_open_selections_which_are_active_and_have_cash_out_option_available_then_the_cash_out_button_must_be_displayed_with_cash_out_value_on_the_button(self):
        """
        DESCRIPTION: When the user views his edited Acca in My Bets and he has more than 1 open selections which are active and have cash out option available then the cash out button must be displayed with Cash out value on the button
        EXPECTED: We should only see a cash out button
        """
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        for bet_name, bet in list(bets.items())[:1]:
            self.assertTrue(bet.has_edit_my_acca_button(),
                            msg='"Edit my acca button" is not displayed')
            self.assertTrue(bet.buttons_panel.full_cashout_button.is_displayed(),
                            msg='"Full cashout button" is not displayed')
            self.assertTrue(bet.buttons_panel.full_cashout_button.amount.is_displayed(),
                            msg='"Amount value" is not displayed')
            bet.edit_my_acca_button.click()

            bet_legs = bet.items_as_ordered_dict
            for bet_leg_name, bet_leg in list(bet_legs.items())[1:]:
                bet_leg.edit_my_acca_remove_icon.click()
                self.assertTrue(wait_for_result(lambda: bet_leg.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                                msg='"Undo Button" not displayed')
            bet.confirm_button.click()
            self.site.wait_splash_to_hide(3)

    def test_002_verify_edit_my_bet_button_is_no_longer_displayed_for_the_user_when_only_one_selection_remains_open(self):
        """
        DESCRIPTION: Verify Edit My Bet button is no longer displayed for the user when only one selection remains open
        EXPECTED: The Edit My Bet button should not be available
        """
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        for bet_name, bet in list(bets.items())[:1]:
            self.assertFalse(bet.has_edit_my_acca_button(expected_result=False),
                             msg='"Edit my acca button" is displayed')
