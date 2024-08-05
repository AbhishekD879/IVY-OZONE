import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
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
class Test_C60094970_Verify_CSS_of_BOG_text_in_settled_bet_tab(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C60094970
    NAME: Verify CSS of BOG text in settled bet tab
    DESCRIPTION: This test case Verify BOG text and price difference is not displayed in Settled bet tab when the BOG toggle is OFF in CMS
    PRECONDITIONS: 1. BOG has been enabled in CMS(Sysytem config)
    PRECONDITIONS: 2. BOG Signposting, Pop-up configured with Header, Pop-up text and Link in CMS (CMS > Promotions > Promotions)
    PRECONDITIONS: 3. Events with market configured to show BOG flag available (Market should have 'GP Available' 'SP Available' and 'LP Available' checkmarks)
    """
    keep_browser_open = True
    prices = {0: '1/2', 1: '2/3', 2: '1/3', 3: '1/4', 4: '1/6'}

    def verify_css_for_result(self, font_family, font_size, font_weight, color, result):

        actual_font_family = result.value_of_css_property('font-family')
        actual_font_size = result.value_of_css_property('font-size')
        actual_font_weight = result.value_of_css_property('font-weight')
        actual_color = self.rgba_to_hex(result.value_of_css_property('color'))

        self.assertIn(font_family, actual_font_family,
                      msg=f'Required font family :"{font_family}" is not in '
                          f'Actual font family: "{actual_font_family}".')
        self.assertEqual(font_size, actual_font_size,
                         msg=f'Actual font size :"{actual_font_size}" is not same as '
                             f'Expected font size: "{font_size}".')
        self.assertEqual(font_weight, actual_font_weight,
                         msg=f'Actual font weight :"{actual_font_weight}" is not same as '
                             f'Expected font weight: "{font_weight}".')
        self.assertEqual(color, actual_color,
                         msg=f'Actual font color :"{actual_color}" is not same as '
                             f'Expected font color: "{color}".')

    def test_000_preconditions(self):
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
        self.__class__.cms_horse_tab_name = self.get_sport_title(category_id=21)

    def test_001_launch_ladbrokescoral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: Ladbrokes/Coral URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('HomePage')
        self.device.refresh_page()

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
        self.site.wait_content_state_changed(timeout=20)
        self.site.wait_content_state('Horseracing')

    def test_003_click_on_any_horse_race_event_from_which_have_bog_signpost(self):
        """
        DESCRIPTION: Click on any Horse race event from which have BOG signpost
        EXPECTED: It should be displayed below on Horses in HR EDP
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

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
        # Step 6 is covered at step 7 inside while loop

    def test_007_verify_the_css_for_bog(self):
        """
        DESCRIPTION: Verify the CSS for BOG
        EXPECTED: ONLY LADBROKES
        EXPECTED: .Best-Odds-Guaranteed-Copy {
        EXPECTED: font-family: HelveticaNeue;
        EXPECTED: font-size: 10px;
        EXPECTED: font-weight: 400;
        EXPECTED: color: #777777;
        EXPECTED: }
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

        result = settle_bet.bog_label
        if self.brand == 'bma':
            self.verify_css_for_result(font_family='Helvetica Neue', font_size='10px', font_weight='700',
                                       color='#41494e', result=result)
        else:
            self.verify_css_for_result(font_family='Helvetica Neue', font_size='10px', font_weight='400',
                                       color='#777777', result=result)
