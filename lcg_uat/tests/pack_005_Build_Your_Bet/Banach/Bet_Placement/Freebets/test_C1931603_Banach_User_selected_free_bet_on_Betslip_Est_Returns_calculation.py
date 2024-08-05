import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.banach
@pytest.mark.build_your_bet
@pytest.mark.betslip
@pytest.mark.freebets
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-35202')
@pytest.mark.login
@vtest
class Test_C1931603_Banach_User_selected_free_bet_on_Betslip_Est_Returns_calculation(BaseBanachTest, BaseBetSlipTest):
    """
    TR_ID: C1931603
    NAME: Banach. User selected free bet on Betslip - Est. Returns calculation
    DESCRIPTION: Test case verifies successful Banach bet placement using freebets only
    PRECONDITIONS: Banach free bets tokens - a standard offer with default sportsbook token reward should be configured and active, with all channels ticked- it will include new Banach OB channels
    PRECONDITIONS: [To add freebet to user account][1]
    PRECONDITIONS: [1]:https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To retrieve Banach Odds value check Network tab : price request
    PRECONDITIONS: **User has Banach free bets**
    PRECONDITIONS: **Banach selections are added to the dashboard**
    """
    keep_browser_open = True
    proxy = None
    odds = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Login and navigate to EDP using derived event_id
        """
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        self.site.login(username=tests.settings.freebet_user)
        self.navigate_to_edp(event_id=self.eventID)
        byb_tab = self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet,
                                                                           timeout=5)
        self.assertTrue(byb_tab, msg=f'{self.expected_market_tabs.build_your_bet} tab is not active')
        self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.match_betting,
                                            selection_index=1)
        self.__class__.initial_counter += 1
        self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.both_teams_to_score,
                                            selection_index=1)

    def test_001_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on "Place bet" button
        EXPECTED: - Betslip with price field and freebets dropdown appears
        """
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.click()

        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='Build Your Bet Betslip panel not shown')
        self.assertTrue(self.site.byb_betslip_panel.selection.content.has_use_free_bet_link(), msg='Use Free Bet link is not shown')

        self.__class__.odds = self.site.byb_betslip_panel.selection.content.odds
        self.assertTrue(self.odds, msg='Odds/price are not shown')

    def test_002_select_freebet_from_the_dropdown(self):
        """
        DESCRIPTION: Select freebet from the dropdown
        EXPECTED: Stake and Est.Returned are populated with the values
        EXPECTED: - Stake - amount of freebet
        EXPECTED: - Est.Returns - calculated based on Odds value: (odds + 1)*freebet - freebet
        """
        byb_betslip_panel = self.site.byb_betslip_panel
        self.site.byb_betslip_panel.selection.content.use_free_bet_link.click()

        freebet_stake = float(self.select_free_bet())

        wait_for_result(lambda: byb_betslip_panel.selection.bet_summary.total_stake != '0.00',
                        name='Total Stake value to appear',
                        timeout=10)
        actual_stake = '%0.2f' % float(byb_betslip_panel.selection.bet_summary.free_bet_stake)
        expected_stake = '%0.2f' % float(freebet_stake)
        self.assertEqual(actual_stake, expected_stake, msg=f'Stake "{actual_stake}" is not equal to previously '
                                                           f'selected Free bet value "{expected_stake}"')

        actual_est_returns = self.site.byb_betslip_panel.selection.bet_summary.total_estimate_returns
        expected_est_returns = \
            '%0.2f' % float(round((eval(self.odds) + 1) * float(freebet_stake) - float(freebet_stake), 2))
        self.assertEqual(actual_est_returns, expected_est_returns,
                         msg=f'Total Est. Returns amount value "{actual_est_returns}" is '
                             f'not the same as expected "{expected_est_returns}"')
