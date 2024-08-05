import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events cannot be created on prod & beta
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@vtest
class Test_C59486933_Verify_the_BOG_signposting_is_displayed_in_Horse_Racing_Settled_bets_as_per_the_designs_mentioned(BaseCashOutTest):
    """
    TR_ID: C59486933
    NAME: Verify the BOG signposting is displayed in Horse Racing "Settled bets" as per the designs mentioned
    DESCRIPTION: This test case Verify BOG text and price difference is displayed in Settled bet tab when the BOG toggle is ON in CMS
    PRECONDITIONS: 1. BOG has been enabled in CMS(Sysytem config)
    PRECONDITIONS: 2. BOG Signposting, Pop-up configured with Header, Pop-up text and Link in CMS (CMS > Promotions > Promotions)
    PRECONDITIONS: 3. Events with market configured to show BOG flag available (Market should have 'GP Available' 'SP Available' and 'LP Available' checkmarks)
    """
    keep_browser_open = True
    prices = {0: '1/2', 1: '1/3', 2: '2/3', 3: '2/7', 4: '1/9'}

    def test_000_pre_conditions(self):

        bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']

        if not bog_toggle:
            self.cms_config.update_system_configuration_structure(config_item='BogToggle', field_name='bogToggle',
                                                                  field_value=True)
            bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']
        self.assertTrue(bog_toggle, msg='"Bog toggle" is not enabled in CMS')

        event = self.ob_config.add_UK_racing_event(cashout=True, gp=True, lp_prices=self.prices)
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
        self.assertTrue(self.site.wait_content_state('homepage'), msg='User has not re-directed to homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        self.site.wait_content_state('HomePage')
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.site.home.menu_carousel.items_as_ordered_dict.get(
                vec.sb.HORSERACING.upper() if self.brand == 'bma' else vec.sb.HORSERACING.title()).click()

        self.site.wait_content_state_changed(timeout=10)
        self.site.wait_content_state('Horseracing')

    def test_003_click_on_any_horse_race_event_from_which_have_bog_signpost(self):
        """
        DESCRIPTION: Click on any Horse race event from which have BOG signpost
        EXPECTED: It should be displayed below on Horses in HR EDP
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')

    def test_004_add_a_hr_selectionselections_to_bet_slip(self):
        """
        DESCRIPTION: Add a HR selection/selections to bet slip
        EXPECTED: The selection/selections is added to bet slip
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_005_enter_the_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Enter the Stake and click on Place bet button
        EXPECTED: User should be able to place the bet successfully
        EXPECTED: Bet receipt should be generated
        """
        self.place_and_validate_single_bet()
        self.site.is_bet_receipt_displayed(expected_result=True)

        # Setteling the bet
        self.ob_config.update_selection_result(event_id=self.event_id, selection_id=self.selection_id,
                                               market_id=self.market_id,
                                               price='10/1')
        self.site.bet_receipt.footer.click_done()

    def test_006_navigate_to_settled_bets_tab_on_my_bets(self):
        """
        DESCRIPTION: Navigate to 'Settled bets' tab on My Bets
        EXPECTED: Settled Bets tab should be opened
        """
        self.site.open_my_bets_settled_bets()
        self.site.wait_content_state_changed(timeout=40)
        self.site.wait_splash_to_hide()
        wait_for_result(lambda: self.site.bet_history.tab_content.accordions_list.is_displayed(timeout=10) is True,
                        timeout=60)
        self.assertTrue(self.site.bet_history.is_displayed(), msg=f'"{vec.bma.MY_ACC_BETHISTORY}" is not displayed')

    def test_007_verify_the_bog_signposting(self):
        """
        DESCRIPTION: Verify the BOG signposting
        EXPECTED: BOG should be displayed as per the zeplin screen
        """
        bet_name, settle_bet = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name, number_of_bets=1)
        self.assertTrue(settle_bet.bog_icon, msg='Bog icon is not displayed in bet history')
