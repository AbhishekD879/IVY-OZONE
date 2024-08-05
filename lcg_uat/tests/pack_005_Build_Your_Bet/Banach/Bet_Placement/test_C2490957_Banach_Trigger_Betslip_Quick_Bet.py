import re
import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.critical
@pytest.mark.banach
@pytest.mark.build_your_bet
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.reg156_fix
@vtest
class Test_C2490957_Banach_Trigger_Betslip_Quick_Bet(BaseBanachTest, BaseBetSlipTest):
    """
    TR_ID: C2490957
    NAME: Banach. Trigger Betslip (Quick Bet)
    DESCRIPTION: Test case verifies Betslip (Quick Bet) triggering and info, buttons and Est.Returns calculation
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To retrieve odds value check Network tab: "price" request
    PRECONDITIONS: **Banach selections are added to the dashboard**
    """
    keep_browser_open = True
    proxy = None
    expected_dashboard_all_markets_and_selections = []
    byb_betslip_panel = None
    odds = None
    expected_amount_value = '0.00'
    stake_value = '5.00'
    blocked_hosts = ['*spark-br.*']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Login and navigate to EDP using derived event_id
        """
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        username = tests.settings.freebet_user if tests.settings.backend_env != 'prod' \
            else tests.settings.betplacement_user
        if tests.settings.backend_env != 'prod':
            self.ob_config.grant_freebet(username=username)
        self.site.login(username=username)
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='EventDetails')
        byb_tab = self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(byb_tab, msg=f'{self.expected_market_tabs.build_your_bet} tab is not active')

        # Match betting 90 mins selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        match_betting_selection_name = match_betting.set_market_selection(selection_index=1)[0]
        match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_name, msg='No selections added to Dashboard')
        match_betting_default_switcher = match_betting.time_period_outcomes_list.current
        self.assertTrue(match_betting_selection_name, msg='Match betting selection is not added to Dashboard')
        if "Minutes" in match_betting_default_switcher:
            match_betting_default_switcher = match_betting_default_switcher.replace("Minutes", "mins")
        match_betting_market_and_selection_name = f'{match_betting_selection_name} ' \
                                                  f'{self.expected_market_sections.match_betting.title()} ' \
                                                  f'{match_betting_default_switcher}'

        self.__class__.expected_dashboard_all_markets_and_selections.append(match_betting_market_and_selection_name)
        match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1

        # Double chance selection
        # ToDo: sometimes fails on the following assert because of VOL-3453
        double_chance_market = self.get_market(self.expected_market_sections.double_chance)

        grouping_buttons = double_chance_market.grouping_buttons
        grouping_buttons.scroll_to()
        double_chance_default_switcher = grouping_buttons.current
        self.assertTrue(double_chance_default_switcher, msg='Double chance selection switcher is empty')
        double_chance_market.scroll_to()
        double_chance_selection_name = double_chance_market.set_market_selection(selection_index=1)[0]
        self.assertTrue(double_chance_selection_name, msg='No selections added to Dashboard')
        double_chance_market_and_selection_name = f'{double_chance_selection_name} ' \
                                                  f'{self.expected_market_sections.double_chance.title()} ' \
                                                  f'{double_chance_default_switcher.lower()}'
        self.__class__.expected_dashboard_all_markets_and_selections.append(double_chance_market_and_selection_name)
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1

    def test_001_tap_on_the_place_bet_button_with_odds(self):
        """
        DESCRIPTION: Tap on the Place bet button with odds
        EXPECTED: -  Betslip appears
        """
        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.click()

        self.assertTrue(self.site.wait_for_byb_betslip_panel(timeout=10), msg='Build Your Bet Betslip not appears')
        self.__class__.byb_betslip_panel = self.site.byb_betslip_panel
        self.assertTrue(self.byb_betslip_panel.is_displayed(), msg='Betslip is not shown')

    def test_002_verify_betslip_quick_bet_info_and_buttons(self):
        """
        DESCRIPTION: Verify Betslip (Quick Bet) info and buttons
        EXPECTED: - Title BETSLIP
        EXPECTED: - Selections names are the same as they were on dashboard in the next format: - Market Name SELECTION NAME
        EXPECTED: - Odds field
        EXPECTED: - Stake box
        EXPECTED: - "Use Free Bet" link is displayed under event name (if free bets are available for user)
        EXPECTED: - Quick stakes
        EXPECTED: - Stake and Est. Returns have value 0.00
        EXPECTED: - Back button
        EXPECTED: - Disabled Place bet button
        """
        title = self.byb_betslip_panel.header.title
        self.assertEqual(
            title, vec.yourcall.YOUR_CALL_BETSLIP_TITLE,
            msg=f'Header title "{title}" is not the same as expected "{vec.yourcall.YOUR_CALL_BETSLIP_TITLE}"')

        selection_names = list(self.byb_betslip_panel.selection.content.outcomes_section.items_as_ordered_dict.keys())
        self.assertListEqual(selection_names, self.expected_dashboard_all_markets_and_selections,
                             msg=f'Selection names: \n"{selection_names}" \nare not the same as they were on dashboard:'
                                 f' \n"{self.expected_dashboard_all_markets_and_selections}"')

        self.__class__.odds = self.byb_betslip_panel.selection.content.odds
        self.assertTrue(self.odds, msg='Odds/price are not shown')

        stake_box = self.byb_betslip_panel.selection.content.amount_form
        self.assertTrue(stake_box.is_displayed(), msg='Stake box is not shown')

        if tests.settings.backend_env != 'prod' and self.brand != 'ladbrokes':
            self.assertTrue(self.byb_betslip_panel.selection.content.has_use_free_bet_link(),
                            msg='"Use Free Bet" link is not present')

        self.assertTrue(self.byb_betslip_panel.quick_stake_panel.is_displayed(), msg='Quick stakes are not shown')

        stake = self.byb_betslip_panel.selection.bet_summary.total_stake
        self.assertEqual(stake, self.expected_amount_value,
                         msg=f'Stake amount value "{stake}" is not the same as expected "{self.expected_amount_value}"')

        est_returns = self.byb_betslip_panel.selection.bet_summary.total_estimate_returns
        self.assertEqual(
            est_returns, self.expected_amount_value,
            msg=f'Est. Returns amount value "{est_returns}" is not the same as expected "{self.expected_amount_value}"')

        self.assertTrue(self.byb_betslip_panel.back_button.is_displayed(), msg='Back button is not shown')

        place_bet_button = self.byb_betslip_panel.place_bet
        self.assertFalse(place_bet_button.is_enabled(expected_result=False), msg='Place bet button is not disabled')

    def test_003_enter_value_in_a_stake_box(self):
        """
        DESCRIPTION: Enter value in a Stake box
        EXPECTED: - Stake and Est.Returned are populated with the values
        EXPECTED: Stake - amount entered by user
        EXPECTED: Est.Returns - calculated based on Odds value: (odds + 1)*stake
        EXPECTED: - PLACE BET button is enabled
        """
        self.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.stake_value)

        is_amount_changed = wait_for_result(lambda: self.byb_betslip_panel.selection.bet_summary.total_stake != '0.00',
                                            name='Stake amount to change',
                                            timeout=2)
        self.assertTrue(is_amount_changed, msg='Stake amount is not populated with test value')
        stake = self.byb_betslip_panel.selection.bet_summary.total_stake
        self.assertEqual(stake, self.stake_value,
                         msg=f'Stake amount value {stake} is not the same as entered {self.stake_value}')

        est_returns = self.byb_betslip_panel.selection.bet_summary.total_estimate_returns
        if re.match(r'^\d+\.\d', self.odds):
            calculated_est_returns = round((eval(self.odds)) * float(self.stake_value), 2)
        else:
            calculated_est_returns = round((eval(self.odds) + 1) * float(self.stake_value), 2)
        self.assertAlmostEqual(float(est_returns), calculated_est_returns, delta=0.026,
                               msg=f'Est. Returns amount value {float(est_returns)} '
                                   f'is not the same as calculated {calculated_est_returns} '
                                   f'within 0.026 delta')

        self.assertTrue(self.byb_betslip_panel.place_bet.is_enabled(), msg='Place bet button is not enabled')
