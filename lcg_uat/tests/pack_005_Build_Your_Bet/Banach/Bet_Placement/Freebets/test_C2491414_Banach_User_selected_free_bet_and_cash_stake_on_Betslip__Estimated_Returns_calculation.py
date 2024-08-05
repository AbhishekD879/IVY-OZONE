import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from time import sleep


# @pytest.mark.tst2 # cannot get banach events in qa environments
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.build_your_bet
@pytest.mark.reg157_fix
@pytest.mark.desktop
@vtest
class Test_C2491414_Banach_User_selected_free_bet_and_cash_stake_on_Betslip__Estimated_Returns_calculation(BaseBanachTest, BaseBetSlipTest):
    """
    TR_ID: C2491414
    NAME: Banach. User selected free bet and cash stake on Betslip - Estimated Returns calculation
    DESCRIPTION: Test case verifies Estimated Returns calculation on Banach Betslip when user combines free bet and and cash stake
    PRECONDITIONS: Banach free bets tokens - a standard offer with default sportsbook token reward should be configured and active, with all channels ticked- it will include new Banach OB channels. Ahhoc tokens with default offer ID will not work for Banach bets. Only adhoc tokens created with associated Banach offer as mentioned above.
    PRECONDITIONS: [To add freebet to user account][1]
    PRECONDITIONS: [1]:https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **User has Banach free bets**
    PRECONDITIONS: **User has added Banach selections to dashboard**
    """
    keep_browser_open = True
    proxy = None
    bet_amount = 0.5

    def handle_player_cannot_be_selected_popup(self):
        sleep(6)
        try:
            self.assertFalse(self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_PLAYER_NOT_SELECTED, timeout=5))
        except VoltronException:
            # Handling <Player cannot Be Selected> dialog
            playerbet_dailog = self.site.wait_for_dialog(
                vec.dialogs.DIALOG_MANAGER_PLAYER_NOT_SELECTED, timeout=5)
            playerbet_dailog.ok_thanks_btn.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as user that has freebets
        DESCRIPTION: Find event with Banach markets
        DESCRIPTION: Add two combinable selections to BYB Dashboard
        """
        self.__class__.event_id = self.get_ob_event_with_byb_market()
        username = tests.settings.freebet_user
        self.site.login(username=username)
        self.__class__.user_balance = self.site.header.user_balance
        self.navigate_to_edp(event_id=self.event_id, timeout=50)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.handle_player_cannot_be_selected_popup()
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        match_betting_selection_name = match_betting.set_market_selection(selection_index=1)[0]
        match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_name, msg='No selections added to Dashboard')
        sleep(3)
        match_betting.add_to_betslip_button.click()
        double_chance_market = self.get_market(self.expected_market_sections.double_chance)
        grouping_buttons = double_chance_market.grouping_buttons
        grouping_buttons.scroll_to()
        double_chance_default_switcher = grouping_buttons.current
        self.assertTrue(double_chance_default_switcher, msg='Double chance selection switcher is empty')
        double_chance_market.scroll_to()
        double_chance_selection_name = double_chance_market.set_market_selection(selection_index=1)[0]
        self.assertTrue(double_chance_selection_name, msg='No selections added to Dashboard')

    def test_001_tap_on_odds_area(self):
        """
        DESCRIPTION: Tap on odds area
        EXPECTED: - Betslip with price field, numeric keyboard and freebets dropdown appears
        """
        summary_block = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary
        summary_block.place_bet.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                        msg='BYB Dashboard panel is displayed')
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip is not shown')
        self.assertTrue(self.site.byb_betslip_panel.quick_stake_panel.has_use_free_bet_link(),
                        msg='Use Free Bet link is not shown')
        self.__class__.odds = self.site.byb_betslip_panel.selection.content.odds
        self.assertTrue(self.odds, msg='Odds/price are not shown')

    def test_002_select_free_bet_from_dropdown(self):
        """
        DESCRIPTION: Select Free bet from dropdown
        EXPECTED: Total Stake and Estimated Returned are populated with the values
        EXPECTED: - Total Stake - amount of freebet
        EXPECTED: - Estimated Returns - calculated based on Odds value:
        EXPECTED: (odds + 1)*freebet - freebet
        """
        byb_betslip_panel = self.site.byb_betslip_panel
        byb_betslip_panel.quick_stake_panel.free_bet.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5,
                                           verify_name=False)
        self.__class__.freebet_amount = dialog.freebet_amount[1:].split(' ')[0].strip('-')
        dialog.select_first_free_bet()
        actual_stake = byb_betslip_panel.selection.bet_summary.free_bet_stake.split('FREE BET')[0].strip()
        expected_stake = self.freebet_amount
        self.assertEqual(expected_stake, actual_stake, msg=f'Stake "{actual_stake}" is not equal to previously '
                                                           f'selected Free bet value "{expected_stake}"')

        actual_est_returns = self.site.byb_betslip_panel.selection.bet_summary.total_estimate_returns
        expected_est_returns = \
            '%0.2f' % float(round((eval(self.odds) + 1) * float(self.freebet_amount) - float(self.freebet_amount), 2))
        self.assertEqual(actual_est_returns, expected_est_returns,
                         msg=f'Total Est. Returns amount value "{actual_est_returns}" is '
                             f'not the same as expected "{expected_est_returns}"')

    def test_003_enter_cash_stake_in_a_stake_box(self):
        """
        DESCRIPTION: Enter cash stake in a Stake box
        EXPECTED: total Stake and Estimated Returned values are updated
        EXPECTED: - Total Stake: cash stake + freebet (further Total Stake)
        EXPECTED: - Estimated Returns: (odds +1)*Total Stake - freebet
        """
        byb_betslip_panel = self.site.byb_betslip_panel.selection.content
        byb_betslip_panel.amount_form.enter_amount(value=self.bet_amount)
        expected_total_stake = '%0.2f' % (float(self.site.byb_betslip_panel.selection.bet_summary.free_bet_stake.split('FREE BET')[0].strip()) + self.bet_amount)
        combined_stake = self.site.byb_betslip_panel.selection.bet_summary.combined_total_stake
        total_stake = combined_stake.split(" + ")
        actual_total_stake = '%0.2f' % (float(total_stake[0].split('FREE BET')[0].strip().strip("£")) + float(total_stake[1].strip("£")))
        self.assertEqual(actual_total_stake, expected_total_stake,
                         msg=f'Actual stake "{actual_total_stake}" Expected Stake "{expected_total_stake}"')
        actual_est_returns = self.site.byb_betslip_panel.selection.bet_summary.total_estimate_returns
        expected_est_returns = \
            '%0.2f' % float(round((eval(self.odds) + 1) * float(actual_total_stake) - float(self.freebet_amount), 2))
        self.assertEqual(actual_est_returns, expected_est_returns,
                         msg=f'Total Est. Returns amount value "{actual_est_returns}" is '
                             f'not the same as expected "{expected_est_returns}"')
