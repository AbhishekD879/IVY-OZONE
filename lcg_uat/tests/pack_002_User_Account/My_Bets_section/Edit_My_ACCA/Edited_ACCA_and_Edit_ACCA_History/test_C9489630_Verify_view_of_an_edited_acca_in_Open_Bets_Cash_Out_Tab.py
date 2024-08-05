import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.portal_dependant
@vtest
class Test_C9489630_Verify_view_of_an_edited_acca_in_Open_Bets_Cash_Out_Tab(BaseCashOutTest):
    """
    TR_ID: C9489630
    NAME: Verify view of an edited acca in 'Open Bets'/'Cash Out' Tab
    DESCRIPTION: This test case view of an edited acca in 'Open Bets'/Cash Out Tab
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Acca' button is available
    PRECONDITIONS: Tap on 'Edit My Acca' button -> verify that user is in 'My Acca Edit' mode
    PRECONDITIONS: Remove selection from 'My Acca Edit' mode
    PRECONDITIONS: Tap 'Confirm' button -> user has successfully edited their acca
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True
    number_of_events = 2
    selection_ids = []
    event_names = []

    def get_bet_with_my_acca_edit(self, bet_type: str, event_names: str, open_bets=True):
        """
        Get bet with My ACCA edit functionality
        """
        if open_bets:
            _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=bet_type, event_names=event_names, number_of_bets=1)
        else:
            _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=bet_type, event_names=event_names, number_of_bets=1)
        self.assertTrue(bet, msg=f'Cannot find bet for "{event_names}"')
        return bet

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Enable My ACCA feature toggle in CMS
        PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
        PRECONDITIONS: Login into App
        PRECONDITIONS: Place Multiple bet
        PRECONDITIONS: Navigate to the Bet History from Right/User menu
        PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Acca' button is available
        PRECONDITIONS: Tap on 'Edit My Acca' button -> verify that user is in 'My Acca Edit' mode
        PRECONDITIONS: Remove selection from 'My Acca Edit' mode
        PRECONDITIONS: Tap 'Confirm' button -> user has successfully edited their acca
        PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
        """
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in CMS')
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            for event in events:
                event_name = normalize_name(event['event']['name'])
                self.event_names.append(event_name)
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = [i['outcome']['id'] for i in outcomes]
                selection_id = all_selection_ids[0]
                self.selection_ids.append(selection_id)
        else:
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)
            event_params = self.create_several_autotest_premier_league_football_events(
                number_of_events=self.number_of_events)
            for event in event_params:
                event_name = f'{event.team1} v {event.team2}'
                self.event_names.append(event_name)
            self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
        self.site.login()
        self.open_betslip_with_selections(self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        if self.device_type == 'mobile':
            self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_open_bets()
        bet = self.get_bet_with_my_acca_edit(open_bets=True, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event_names[0])
        self.__class__.stake = bet.stake.value
        self.__class__.actual_potential_returns = bet.est_returns.value
        self.__class__.bet_before_ema = bet.bet_type
        self.assertTrue(bet.has_edit_my_acca_button(), msg=f'"{vec.EMA.EDIT_MY_BET}" is not displayed')
        bet.edit_my_acca_button.click()
        selection = list(bet.items_as_ordered_dict.values())[0]
        selection.edit_my_acca_remove_icon.click()
        self.assertTrue(selection.edit_my_acca_undo_icon.is_displayed(), msg='undo icon is not displayed')
        self.assertTrue(selection.leg_remove_marker.is_displayed(), msg='REMOVED text is not displayed')
        bet.confirm_button.click()

    def test_001_verify_that_the_new_bet_type_name_is_displayed(self, open_bets=True):
        """
        DESCRIPTION: Verify that the new bet type name is displayed
        EXPECTED: The new bet type name is displayed
        """
        self.site.wait_content_state_changed()
        self.__class__.bet = self.get_bet_with_my_acca_edit(open_bets=open_bets, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_names[1])
        bet_type = self.bet.bet_type
        self.assertNotEqual(bet_type, self.bet_before_ema, msg=f'Actual bet type "{bet_type}" is same as Expected bet type "{self.bet_before_ema}"')

    def test_002_verify_that_all_selections_from_the_original_acca_are_displayed(self):
        """
        DESCRIPTION: Verify that all selections from the original acca are displayed
        EXPECTED: All selections from the original acca are displayed
        """
        selections = list(self.bet.items_as_ordered_dict.values())
        for selection in selections:
            self.assertIn(selection.event_name, self.event_names, msg=f'"{selection.event_name}" is not present in "{self.event_names}"')

    def test_003_verify_that_the_selections_which_were_removed_have_a_removed_token_displayed(self):
        """
        DESCRIPTION: Verify that the selection(s) which were removed have a Removed token displayed
        EXPECTED: - The selection(s) which were removed have a Removed token displayed
        EXPECTED: - Removed selections should appear below Open selections
        """
        new_selection = list(self.bet.items_as_ordered_dict.values())[-1]
        self.assertTrue(new_selection.leg_remove_marker.is_displayed(),
                        msg='"REMOVED" icon is not displayed')

    def test_004_verify_that_the_stake_is_displayed(self):
        """
        DESCRIPTION: Verify that the stake is displayed
        EXPECTED: The stake is displayed
        EXPECTED: New stake value is received from validateBet request - 'newBetStake' parameter
        """
        new_stake = self.bet.stake.value
        self.assertNotEqual(new_stake, self.stake, msg=f'Actual stake "{new_stake}" is not same as Expected stake "{self.stake}"')

    def test_005_verify_that_prices_are_displayed_for_any_selections(self):
        """
        DESCRIPTION: Verify that prices are displayed for any selections
        EXPECTED: Prices are displayed for any selections
        """
        selections = self.bet.items_as_ordered_dict.values()
        for selection in list(selections):
            self.assertTrue(selection.odds_value, msg=f'The odd: "{selection.odds_value}" is not displayed')

    def test_006_verify_that_the_new_potential_returns_are_displayed(self):
        """
        DESCRIPTION: Verify that the new potential returns are displayed
        EXPECTED: The new potential returns are displayed
        EXPECTED: New potential return value is received from validateBet request - 'betPotentialWin' parameter
        """
        est_returns = self.bet.est_returns
        self.assertNotEqual(est_returns, self.actual_potential_returns, msg=f'Actual returns "{est_returns}" is same as Expected returns "{self.actual_potential_returns}"')

    def test_007_repeat_all_from_1_to_6_steps_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat all from 1 to 6 steps in 'Cash Out' tab
        EXPECTED: results are the same, but removed selections are not shown
        """
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            self.test_001_verify_that_the_new_bet_type_name_is_displayed(open_bets=False)
            self.test_002_verify_that_all_selections_from_the_original_acca_are_displayed()
            self.test_004_verify_that_the_stake_is_displayed()
            self.test_005_verify_that_prices_are_displayed_for_any_selections()
