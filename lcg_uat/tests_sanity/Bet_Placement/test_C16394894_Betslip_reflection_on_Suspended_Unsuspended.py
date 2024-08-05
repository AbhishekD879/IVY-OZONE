import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Event cannot be suspended
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.sanity
@vtest
class Test_C16394894_Betslip_reflection_on_Suspended_Unsuspended(BaseBetSlipTest):
    """
    TR_ID: C16394894
    NAME: Betslip reflection on Suspended/Unsuspended
    DESCRIPTION: This test case verifies Betslip reflection when <Sport> Event is Suspended/Unsuspended for Single Bet.
    """
    keep_browser_open = True
    selection_name = []
    selection_ids = []
    eventIDs = []
    first_sport = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football event and racing events
        """
        if self.first_sport:
            for i in range(2):
                event_params = self.ob_config.add_autotest_premier_league_football_event()
                self.selection_name.append(list(event_params.selection_ids.keys())[0])
                self.selection_ids.append(list(event_params.selection_ids.values())[0])
                self.eventIDs.append(event_params.event_id)
        else:
            for i in range(2):
                event_params1 = self.ob_config.add_UK_racing_event()
                self.selection_name.append(list(event_params1.selection_ids.keys())[0])
                self.selection_ids.append(list(event_params1.selection_ids.values())[0])
                self.eventIDs.append(event_params1.event_id)

    def test_001_add_single_sport_bet_to_the_betslipnavigate_to_betslip(self):
        """
        DESCRIPTION: Add single <Sport> bet to the Betslip
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Betslip is opened, selection is displayed
        """
        self.site.wait_content_state('Homepage')
        self.__class__.betslip_counter = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        single_section = self.get_betslip_sections().Singles
        self.__class__.stake = single_section.get(self.selection_name[0])
        self.assertTrue(self.stake, msg=f'Stake: "{self.selection_name[0]}" section not found')

    def test_002_trigger_the_following_situation_for_this_eventeventstatuscodes_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode="S" and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: * 'Stake' field, 'Odds' and 'Estimated returns'  - disabled and greyed out.
        EXPECTED: * 'Bet Now' ('Log In and Bet') button is disabled and greyed out
        EXPECTED: * Error message 'Sorry, the event has been suspended' is shown below corresponding single
        EXPECTED: * Warning message 'Please beware that # of your selections has been suspended' is shown on the yellow background in the bottom of the Betslip
        EXPECTED: **From OX99**
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: ![](index.php?/attachments/get/33909)
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        EXPECTED: ![](index.php?/attachments/get/33910)
        """
        self.ob_config.change_event_state(event_id=self.eventIDs[0], displayed=True, active=False)
        self.verify_betslip_is_suspended(stakes=[self.stake])

    def test_003_from_ox_99_for_ladbrokeswait_5_secverify_that_message_on_the_top_ob_betslip_is_removed(self):
        """
        DESCRIPTION: **From OX 99 for Ladbrokes:**
        DESCRIPTION: Wait 5 sec
        DESCRIPTION: Verify that message on the top ob Betslip[ is removed
        EXPECTED: Message 'Some of your selections have been suspended' is removed from the top of the Betslip
        """
        self.site.wait_content_state_changed(timeout=5)
        if self.brand == 'ladbrokes':
            self.assertFalse(self.get_betslip_content().top_notification.wait_for_error(expected_result=False,
                                                                                        timeout=10),
                             msg=f'Betslip top error message did not disappear')

    def test_004_make_the_event_active_againeventstatuscodea_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Make the event active again:
        DESCRIPTION: eventStatusCode="A" and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: * 'Stake' field and 'Bet Now' ('Log In and Bet') buttons are enabled and not greyed out.
        EXPECTED: * Both error messages disappear from the Betslip
        EXPECTED: **After OX99**
        EXPECTED: * Selection becomes enabled
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (until stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_event_state(event_id=self.eventIDs[0], displayed=True, active=True)
        self.verify_betslip_is_active(stakes=[self.stake], is_stake_filled=False)

    def test_005_add_few_more_selection_to_betslipnavigate_to_betslip_and_enter_stake_for_the_multiple_bet(self):
        """
        DESCRIPTION: Add few more selection to Betslip
        DESCRIPTION: Navigate to Betslip and Enter Stake for the Multiple bet
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[1])
        betslip_section = self.get_betslip_sections(multiples=True)
        self.__class__.singles_section, multiples_section = betslip_section.Singles, betslip_section.Multiples
        self.__class__.stake = list(multiples_section.items())[0]
        self.assertTrue(self.stake, msg=f'Stake: "{vec.betslip.MULTIPLES}" section not found')
        self.enter_stake_amount(stake=self.stake)

    def test_006_suspend_two_of_the_eventseventstatuscodes_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Suspend two of the events:
        DESCRIPTION: eventStatusCode="S" and at the same time have Betslip page opened to watch for updates
        EXPECTED: - 'Multiples' section is not rebuilt and it is still contains selection from Suspended event
        EXPECTED: - No error messages are displayed for active selections
        EXPECTED: **Before OX99**
        EXPECTED: * Error message 'Sorry, the event has been suspended' is shown on the red background below the single from Suspended event
        EXPECTED: * 'Stake' field is disabled and greyed out for the single from Suspended market
        EXPECTED: * 'Bet Now' ('Log In and Bet') button is disabled and greyed out
        EXPECTED: * Warning message "Please beware that # of your selections has been suspended. Please remove suspended selections to get new multiple options"
        EXPECTED: **After OX99**
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware some of your selections have been suspended'
        EXPECTED: ![](index.php?/attachments/get/33915)
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Some of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'Some of your selections have been suspended' with duration: 5s
        EXPECTED: ![](index.php?/attachments/get/33914)
        """
        self.ob_config.change_event_state(event_id=self.eventIDs[0], displayed=True, active=False)
        self.ob_config.change_event_state(event_id=self.eventIDs[1], displayed=True, active=False)
        stakes = [self.singles_section.get(self.selection_name[0]), self.singles_section.get(self.selection_name[1])]
        if self.brand == 'ladbrokes':
            actual_top_message = self.get_betslip_content().top_notification.wait_for_error(timeout=60)
            if not vec.betslip.BELOW_MULTIPLE_DISABLED == actual_top_message:
                sleep(2)
                actual_top_message = self.get_betslip_content().top_notification.wait_for_error(timeout=60)
            self.assertEqual(actual_top_message, vec.betslip.BELOW_MULTIPLE_DISABLED,
                             msg=f'Error message "{actual_top_message}" != expected "{vec.betslip.BELOW_MULTIPLE_DISABLED}"')
            self.assertFalse(self.get_betslip_content().top_notification.wait_for_error(expected_result=False,
                                                                                        timeout=6),
                             msg=f'Betslip top error message did not disappear')
            result = self.get_betslip_content().wait_for_specified_error(expected_message=vec.betslip.BELOW_MULTIPLE_DISABLED,
                                                                         timeout=10)
            self.assertTrue(result,
                            msg=f'Error message "{self.get_betslip_content().error}" != expected "{vec.betslip.BELOW_MULTIPLE_DISABLED}"')
        else:
            result = self.get_betslip_content().wait_for_specified_error(
                expected_message=vec.betslip.MULTIPLE_DISABLED,
                timeout=10)
            self.assertTrue(result,
                            msg=f'Error message "{self.get_betslip_content().error}" != expected "{vec.betslip.MULTIPLE_DISABLED}"')

        for stake in stakes:
            self.assertTrue(stake.is_suspended(timeout=5), msg=f'Stake is not suspended')
            self.assertFalse(stake.amount_form.input.is_enabled(expected_result=False, timeout=5),
                             msg=f'Stake amount input field for suspended event "{stake.event_name}" is not disabled')

        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                         msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" button is not disabled')

    def test_007_unsuspend_the_same_eventseventstatuscodea_and_at_the_same_tame_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Unsuspend the same events:
        DESCRIPTION: eventStatusCode="A" and at the same tame have Betslip page opened to watch for updates
        EXPECTED: 'Multiples' section is not rebuilt
        EXPECTED: **Before OX99**
        EXPECTED: * Both error messages disappear from the Betslip
        EXPECTED: * 'Stake' field and 'Bet Now' ('Log In and Bet') buttons are enabled and not greyed out for the single
        EXPECTED: **After OX99**
        EXPECTED: * Selection become enabled for unsuspended event
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        self.ob_config.change_event_state(event_id=self.eventIDs[0], displayed=True, active=True)
        self.ob_config.change_event_state(event_id=self.eventIDs[1], displayed=True, active=True)
        self.verify_betslip_is_active(stakes=[self.singles_section.get(self.selection_name[0]), self.singles_section.get(self.selection_name[1])], is_stake_filled=True)

    def test_008_remove_selection_and_add_race_selection_to_betslipprovide_same_verification_for_race_events(self):
        """
        DESCRIPTION: Remove selection and add <Race> selection to Betslip
        DESCRIPTION: Provide same verification for <Race> events
        EXPECTED: Results are the same
        """
        self.clear_betslip()
        self.selection_ids.clear()
        self.selection_name.clear()
        self.eventIDs.clear()
        self.__class__.first_sport = False
        self.test_000_preconditions()
        self.test_001_add_single_sport_bet_to_the_betslipnavigate_to_betslip()
        self.test_002_trigger_the_following_situation_for_this_eventeventstatuscodes_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates()
        self.test_003_from_ox_99_for_ladbrokeswait_5_secverify_that_message_on_the_top_ob_betslip_is_removed()
        self.test_004_make_the_event_active_againeventstatuscodea_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates()
        self.test_005_add_few_more_selection_to_betslipnavigate_to_betslip_and_enter_stake_for_the_multiple_bet()
        self.test_006_suspend_two_of_the_eventseventstatuscodes_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates()
        self.test_007_unsuspend_the_same_eventseventstatuscodea_and_at_the_same_tame_have_betslip_page_opened_to_watch_for_updates()
