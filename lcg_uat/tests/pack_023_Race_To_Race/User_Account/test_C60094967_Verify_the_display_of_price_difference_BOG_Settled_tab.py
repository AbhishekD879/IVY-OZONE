import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from decimal import Decimal
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod : # Events with specific markets cannot created in Prod/Beta
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C60094967_Verify_the_display_of_price_difference_BOG_Settled_tab(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C60094967
    NAME: Verify the display of price difference BOG -Settled tab
    DESCRIPTION: This test case verify BOG text and price difference in Settled bet tab when the events have BOG signpost and BOG flag is ON in CMS
    PRECONDITIONS: 1. BOG has been enabled in CMS(Sysytem config)
    PRECONDITIONS: 2. BOG Signposting, Pop-up configured with Header, Pop-up text and Link in CMS (CMS > Promotions > Promotions)
    PRECONDITIONS: 3. Events with market configured to show BOG flag available (Market should have 'GP Available' 'SP Available' and 'LP Available' checkmarks)
    """
    keep_browser_open = True
    prices = {0: '1/2', 1: '1/3', 2: '2/3', 3: '2/7', 4: '1/9'}

    def test_000_pre_conditions(self):
        bog_toggle_status = self.cms_config.get_initial_data(device_type=self.device_type)['systemConfiguration']['BogToggle']['bogToggle']
        if not bog_toggle_status:
            self.cms_config.update_system_configuration_structure(config_item='BogToggle', field_name='bogToggle',
                                                                  field_value=True)
            bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']
            self.assertTrue(bog_toggle, msg='"Bog toggle" is not enabled in CMS')
        event = self.ob_config.add_UK_racing_event(gp=True, lp_prices=self.prices)
        self.__class__.event_id = event.event_id
        self.__class__.market_id = event.market_id
        self.__class__.created_event_name = event[6]['event']['name']
        self.__class__.selection_id = list(event.selection_ids.values())[0]

    def test_001_launch_ladbrokescoral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: Ladbrokes/Coral URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.site.home.menu_carousel.items_as_ordered_dict.get(
                vec.sb.HORSERACING.upper() if self.brand == 'bma' else vec.sb.HORSERACING.title()).click()
        self.site.wait_content_state_changed(timeout=10)
        self.site.wait_content_state('Horseracing')

    def test_003_click_on_any_horse_race_event_which_has_bog_signpost(self):
        """
        DESCRIPTION: Click on any Horse race event which has BOG signpost
        EXPECTED: It should be displayed below on Horses in HR EDP
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')

    def test_004_add_a_hr_selectionselections_to_bet_slip(self):
        """
        DESCRIPTION: Add a HR selection/selections to bet slip
        EXPECTED: The selection/selections is added to bet slip
        """
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_005_enter_the_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Enter the Stake and click on Place bet button
        EXPECTED: User should be able to place the bet successfully
        EXPECTED: Bet receipt should be generated
        """
        self.place_and_validate_single_bet()
        self.site.is_bet_receipt_displayed(expected_result=True)
        self.ob_config.update_selection_result(event_id=self.event_id, selection_id=self.selection_id,
                                               market_id=self.market_id,
                                               price='10/1')
        self.site.bet_receipt.footer.click_done()

    def test_006_navigate_to_settled_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page
        EXPECTED: Bet History' page/tab is opened
        """
        # Step 6 is covered at Step 7 inside while loop

    def test_007_verify_the_bog_text_and_price_differencesindexphpattachmentsget121534956(self):
        """
        DESCRIPTION: Verify the BOG text and Price differences
        DESCRIPTION: ![](index.php?/attachments/get/121534956)
        EXPECTED: * BOG Best Odds Guaranteed should be displayed below Event time & Name
        EXPECTED: * You won £xx.xx extra with BOG offer should be displayed below the Stake and Returns
        EXPECTED: £xx.xx- Price difference
        EXPECTED: * Bet Receipt should be displayed below and Time & Date on right side
        """
        bet_found = False
        settle_bet = None
        while not bet_found:
            try:
                self.device.refresh_page()
                self.site.wait_content_state_changed(timeout=20)
                self.site.open_my_bets_settled_bets()
                self.assertTrue(self.site.bet_history.is_displayed(),
                                msg=f'"{vec.bma.MY_ACC_BETHISTORY}" is not displayed')
                bet_name, settle_bet = self.site.bet_history.tab_content.accordions_list.get_bet(
                    bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name,
                    number_of_bets=1)
                bet_found = True
            except VoltronException:
                self._logger.info(msg='Bet not found')
                bet_found = False
        self.assertTrue(settle_bet.bog_icon, msg='Bog icon is not displayed in bet history')
        if self.brand == 'bma':
            self.assertEqual(settle_bet.bog_icon_txt.upper(), vec.Dialogs.DIALOG_MANAGER_BEST_ODDS_GUARANTEED,
                             msg='Best Odds Guaranteed text is not appearing in UI ')
        else:
            self.assertEqual(settle_bet.bog_icon_txt, vec.Dialogs.DIALOG_MANAGER_BEST_ODDS_GUARANTEED,
                             msg='Best Odds Guaranteed text is not appearing in UI ')
        self.assertTrue(settle_bet.bet_receipt_info.bet_id, msg='Bet recepit is not appearing in UI')

        ui_extra_bog = settle_bet.extra_bog
        you_won = Decimal(settle_bet.cashed_out_value.name.replace('£', '').strip())
        est_return_1 = Decimal(settle_bet.est_returns.name.replace('|Returns:£', '').strip())

        if self.brand == 'bma':
            bog_text = 'You have won an extra £' + str(Decimal(you_won - est_return_1)) + ' with BOG'
        else:
            bog_text = 'You have won an extra  £' + str(Decimal(you_won - est_return_1)) + '  with BOG'
        self.assertEqual(ui_extra_bog.replace(" ", ""), bog_text.replace(" ", ""),
                         msg='Extra earn bog value is incorrect')
