import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from time import sleep


# @pytest.mark.tst2 # Tote wont available in qa envs
# @pytest.mark.stg2 # Tote wont available in qa envs
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.uk_tote
@pytest.mark.horseracing
@pytest.mark.liveserv_updates
@pytest.mark.races
@vtest
class Test_C1922453_Verify_pop_up_messages_for_Betslip_limitation_for_Tote_bets(BaseUKTote, BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C1922453
    NAME: Verify pop-up messages for Betslip limitation for Tote bets
    DESCRIPTION: This test case verifies pop-up messages for Tote bets in Betslip which appears in the next cases:
    DESCRIPTION: * user tries to add a Tote bet to Betslip and he doesn't have any bets in the Betslip
    DESCRIPTION: * user tries to add a Tote bet to Betslip and he already has Tote bets in the Betslip
    DESCRIPTION: * user tries to add a Tote bet to Betslip and he already has regular (non-Tote) bets in the Betslip
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is sufficient to cover the bet stake
    PRECONDITIONS: * There are no bets in Betslip
    PRECONDITIONS: * Quick Bet functionality is enabled in CMS
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Tote" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Totepool are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- endpoint .symphony-solutions.eu)
    PRECONDITIONS: endpoint can be found using devlog
    """
    keep_browser_open = True

    def make_selection(self, outcomes):
        outcome_name, outcome = outcomes[0]
        checkbox = outcome.items[0]

        checkbox.click()
        self.assertTrue(outcome.items[0].is_selected(timeout=2),
                            msg=f'Cell is not selected for "{outcome_name}" runner')
        return checkbox

    def get_selection_id(self, event_id, outcomes):

        ss_uk_tote_pool_outcomes = self.ss_req.ss_event_to_outcome_for_event(
            event_id=event_id)[0]['event']['children'][0]['market']['children']

        for index, (outcome_name, outcome) in enumerate(outcomes):
            for element in ss_uk_tote_pool_outcomes:
                if element['outcome']['name'].strip('|') == outcome_name:
                    return element['outcome']['id']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event
        """
        event = self.get_uk_tote_event(uk_tote_win=True)
        self.__class__.eventID = event.event_id
        self.__class__.marketID = event.market_id

    def test_001_make_selection_and_tap_add_to_betslip_button(self, tab_name=vec.uk_tote.UK_TOTE_TABS.win):
        """
        DESCRIPTION: Make selection and tap 'ADD TO BETSLIP' button
        EXPECTED: * Bet builder disappears
        EXPECTED: * Tote bet is added to Betslip (betslip icon displays correct indicator)
        EXPECTED: * Selections become unchecked
        EXPECTED: * No pop-up messages appears (as there were no bets in Betslip)
        EXPECTED: * Footer menu is displayed
        """
        self.__class__.outcomes = self.get_single_leg_outcomes(tab_name=tab_name, event_id=self.eventID)
        self.__class__.cell = self.make_selection(outcomes=self.outcomes)
        self.__class__.selection_id = self.get_selection_id(event_id=self.eventID, outcomes=self.outcomes)

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, self.__class__.section = list(sections.items())[0]

        result = wait_for_result(lambda: self.section.bet_builder.is_present(timeout=0) is True,
                                 name='Bet builder has not been shown', timeout=10)
        self.assertTrue(result, msg='Bet builder was not shown')

        self.assertTrue(self.section.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='"Add to betslip" button is not enabled')
        self.section.bet_builder.summary.add_to_betslip_button.click()
        if self.device_name == "Mobile":
            self.assertTrue(self.get_betslip_counter_value() == "1", msg='Tote bet is not added to Betslip')

    def test_002_make_some_more_selections_and_press_add_to_betslip_button(self):
        """
        DESCRIPTION: Make some more selections and press Add to betslip button
        EXPECTED: Pop-up message appears:
        EXPECTED: * The header of message: "NOTICE"
        EXPECTED: * The text of message: "You already have one or more selections in the bet slip that can't be combined, please remove those selections to add any new selection"
        EXPECTED: * "OK" button is displayed
        """
        self.test_001_make_selection_and_tap_add_to_betslip_button()
        self.site.wait_content_state_changed()
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_BETSLIP_LIMITATION, verify_name=False)
        self.assertTrue(self.dialog, msg='Betslip limitation popup did not appeared')
        sleep(5)
        betslip_limitiation_message = self.dialog.message.split("\n")
        self.assertEqual(betslip_limitiation_message[0], vec.betslip.BETSLIP_LIMITATION_MESSAGE,
                         msg=f'Actual bet slip limitation message "{betslip_limitiation_message[0]}" is not equal with '
                             f'Expected limitation message "{vec.betslip.BETSLIP_LIMITATION_MESSAGE}"')
        self.assertTrue(self.dialog.ok_button, msg='"OK" button is not  displayed')

    def test_003_tap_ok_button(self):
        """
        DESCRIPTION: Tap "OK" button
        EXPECTED: * Pop-up message disappears
        EXPECTED: * User is remaining on the same page
        EXPECTED: * Selections are not removed (are still checked)
        """
        self.dialog.ok_button.click()
        try:
            self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_BETSLIP_LIMITATION, timeout=1,verify_name=True)
        except VoltronException:
            self._logger.info('****Voltron exception raised as Pop-up message disappeared****')

    def test_004_open_betslip_and_remove_selections_using_delete_button_or_place_bets(self):
        """
        DESCRIPTION: Open betslip and remove selections (using 'Delete' button) or place bets
        EXPECTED: * Betslip is empty
        EXPECTED: * "Your betslip is empty" message is displayed
        """
        self.site.open_betslip()
        self.clear_betslip()

    def test_005_add_any_single_or_multiple_selection_to_betslip_not_tote_events(self):
        """
        DESCRIPTION: Add any single or multiple selection to betslip (not tote events)
        EXPECTED: * Quick Bet is closed after tapping 'Add to Betslip' button
        EXPECTED: * Bet is added to Betslip
        """
        self.test_001_make_selection_and_tap_add_to_betslip_button()

    def test_006_make_another_tote_selection_and_tap_add_to_betslip(self):
        """
        DESCRIPTION: Make another tote selection and tap Add to betslip
        EXPECTED: Pop-up message appears:
        EXPECTED: * The header of message: "NOTICE"
        EXPECTED: * The text of message: "You already have one or more selections in the bet slip that can't be combined, please remove those selections to add any new selection"
        EXPECTED: * "OK" button is displayed
        """
        self.test_002_make_some_more_selections_and_press_add_to_betslip_button()

    def test_007_tap_ok_button(self):
        """
        DESCRIPTION: Tap "OK" button
        EXPECTED: * Pop-up message disappears
        EXPECTED: * User is remaining on the same page
        EXPECTED: * Selections are not removed (are still checked)
        """
        self.test_003_tap_ok_button()

    def test_008_remove_selections_from_betslip_using_delete_button_or_place_a_bet_and_add_new_selections_from_tote_pool_to_betslip(self):
        """
        DESCRIPTION: Remove selections from betslip (using delete button or place a bet) and add new selections from tote pool to betslip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Tote bet is added to Betslip
        EXPECTED: * No pop-up messages appears (as there were no bets in Betslip)
        EXPECTED: * Betslip indicator is increased by 1
        """
        self.test_004_open_betslip_and_remove_selections_using_delete_button_or_place_bets()
        self.test_001_make_selection_and_tap_add_to_betslip_button()

    def test_009_repeat_step__7(self):
        """
        DESCRIPTION: Repeat step # 7
        EXPECTED: * Quick Bet is closed after tapping 'Add to Betslip' button
        EXPECTED: Pop-up message appears:
        EXPECTED: * The header of message: "NOTICE"
        EXPECTED: * The text of message: "You already have one or more selections in the bet slip that can't be combined, please remove those selections to add any new selection"
        EXPECTED: * "OK" button is displayed
        """
        # covered in above steps

    def test_010_tap_ok_button(self):
        """
        DESCRIPTION: Tap "OK" button
        EXPECTED: * Pop-up message disappears
        EXPECTED: * User is remaining on the same page
        EXPECTED: * Selections are not removed (are still checked)
        """
        # covered in above steps
