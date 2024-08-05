import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


# @pytest.mark.prod - This test case is limited to QA2 only, can't create events in prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C44870200_Verify_the_selection_availability_when_viewing_the_racecard_Forecast_and_tricast_displayed_in_separate_tab_Check_only_two_Selections_are_highligted_for_forecast_and_three_for_tricast_And_any_option_available_for_both_foirecast_and_tricast_Veri(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C44870200
    NAME: "Verify the selection availability when viewing the racecard -Forecast and tricast displayed in separate tab -Check only two Selections are highligted for forecast and three for tricast ...And any option available for both foirecast and tricast -Veri
    DESCRIPTION: "Verify the selection availability when viewing the racecard
    DESCRIPTION: -Forecast and tricast displayed in separate tab
    DESCRIPTION: -Check only two Selections are highligted for forecast and three for tricast ...And any option available for both foirecast and tricast
    DESCRIPTION: -Verify that the non-runners shouldnot be shown in forecast and tricast tabs
    DESCRIPTION: - Check bet placement is working fine and display of betslip and betreceipt"
    """
    keep_browser_open = True
    expected_estimate_returns = 'N/A'

    def preconditions(self):
        """
        PRECONDITIONS: Login into Application
        PRECONDITIONS: Navigate to 'HR/Greyhounds' page
        PRECONDITIONS: Choose event -> see that Ferecast/Tricast Tab is available
        PRECONDITIONS: Navigate to Ferecast/Tricast Tab
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.__class__.event_params = self.ob_config.add_UK_racing_event(number_of_runners=6,
                                                                         forecast_available=True, tricast_available=True, win_or_each_way=False)
        self.__class__.event_name = f"{self.event_params.event_off_time} {self.horseracing_autotest_uk_name_pattern}"
        selection_name, selection_id = list(self.event_params.selection_ids.items())[0]
        self.__class__.new_selection_name = f'{selection_name} N/R'
        self.ob_config.change_selection_name(selection_id=selection_id, new_selection_name=self.new_selection_name)
        self.ob_config.update_selection_result(event_id=self.event_params.event_id, market_id=self.event_params.market_id, selection_id=selection_id, result='V')

    def tricast_forecast_bet_placement(self, forecast, tricast):
        self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing', forecast=forecast, tricast=tricast)
        self.site.open_betslip()
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" are not added to the betslip')
        self.__class__.stake_name, stake = list(selections.items())[0]
        self.enter_stake_amount(stake=(self.stake_name, stake))

    def verify_selection_details_in_betslip(self, market_name):
        betslip = self.get_betslip_content()
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.ordered_collection.values())[0]
        self.assertEqual(stake.market_name, market_name,
                         msg=f'Actual Market name "{stake.market_name}" is not the same as expected "{market_name}"')
        self.assertEqual(stake.event_name, self.event_name,
                         msg=f'Actual Event name "{stake.event_name}" is not the same as expected "{self.event_name}"')
        self.assertTrue(stake.amount_form.has_amount_input(), msg='"Amount input" is not displayed')
        self.assertEqual(stake.est_returns, self.expected_estimate_returns, msg=f'Actual estimate returns: "{stake.est_returns}" is not the same as expected estimate returns:"{self.expected_estimate_returns}"')
        self.assertTrue(betslip.total_stake, msg='"Total Stake" is not displayed')
        self.assertTrue(stake.remove_button, msg='"Remove button" is not displayed')
        self.assertTrue(betslip.bet_now_button.is_displayed(), msg='"Place bet button" is not displayed')
        betslip.bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No "sections" found in BetReceipt')
        receipt_bet_type_section = receipt_sections.get(vec.betslip.SINGLE)
        section_items = receipt_bet_type_section.items_as_ordered_dict
        self.assertTrue(section_items, msg='"No bets" found in BetReceipt')
        bet_info = list(section_items.values())[0]
        self.assertTrue(bet_info.bet_id, msg='"Bet Id" not found')
        self.assertIn(market_name, bet_info.event_market_name, msg=f'Market placed "{market_name}" does not match with bet receipt"{bet_info.event_market_name}"')
        self.assertEqual(self.event_name, bet_info.event_name, msg=f'Event placed "{self.event_name}" does not match with bet receipt"{bet_info.event_name}"')
        self.assertEqual(bet_info.estimate_returns, self.expected_estimate_returns, msg=f'Actual estimate returns: "{bet_info.estimate_returns}" is not the same as expected estimate returns:"{self.expected_estimate_returns}"')
        self.assertEqual(bet_info.total_stake, betslip.total_stake, f'Actual total stake: "{bet_info.total_stake}" is not the same as expected total stake:"{betslip.total_stake}"')

    def test_001_verify_the_selection_availability_when_viewing_the_racecard_for_forecast(self):
        """
        DESCRIPTION: Verify the selection availability when viewing the racecard for forecast
        EXPECTED: Only two selections should be  highligted for forecast
        EXPECTED: And any option available
        """
        self.preconditions()
        # covered in step_5

    def test_002_verify_the_selection_availability_when_viewing_the_racecard_for_tricast(self):
        """
        DESCRIPTION: Verify the selection availability when viewing the racecard for forecast
        EXPECTED: Only three selections should  be highligted for tricast
        EXPECTED: And any option available
        """
        # covered in step_10

    def test_003_verify_that_the_non_runners_shouldnot_be_shown_in_forecast_and_tricast_tabs(self) -> object:
        """
        DESCRIPTION: Verify that the non-runners shouldnot be shown in forecast and tricast tabs
        """
        # covered in step_4 and step_9

    def test_004_select_forecast_tab(self):
        """
        DESCRIPTION: Select 'Forecast' tab
        EXPECTED: Forecast tab is selected
        """
        self.navigate_to_edp(event_id=self.event_params.event_id, sport_name='horse-racing')
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        open_tab = racing_event_tab_content.market_tabs_list.open_tab(vec.racing.RACING_EDP_FORECAST_MARKET_TAB)
        self.assertTrue(open_tab, msg=f'Expected market tab: "{vec.racing.RACING_EDP_FORECAST_MARKET_TAB}" is not selected')
        sections = racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No "sections" was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='"outcomes" not found')
        for outcome_name, outcome in outcomes.items():
            runner_buttons = outcome.items_as_ordered_dict
            self.assertTrue(runner_buttons, msg=f'No "runner buttons"" found for "{outcome_name}"')
            runner_bet_button_names = list(runner_buttons.keys())
            self.assertEqual(runner_bet_button_names, vec.racing.RACING_EDP_FORECAST_RACING_BUTTONS,
                             msg=f'Actual racing button names "{runner_bet_button_names}" '
                             f'does not match expected "{vec.racing.RACING_EDP_FORECAST_RACING_BUTTONS}"')
            self.assertFalse(outcome.is_non_runner, msg=f'"{self.new_selection_name}" is displayed')

    def test_005_select_1st_and_2nd_runners(self):
        """
        DESCRIPTION: Select '1st' and '2nd' runners
        EXPECTED: 1st and 2nd selections are highlighted
        """
        self.tricast_forecast_bet_placement(forecast=True, tricast=False)
        forecast_selections = len(self.stake_name.split("\n"))
        self.assertEqual(forecast_selections, 2, msg='"two selections" are not highlited')

    def test_006_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap 'Add to Betslip' button
        EXPECTED: Selections are added to betslip
        """
        self.verify_selection_details_in_betslip(market_name='Forecast')

    def test_007_navigate_to_betslipverify_that_forecast_single_bet_is_shown(self, market_name='Forecast'):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that Forecast Single bet is shown
        EXPECTED: Forecast bet is shown under SINGLES with appropriate elements:
        EXPECTED: 'Remove' button
        EXPECTED: 'Stake' field
        EXPECTED: Bet selection (Runners) information according to selected runners. e.g. : 1 HorseDan 2 HorseTed From OX99: 1st HorseDan 2nd HorseTed
        EXPECTED: Event name and time
        EXPECTED: Bet Sort: Forecast
        EXPECTED: Total Stake information
        EXPECTED: Coral: Estimated Returns; Ladbrokes: Potential Returns'
        EXPECTED: 'Place Bet' button
        EXPECTED: NOTE: No singles selections are added to Betslip - only Forecast is added to Betslip
        """
        # covered in_6

    def test_008_add_a_stakeverify_that_total_est_returns_is_displayed_na(self):
        """
        DESCRIPTION: Add a Stake
        DESCRIPTION: Verify that Total Est. Returns is displayed N/A
        EXPECTED: The stake is added and shown in the 'Stake' and 'Total Stake' fields
        EXPECTED: ( Coral: Estimated Returns; Ladbrokes: Potential Returns')
        """
        # covered in_6

    def test_009_select_tricast_tab(self):
        """
        DESCRIPTION: Select 'Tricast' tab
        EXPECTED: Tricast tab is selected
        """
        self.navigate_to_edp(event_id=self.event_params.event_id, sport_name='horse-racing')
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        open_tab = racing_event_tab_content.market_tabs_list.open_tab(vec.racing.RACING_EDP_TRICAST_MARKET_TAB)
        self.assertTrue(open_tab, msg=f'Expected market tab: "{vec.racing.RACING_EDP_TRICAST_MARKET_TAB}" is not selected')
        sections = racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No "sections" was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='"outcomes" not found')
        for outcome_name, outcome in outcomes.items():
            runner_buttons = outcome.items_as_ordered_dict
            self.assertTrue(runner_buttons, msg=f'No "runner buttons"" found for "{outcome_name}"')
            runner_bet_button_names = list(runner_buttons.keys())
            self.assertEqual(runner_bet_button_names, vec.racing.RACING_EDP_TRICAST_RACING_BUTTONS,
                             msg=f'Actual racing button names "{runner_bet_button_names}" '
                             f'does not match expected "{vec.racing.RACING_EDP_TRICAST_RACING_BUTTONS}"')
            self.assertFalse(outcome.is_non_runner, msg=f'"{self.new_selection_name}" is displayed')

    def test_010_select_1st_2nd_and_3rd_runners(self):
        """
        DESCRIPTION: Select '1st', '2nd' and '3rd' runners
        EXPECTED: 1st , 2nd and 3rd selections are highlighted
        """
        self.tricast_forecast_bet_placement(forecast=False, tricast=True)
        forecast_selections = len(self.stake_name.split("\n"))
        self.assertEqual(forecast_selections, 3, msg='"three selections" are not highlited')

    def test_011_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap 'Add to Betslip' button
        EXPECTED: Selections are added to betslip
        """
        self.verify_selection_details_in_betslip(market_name='Tricast')

    def test_012_navigate_to_betslipverify_that_tricast_single_bet_is_shown(self, market_name='Tricast'):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that Tricast Single bet is shown
        EXPECTED: Tricast bet is shown under SINGLES with appropriate elements:
        EXPECTED: Remove button
        EXPECTED: 'Stake' field
        EXPECTED: Bet selection (Runners) information according to selected runners. e.g. : 1 HorseDan 2 HorseTed 3 HourseBen : 1st HorseDan 2nd HorseTed 3rd HourseBen
        EXPECTED: Event name and time
        EXPECTED: Bet Sort: Tricast
        EXPECTED: Total Stake information
        EXPECTED: Coral: Estimated Returns; Ladbrokes: Potential Returns')
        EXPECTED: 'Place Bet' button
        EXPECTED: NOTE: No singles selections are added to Betslip - only Tricast is added to Betslip
        """
        # covered in step_11

    def test_013_add_a_stakeverify_that_total_est_returns_is_displayed_na(self):
        """
        DESCRIPTION: Add a Stake
        DESCRIPTION: Verify that Total Est. Returns is displayed N/A
        EXPECTED: The stake is added and shown in the 'Stake' and 'Total Stake' fields
        EXPECTED: Total Est. Returns information displayed as N/A ( Coral: Estimated Returns; Ladbrokes: Potential Returns')
        """
        # covered in step_11
