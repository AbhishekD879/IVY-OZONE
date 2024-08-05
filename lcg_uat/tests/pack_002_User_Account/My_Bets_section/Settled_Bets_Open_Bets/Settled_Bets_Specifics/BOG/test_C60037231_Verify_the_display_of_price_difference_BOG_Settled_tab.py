import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create/settle events in beta/prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.desktop
@vtest
class Test_C60037231_Verify_the_display_of_price_difference_BOG_Settled_tab(BaseBetSlipTest):
    """
    TR_ID: C60037231
    NAME: Verify the display of price difference BOG -Settled tab
    DESCRIPTION: This test case verify BOG text and price difference in Settled bet tab when the events have BOG signpost and BOG flag is ON in CMS
    PRECONDITIONS: 1. BOG has been enabled in CMS(Sysytem config)
    PRECONDITIONS: 2. BOG Signposting, Pop-up configured with Header, Pop-up text and Link in CMS (CMS > Promotions > Promotions)
    PRECONDITIONS: 3. Events with market configured to show BOG flag available (Market should have 'GP Available' 'SP Available' and 'LP Available' checkmarks)
    """
    keep_browser_open = True
    prices = {0: '1/3', 1: '1/3', 2: '2/3', 3: '2/7', 4: '1/9'}

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: BOG has been enabled in CMS(Sysytem config)
        DESCRIPTION: BOG flag disabled in OB event level 'GP available' should be checked
        """
        bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']

        if not bog_toggle:
            self.cms_config.update_system_configuration_structure(config_item='BogToggle', field_name='bogToggle',
                                                                  field_value=True)
            bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']
        self.assertTrue(bog_toggle, msg='"Bog toggle" is not enabled in CMS')

        event = self.ob_config.add_UK_racing_event(gp=True, lp_prices=self.prices)
        self.__class__.event_id = event.event_id
        self.__class__.market_id = event.market_id
        self.__class__.created_event_name = event.ss_response['event']['name']
        self.__class__.selection_id = list(event.selection_ids.values())[0]

    def test_001_launch_ladbrokescoral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: Ladbrokes/Coral URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.login()

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        # covered in step_003

    def test_003_click_on_any_horse_race_event_which_has_bog_signpost(self):
        """
        DESCRIPTION: Click on any Horse race event which has BOG signpost
        EXPECTED: It should be displayed below on Horses in HR EDP
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

    def test_004_add_a_hr_selectionselections_to_bet_slip(self):
        """
        DESCRIPTION: Add a HR selection/selections to bet slip
        EXPECTED: The selection/selections is added to bet slip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_005_enter_the_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Enter the Stake and click on Place bet button
        EXPECTED: User should be able to place the bet successfully
        EXPECTED: Bet receipt should be generated
        """
        self.place_single_bet()

        # Settling the bet
        self.ob_config.update_selection_result(event_id=self.event_id, selection_id=self.selection_id,
                                               market_id=self.market_id,
                                               price='10/1')
        self.site.is_bet_receipt_displayed(expected_result=True)
        self.site.bet_receipt.footer.click_done()

    def test_006_navigate_to_settled_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page
        EXPECTED: Bet History' page/tab is opened
        """
        self.site.wait_content_state_changed(timeout=15)
        self.site.open_my_bets_settled_bets()
        wait_for_result(lambda: self.site.bet_history.tab_content.accordions_list.is_displayed(timeout=10) is True, timeout=60)
        self.assertTrue(self.site.bet_history.is_displayed(), msg=f'"{vec.bma.MY_ACC_BETHISTORY}" is not displayed')

    def test_007_verify_the_bog_text_and_price_differencesindexphpattachmentsget131712243(self):
        """
        DESCRIPTION: Verify the BOG text and Price differences
        DESCRIPTION: ![](index.php?/attachments/get/131712243)
        EXPECTED: * BOG Best Odds Guaranteed should be displayed above Event time & Name
        EXPECTED: * You won £xx.xx extra with BOG offer should be displayed above the Stake and Returns
        EXPECTED: £xx.xx- Price difference
        EXPECTED: * Bet Receipt should be displayed below and Time & Date on right side.
        EXPECTED: Note: The potential returns includes the extra winnings total.
        """
        bet_name, settle_bet = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name, number_of_bets=1)
        self.assertTrue(settle_bet.bog_icon, msg='Bog icon is not displayed in bet history')
        self.assertEqual(settle_bet.bog_icon_txt, vec.Dialogs.DIALOG_MANAGER_BEST_ODDS_GUARANTEED.title(),
                         msg=f'Actual BOG text "{settle_bet.bog_icon_txt}" is not same as'
                             f'Expected BOG text "{vec.Dialogs.DIALOG_MANAGER_BEST_ODDS_GUARANTEED.title()}"')
        self.assertTrue(settle_bet.bet_receipt_info.bet_id, msg='Bet recepit is not appearing in UI')

        ui_extra_bog = settle_bet.extra_bog
        old_returns = self.calculate_estimated_returns(odds=[self.prices[0]], bet_amount=self.bet_amount)
        est_return_1 = float(settle_bet.est_returns.name.replace('|Returns:£', ''))
        bog_text = 'You won an extra £' + str(round(est_return_1 - old_returns, ndigits=2))
        self.assertEqual(ui_extra_bog, bog_text,
                         msg=f'Actual Extra earn bog value "{ui_extra_bog}" is '
                             f'different from Expected value "{bog_text}"')
