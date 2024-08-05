import pytest
import tests
import datetime
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870417_Verify_the_messages_displayed_for_user_in_Bet_Slip_and_My_Bets_section_when_Logged_Out_Logged_in(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C44870417
    NAME: Verify the messages displayed for user in Bet Slip and My Bets section when Logged Out/Logged in.
    DESCRIPTION: This TC is verify different messages shown in Bet Slip and My Bets section for logged in/out users.
    """
    keep_browser_open = True
    num_of_events = 3
    device_name = tests.desktop_default
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def place_bet(self):
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.num_of_events)

            outcomes = next(((market['market']['children']) for market in events[0]['event']['children']), None)
            outcomes2 = next(((market['market']['children']) for market in events[1]['event']['children']), None)
            outcomes3 = next(((market['market']['children']) for market in events[2]['event']['children']), None)

            event_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            event2_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes2}
            event3_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes3}
            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            team2 = next((outcome['outcome']['name'] for outcome in outcomes2 if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            team3 = next((outcome['outcome']['name'] for outcome in outcomes3 if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'))
            self.selection_ids = [event_selection_ids[team1], event2_selection_ids[team2],
                                  event3_selection_ids[team3]]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            event2 = self.ob_config.add_autotest_premier_league_football_event()
            event3 = self.ob_config.add_autotest_premier_league_football_event()
            self.selection_ids = [event.selection_ids[event.team1], event2.selection_ids[event2.team1],
                                  event3.selection_ids[event3.team1]]

        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.footer.click_done()

    def verify_bets_layout_with_edit_my_acca_button(self, bets):
        system_configuration = self.cms_config.get_system_configuration_structure()
        ema = system_configuration.get('EMA')
        edit_my_acca_status = ema.get('enabled')

        for bet_name, bet in list(bets.items())[:1]:
            self.assertTrue(bet.bet_type,
                            msg=f'For "{bet_name}" Bet Type is not displayed')
            self.assertTrue(bet.stake.is_displayed(),
                            msg=f'For "{bet_name}" Stake is not displayed')
            self.assertTrue(bet.est_returns.is_displayed(),
                            msg=f'For "{bet_name}" Estimated Returns is not displayed')
            self.assertTrue(bet.buttons_panel.full_cashout_button.is_displayed(),
                            msg=f'For "{bet_name}" Full cashout button is not displayed')
            if edit_my_acca_status:
                self.assertTrue(bet.edit_my_acca_button.is_displayed(),
                                msg=f'For "{bet_name}" Edit My Acca button is not displayed')

            bet_legs = bet.items_as_ordered_dict
            for bet_leg_name, bet_leg in bet_legs.items():
                self.assertTrue(bet_leg.outcome_name,
                                msg=f'For "{bet_leg_name}" Outcome is not displayed')
                self.assertTrue(bet_leg.market_name,
                                msg=f'For "{bet_leg_name}" Market name is not displayed')
                self.assertTrue(bet_leg.event_name,
                                msg=f'For "{bet_leg_name}" Event name is not displayed')
                self.assertTrue(bet_leg.odds_value,
                                msg=f'For "{bet_leg_name}" odds value is not displayed')
                self.assertTrue(bet_leg.event_time,
                                msg=f'For "{bet_leg_name}" Event time is not displayed')

    def test_001_logged_out_user____verify_user_sees_a_message_prompting_them_to_log_in_when_selected_any_of_the_tabs_within_my_bets_as_below__open_bets_tab_your_open_bets_will_appear_here_please_log_in_to_view__cash_out_your_cash_bets_will_appear_here_please_log_in_to_view__settled_bets_your_settled_bets_will_appear_here_please_log_in_to_view(self):
        """
        DESCRIPTION: "LOGGED OUT USER  - Verify user sees a message prompting them to log in when selected any of the tabs within My Bets as below
        DESCRIPTION: - Open Bets tab: 'Your open bets will appear here. Please log in to view.
        DESCRIPTION: - Cash Out: 'Your cash bets will appear here. Please log in to view.
        DESCRIPTION: - Settled Bets: Your settled bets will appear here. Please log in to view
        EXPECTED: User sees following messages:
        EXPECTED: - Open Bets tab: 'Your open bets will appear here. Please log in to view.
        EXPECTED: - Cash Out: 'Your cash out bets will appear here. Please log in to view.
        EXPECTED: - Settled Bets: Your settled bets will appear here. Please log in to view
        """
        self.site.open_my_bets_open_bets()
        self.__class__.open_bet = self.site.open_bets.tab_content
        open_bet_text = self.open_bet.please_login_text
        self.assertEqual(open_bet_text, vec.bet_history.OPEN_BETS_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual_text: "{open_bet_text}" is not equal as'
                             f'Expected_text: "{vec.bet_history.OPEN_BETS_PLEASE_LOGIN_MESSAGE}"')
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            self.__class__.cash_out_bet = self.site.cashout.tab_content
            cash_out_bet_text = self.cash_out_bet.please_login_text
            self.assertEqual(cash_out_bet_text, vec.bet_history.CASHOUT_PLEASE_LOGIN_MESSAGE,
                             msg=f'Actual_text: "{cash_out_bet_text}" is not equal as'
                                 f'Expected_text: "{vec.bet_history.CASHOUT_PLEASE_LOGIN_MESSAGE}"')

        self.site.open_my_bets_settled_bets()
        settled_bet_text = self.site.bet_history.tab_content.please_login_text
        self.assertEqual(settled_bet_text, vec.bet_history.SETTLED_BETS_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual_text: "{settled_bet_text}" is not equal as'
                             f'Expected_text: "{vec.bet_history.SETTLED_BETS_PLEASE_LOGIN_MESSAGE}"')

    def test_002_logged_in____verify_user_sees_their_bets_on_the_relevant_tabs_when_they__select_any_of_the_tabs_within_my_bets__cash_out_or_open_bets_tab_as_below_the_header_eg_double__clickable_text__eg_edit_my_acca_if_available_for_the_bet__bet_details__eg_liverpool_96_match_result_liverpool_v_crystal_palace_time__date__clickable_area_chevron_to_navigate_to_the_event_details__footer_with_the_stake_and_potential_returns__cash_out_button_cash_out_tab_only(self):
        """
        DESCRIPTION: LOGGED IN  - Verify user sees their bets on the relevant tabs when they  select any of the tabs within My Bets ( cash out or open bets tab) as below
        DESCRIPTION: -The Header: e.g. Double
        DESCRIPTION: - Clickable text : e.g Edit my ACCA (if available for the bet)
        DESCRIPTION: - Bet details : e.g Liverpool @9/6, Match result, Liverpool v Crystal palace, time & Date
        DESCRIPTION: - Clickable area (chevron) to navigate to the event details
        DESCRIPTION: - Footer with the stake and potential returns
        DESCRIPTION: - Cash out button (Cash Out tab only)
        EXPECTED: Logged In user sees following messages.
        EXPECTED: -The Header: e.g. Double
        EXPECTED: - Clickable text : e.g Edit my ACCA (if available for the bet)
        EXPECTED: - Bet details : e.g Liverpool @9/6, Match result, Liverpool v Crystal palace, time & Date
        EXPECTED: - Clickable area (chevron) to navigate to the event details
        EXPECTED: - Footer with the stake and potential returns
        EXPECTED: - Cash out button (Cash Out tab only)
        """
        user = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=user, amount=str(20),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year,
                                                                     cvv=tests.settings.master_card_cvv)
        self.site.login(user)

        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            no_cash_out_bet_text = self.cash_out_bet.accordions_list.no_bets_text
            self.assertEqual(no_cash_out_bet_text, vec.bet_history.NO_CASHOUT_BETS,
                             msg=f'Actual_text: "{no_cash_out_bet_text}" is not equal as'
                                 f'Expected_text: "{vec.bet_history.NO_CASHOUT_BETS}"')

        self.site.open_my_bets_open_bets()
        no_open_bet_text = self.open_bet.accordions_list.no_bets_text
        self.assertEqual(no_open_bet_text, vec.bet_history.NO_OPEN_BETS,
                         msg=f'Actual_text: "{no_open_bet_text}" is not equal as'
                             f'Expected_text: "{vec.bet_history.NO_OPEN_BETS}"')

        self.place_bet()
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            cash_out_bets = self.cash_out_bet.accordions_list.items_as_ordered_dict
            self.verify_bets_layout_with_edit_my_acca_button(cash_out_bets)

        self.site.open_my_bets_open_bets()
        open_bet = self.open_bet.accordions_list.items_as_ordered_dict
        self.verify_bets_layout_with_edit_my_acca_button(open_bet)

    def test_003_no_bets_messages____verify_user_sees_you_currently_have_no_opencash_out_bets_when_no_bets_are_available_on_the_cash_out_or_open_bets_tab(self):
        """
        DESCRIPTION: NO BETS MESSAGES  - Verify user sees ''You currently have no [open/cash-out] bets'' when no bets are available on the Cash out or open bets tab
        EXPECTED: Logged in user sees
        EXPECTED: 'You currently have no [open/cash-out] bets' - when no bets are available on the Cash out or open bets tab
        """
        # This step covered in step2

    def test_004_signposting_for_promotions___verify_user_has_bets_available_on_the_cash_out_open_bets_or_settled_bets_tab_and__promotions_are_available_for_any_of_the_bets_on_the_tab_ie_promo_flag_is_ticked_in_obthen_they_should_see_signposting_for_the_available_promotions_up_to_a_maximum_of_two_promos_(self):
        """
        DESCRIPTION: SIGNPOSTING FOR PROMOTIONS - Verify user has bets available on the cash-out, open bets, or settled bets tab and  promotions are available for any of the bets on the tab (i.e promo flag is ticked in OB)
        DESCRIPTION: THEN they should see signposting for the available promotions (up to a maximum of two promos )
        EXPECTED: User is able to see applicable promotion sign postings up to a maximum of two promos.
        """
        # OB Cannot be automated
        pass

    def test_005_sticky_widgetdesktop__verify_user_sees_all_the_content_on_my_betsbetslip_widget_when_they_scroll_up_or_down_thepage(self):
        """
        DESCRIPTION: STICKY WIDGET(Desktop) -Verify user sees all the content on My Bets/Betslip widget when they scroll up or down thepage
        EXPECTED: Its a Mobenga functionality and not applied to Roxanne yet.
        """
        # sticky widget not available for coral
        pass

    def test_006_server_unavailable_message___verify_user_sees_server_unavailable_message_when_service_for_the_site_is_interrupted_and_they_can_view_and_select_the_existing_reload_cta_button_to_refresh_the_page_as_normal(self):
        """
        DESCRIPTION: SERVER UNAVAILABLE MESSAGE - Verify user sees 'server unavailable' message when service for the site is interrupted and they can view and select the existing 'Reload' cta button to refresh the page as normal."
        EXPECTED: User sees 'server unavailable' message when service for the site is interrupted and they can view and select the existing 'Reload' cta button to refresh the page as normal."
        """
        # CMS cannot be automated
        pass
