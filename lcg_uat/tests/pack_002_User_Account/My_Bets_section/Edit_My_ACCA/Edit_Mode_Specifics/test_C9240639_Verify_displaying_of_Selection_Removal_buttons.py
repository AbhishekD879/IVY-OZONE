import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C9240639_Verify_displaying_of_Selection_Removal_buttons(BaseCashOutTest):
    """
    TR_ID: C9240639
    NAME: Verify displaying of Selection Removal buttons
    DESCRIPTION: This test case verifies that Selection Removal buttons after user taps on 'EDIT MY ACCA'/BET' button and user has two or more open selections
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Login with User1
    PRECONDITIONS: User1 has 2(bets) with cash out available placed on TREBLE
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    PRECONDITIONS: NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True
    number_of_events = 3
    selection_ids = []

    def get_bets(self, open_bets=True):
        if open_bets:
            self.site.open_my_bets_open_bets()
            _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history._bet_types_TBL.upper(),
                selection_ids=self.selection_ids)
        else:
            self.site.open_my_bets_cashout()
            _, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history._bet_types_TBL.upper(),
                selection_ids=self.selection_ids)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: EMA is enabled in CMS
        PRECONDITIONS: User should be logged in
        PRECONDITIONS: Login with User1
        PRECONDITIONS: User1 has 2(bets) with cash out available placed on TREBLE
        PRECONDITIONS: All selections in the placed bet are active
        PRECONDITIONS: All selections in the placed bet are open
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
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
        else:
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)
            event_params = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events)
            self.selection_ids = self.selection_ids + [list(event.selection_ids.values())[0] for event in event_params]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_my_bets__cashoutverify_that_edit_my_bet_coraledit_my_acca_ladbrokes_button_and_event_details_are_shown_for_treble_bets(self, open_bets=False, brand='bma'):
        """
        DESCRIPTION: Navigate to My Bets > Cashout
        DESCRIPTION: Verify that 'EDIT MY BET' (Coral)/'EDIT MY ACCA' (Ladbrokes) button and event details are shown for TREBLE bets
        EXPECTED: The appropriate elements are shown for TREBLE bet:
        EXPECTED: - 'EDIT MY BET' (Coral)/'EDIT MY ACCA' (Ladbrokes) button is shown
        EXPECTED: - Selections details
        EXPECTED: - Event Name
        EXPECTED: - Event Time
        EXPECTED: - Scores (For Inplay Events)
        EXPECTED: - Winning / Losing Arrow (For Inplay Events)
        """
        if self.brand in brand:
            self.get_bets(open_bets=open_bets)
            self.assertTrue(self.bet.edit_my_acca_button, msg=f' "{vec.EMA.EDIT_MY_BET}" is not displayed"')
            selections = self.bet.items_as_ordered_dict.values()
            for selection in list(selections):
                self.assertTrue(selection.event_name, msg=f'The event name: "{selection.event_name}" is not displayed')
                self.assertTrue(selection.outcome_name,
                                msg=f'The outcome name: "{selection.outcome_name}" is not displayed')
                self.assertTrue(selection.odds_value, msg=f'The odd: "{selection.odds_value}" is not displayed')
                self.assertTrue(selection.event_time, msg=f'The event time: "{selection.event_time}" is not displayed')

    def test_002_tap_edit_my_betacca_button_for_the_first_betverify_that_selection_removal_buttons_are_displayed_adjacent_to_all_selections_in_the_bet(self, brand='bma'):
        """
        DESCRIPTION: Tap 'EDIT MY BET/ACCA' button for the first bet
        DESCRIPTION: Verify that 'Selection Removal' buttons are displayed adjacent to all selections in the bet
        EXPECTED: The appropriate elements are shown for each selection in the TREBLE bet:
        EXPECTED: - Selection details
        EXPECTED: - Event Name
        EXPECTED: - Event Time
        EXPECTED: - Scores (For Inplay Events)
        EXPECTED: - Winning / Losing Arrow (For Inplay Events)
        EXPECTED: - Selection removal button
        EXPECTED: - Message "Edit My Acca uses the cash out value of this bet and the latest odds of each selection" is shown as ped design
        EXPECTED: - 'CONFIRM' button is shown and is NOT be clickable
        EXPECTED: - 'Cash Out' button is NOT shown
        """
        if self.brand in brand:
            self.bet.edit_my_acca_button.click()
            self.site.wait_splash_to_hide(10)
            selections = self.bet.items_as_ordered_dict.values()
            for selection in list(selections):
                self.assertTrue(selection.has_edit_my_acca_remove_icon(), msg='"removal button" is not displayed')
                self.assertTrue(selection.event_name, msg=f'The event name: "{selection.event_name}" is not displayed')
                self.assertTrue(selection.outcome_name,
                                msg=f'The outcome name: "{selection.outcome_name}" is not displayed')
                self.assertTrue(selection.odds_value, msg=f'The odd: "{selection.odds_value}" is not displayed')
                self.assertTrue(selection.event_time, msg=f'The event time: "{selection.event_time}" is not displayed')
            cancel_button_text = self.bet.edit_my_acca_button.name
            self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                             msg=f'Actual text:"{vec.EMA.EDIT_MY_BET}" is not changed to Expected text:"{vec.EMA.CANCEL}".')
            edit_warning_msg = self.bet.edit_my_acca_warning_message
            self.assertEqual(edit_warning_msg, vec.ema.EDIT_WARNING,
                             msg=f'Actual message: "{edit_warning_msg}" is not the same as Expected message: "{vec.ema.EDIT_WARNING}"')
            self.assertTrue(self.bet.confirm_button.is_displayed(),
                            msg=f'"{vec.ema.CONFIRM_EDIT}" button is not displayed')
            self.assertFalse(self.bet.confirm_button.is_enabled(expected_result=False),
                             msg=f'"{vec.ema.CONFIRM_EDIT}" button is clickable')
            self.assertFalse(self.bet.has_buttons_panel(expected_result=False),
                             msg=f'"{self.bet.has_buttons_panel()}" is displayed')

    def test_003_tap_the_selection_removal_x_button_for_any_selection(self, brand='bma'):
        """
        DESCRIPTION: Tap the Selection Removal "X" button for any selection
        EXPECTED: - The Selection Removal "X" button is no longer displayed next to the removed selection
        EXPECTED: - The Selection Removal "X" button remains displayed next to all other open selections
        """
        if self.brand in brand:
            self.__class__.selections = self.bet.items_as_ordered_dict.values()
            self.assertTrue(self.selections, msg=f'Selections: "{self.selections}"not displayed')
            selection = list(self.selections)[0]
            selection.edit_my_acca_remove_icon.click()
            result = wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(),
                                     name='"UNDO button" to be displayed', timeout=60)
            self.assertTrue(result,
                            msg='"UNDO button" is not displayed when the user clicks on the "Selection removal icon(X)"')
            self.assertTrue(selection.leg_remove_marker.is_displayed(), msg='"REMOVED" icon is not displayed')
            self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                             msg='"Selection removal icon(X)" is still displayed"')
            for selection in list(self.selections)[1:]:
                self.assertTrue(selection.has_edit_my_acca_remove_icon(),
                                msg='"Selection removal icon(X)" is not displayed"')

    def test_004_tap_the_selection_removal_x_button_for_any_selection_one_more_time(self, brand='bma'):
        """
        DESCRIPTION: Tap the Selection Removal "X" button for any selection one more time
        EXPECTED: - The Selection Removal "X" button is no longer displayed next to the removed selection
        EXPECTED: - The Selection Removal "X" button remains displayed next to all other open selections
        EXPECTED: - 'Selection Removal' button is non-clickable on the last open selection
        """
        if self.brand in brand:
            selection = list(self.selections)[1]
            selection.edit_my_acca_remove_icon.click()
            result = wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(),
                                     name='"UNDO button" to be displayed', timeout=60)
            self.assertTrue(result,
                            msg='"UNDO button" is not displayed when the user clicks on the "Selection removal icon(X)"')
            self.assertTrue(selection.leg_remove_marker.is_displayed(), msg='"REMOVED" icon is not displayed')
            self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                             msg='"Selection removal icon(X)" is still displayed"')
            selection = list(self.selections)[2]
            self.assertFalse(selection.edit_my_acca_remove_icon.click(),
                             msg='"Last Open Selection" is still in clickable state')
            self.bet.edit_my_acca_button.click()

    def test_005_navigate_to_my_bets__open_betsverify_that_edit_my_betacca_button_and_event_details_are_shown_for_treble_bets(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/ACCA' button and event details are shown for TREBLE bets
        EXPECTED: The appropriate elements are shown for TREBLE bet:
        EXPECTED: - 'EDIT MY BET/ACCA' button is shown
        EXPECTED: - Selections details
        EXPECTED: - Event Name
        EXPECTED: - Event Time
        EXPECTED: - Scores (For Inplay Events)
        EXPECTED: - Winning / Losing Arrow (For Inplay Events)
        """
        self.test_001_navigate_to_my_bets__cashoutverify_that_edit_my_bet_coraledit_my_acca_ladbrokes_button_and_event_details_are_shown_for_treble_bets(open_bets=True, brand='bma,ladbrokes')

    def test_006_tap_edit_my_betacca_button_for_the_first_betverify_that_selection_removal_buttons_are_displayed_next_to_all_selections_in_the_bet(
            self):
        """
        DESCRIPTION: Tap 'EDIT MY BET/ACCA' button for the first bet
        DESCRIPTION: Verify that 'Selection Removal' buttons are displayed next to all selections in the bet
        EXPECTED: The appropriate elements are shown for each selection in the TREBLE bet:
        EXPECTED: - Selection details
        EXPECTED: - Event Name
        EXPECTED: - Event Time
        EXPECTED: - Scores (For Inplay Events)
        EXPECTED: - Winning / Losing Arrow (For Inplay Events)
        EXPECTED: - Selection removal button
        EXPECTED: - Message "Edit My Acca uses the cash out value of this bet and the latest odds of each selection"
        EXPECTED: - 'CONFIRM' button is shown and is NOT be clickable
        EXPECTED: - 'Cash Out' button is NOT shown
        """
        self.test_002_tap_edit_my_betacca_button_for_the_first_betverify_that_selection_removal_buttons_are_displayed_adjacent_to_all_selections_in_the_bet(brand='bma,ladbrokes')

    def test_007_tap_the_selection_removal_x_button_for_any_selection(self):
        """
        DESCRIPTION: Tap the Selection Removal "X" button for any selection
        EXPECTED: - The Selection Removal "X" button is no longer displayed next to the removed selection
        EXPECTED: - The Selection Removal "X" button remains displayed next to all other open selections
        """
        self.test_003_tap_the_selection_removal_x_button_for_any_selection(brand='bma,ladbrokes')

    def test_008_tap_the_selection_removal_x_button_for_any_selection_one_more_time(self):
        """
        DESCRIPTION: Tap the Selection Removal "X" button for any selection one more time
        EXPECTED: - The Selection Removal "X" button is no longer displayed next to the removed selection
        EXPECTED: - The Selection Removal "X" button remains displayed next to all other open selections
        EXPECTED: - 'Selection Removal' button is non-clickable on the last open selection
        """
        self.test_004_tap_the_selection_removal_x_button_for_any_selection_one_more_time(brand='bma,ladbrokes')
