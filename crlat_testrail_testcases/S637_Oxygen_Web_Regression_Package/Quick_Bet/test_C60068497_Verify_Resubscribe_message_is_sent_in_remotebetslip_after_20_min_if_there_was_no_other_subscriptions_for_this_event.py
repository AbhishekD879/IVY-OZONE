import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C60068497_Verify_Resubscribe_message_is_sent_in_remotebetslip_after_20_min_if_there_was_no_other_subscriptions_for_this_event(Common):
    """
    TR_ID: C60068497
    NAME: Verify Resubscribe message is sent in remotebetslip after  20 min if there was no other subscriptions for this event
    DESCRIPTION: This test case verifies Resubscribe message is sent in remotebetslip after  20 min if there was no other subscriptions for this event
    PRECONDITIONS: 1. 2 users - user_A and user_B existing with  QuickBet turned on is settings.
    PRECONDITIONS: Users are logged in in different browsers.
    PRECONDITIONS: 2. Event is configured and is available for bet placement
    PRECONDITIONS: *NOTE:*
    PRECONDITIONS: - Remotebetslip connection opens as soon as the app is loaded. To verify open DevTools > Network > WS and search for remotebetslip
    PRECONDITIONS: - Confluence Page with links to Kibana logs: https://confluence.egalacoral.com/display/SPI/Symphony+Infrastructure+creds
    PRECONDITIONS: ** Test case is actual starting from OX108
    """
    keep_browser_open = True

    def test_001_select_user_a_and_add_selection_to_quickbet_from_event_from_preconditions(self):
        """
        DESCRIPTION: Select user_A and add selection to Quickbet from event from preconditions.
        EXPECTED: * QuickBet opens
        EXPECTED: * Subscribe to event message sent
        """
        pass

    def test_002_wait_for_10_min_and_then_select_user_b_and_add_selection_to_quickbet_from_same_eventnote__no_other_users_should_add_selectionplace_bet_on_this_event__make_sure_that_both_user_a_and_user_b_are_processed_on_the_same_machinescheck_container_id_in_kibana_logs_it_should_be_same_for_both_usersindexphpattachmentsget122009951(self):
        """
        DESCRIPTION: Wait for 10 min and then select user_B and add selection to QuickBet from same event
        DESCRIPTION: *NOTE:*
        DESCRIPTION: - no other users should add selection/place bet on this event
        DESCRIPTION: - Make sure that both user_A and user_B are processed on the same machines.(Check Container_ID in Kibana logs. It should be same for both Users.)
        DESCRIPTION: ![](index.php?/attachments/get/122009951)
        EXPECTED: * Quick Bet opens
        EXPECTED: * Subscribe to event message sent
        """
        pass

    def test_003_wait_for_another_10_min_and_verify_remotebetslip_resubscribe_messages_for_user_a_and_user_b_in_kibana_logs_for_selected_eventnote_no_other_user_should_add_selectionplace_bet_on_this_event(self):
        """
        DESCRIPTION: Wait for another 10 min and verify remotebetslip resubscribe messages for user_A and user_B in Kibana logs for selected Event
        DESCRIPTION: *NOTE:* no other user should add selection/place bet on this event
        EXPECTED: * Resubscribe messages are NOT present in Kibana Logs for EventID of the Event used in Step 1
        """
        pass

    def test_004_wait_for_another_10_min_should_be_20_min_in_total_since_last_subscribe_and_verify_remotebetslip_resubscribe_messages_for_user_a_and_user_b_in_kibana_logs_for_selected_eventnote_no_updates_should_be_triggered_during_this_time_and_no_other_user_should_add_selectionplace_bet_on_this_event(self):
        """
        DESCRIPTION: Wait for another 10 min (should be 20 min in total since last subscribe) and verify remotebetslip resubscribe messages for user_A and user_B in Kibana logs for selected Event.
        DESCRIPTION: *NOTE:* no updates should be triggered during this time and no other user should add selection/place bet on this event
        EXPECTED: * Resubscribe messages are present in Kibana logs for EventID of the Event used in Step 1 and Step 2
        EXPECTED: ![](index.php?/attachments/get/122009955)
        """
        pass

    def test_005_in_ti_trigger_updates_for_this_selection_on_different_levelsprice_update_or_suspension_on_eventmarketselection_levels_and_verify_if_it_was_received_in_ws(self):
        """
        DESCRIPTION: In TI trigger updates for this selection on different levels(price update or suspension on event/market/selection levels) and verify if it was received in WS
        EXPECTED: * Live update are received in WS and correctly displayed on UI
        """
        pass

    def test_006_close_quick_bet_for_both_user_a_and_user_b_wait_20_minutes_and_verify_that_there_is_no_resubscribe_message_in_kibana_logs_for_selected_eventnote_no_other_user_should_add_selectionplace_bet_on_this_event(self):
        """
        DESCRIPTION: Close Quick bet for both user_A and user_B. Wait 20 minutes and verify that there is no resubscribe message in Kibana logs for selected Event.
        DESCRIPTION: *NOTE*: no other user should add selection/place bet on this event
        EXPECTED: * Resubscribe messages are NOT present in Kibana Logs for EventID of the Event used in Step 1
        """
        pass
