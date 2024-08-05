import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C64378764_Verify_prize_table_configuration_with_different_freebet_ids_and_check_if_the_higher_prize_freebets_get_triggers_to_the_entries_for_which_it_is_allocated(Common):
    """
    TR_ID: C64378764
    NAME: Verify prize table configuration with different freebet ids and check if the higher prize freebets get triggers to the entries for which it is allocated
    DESCRIPTION: This case verifies whether the prize table configured with different freebet ids for an entry triggers higher prize freebet for that entry for which it is allocated
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: Create a contests for an events
    PRECONDITIONS: Contest should be created for future events
    PRECONDITIONS: Important: While creating contest give multiple prize combinations including Cash, freebet, ticket, voucher.
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds."
    PRECONDITIONS: 5) Toggle on automated prize allocation during contest creation
    """
    keep_browser_open = True

    def test_001_in_cms_create_a_contest_with_prizes_which_has_two_freebets_and_two_ticketsdifferent_values_configured_and_user_should_place_bets_on_the_contest(self):
        """
        DESCRIPTION: In CMS, create a contest with prizes which has two freebets and two tickets(different values) configured and User should place bets on the contest.
        EXPECTED: Prizes should be allocated in leaderboard as per configurations.
        """
        pass

    def test_002_once_event_is_live_and_after_90_mins_ert_should_be_receivedafter_10_mins_header_should_be_received_and_prize_allocation_process_should_be_started(self):
        """
        DESCRIPTION: Once event is live and after 90 mins, ERT should be received.
        DESCRIPTION: After 10 mins, header should be received and prize allocation process should be started.
        EXPECTED: ERT is received and the  post leaderboard is seen.
        EXPECTED: ERT grace header is received and can check in Kibana with the below string.
        EXPECTED: "ERT flag from kafka"
        EXPECTED: Once post leaderboard is received check for the below string in Kibana.
        EXPECTED: "5AShowdown started postmatch process for"
        EXPECTED: Once post match process is completed, search for the below string in Kibana, so that a request from Leaderboard is sent to CRM for prize allocation process
        EXPECTED: "5AShowdown CRM publish for unique request id"
        EXPECTED: Response for the above request can be verified with the below string.
        EXPECTED: "5AShowdown CRM consumed for unique request id"
        EXPECTED: Each and every prize has a response along with reward values, transaction IDs.
        EXPECTED: Example of response that is seen in Kibana:
        EXPECTED: 14:39:38.136 INFO  [scheduling-1] com.entain.oxygen.showdown.service.CRMUpdateService
        EXPECTED: 5AShowdown CRM publish for unique request id :: 2147607982-619650b3e1df502ae6486f96, crmAckMessage:{"uniqueRequestId":"2147607982-619650b3e1df502ae6486f96","contestId":"619650b3e1df502ae6486f96","betId":"2147607982","accountName":"ld_Gouth1","rewardType":"CASH","rewardValue":17.0,"rewardCurrency":"GBP","communicationTemplateId":"/id/904d944Tc-c7e5-43e4-a788-9e1e23479c30","commmuncationTypes":["OVERLAY","TOASTER","INBOX"],"communicationReplaceableParams":{},"source":"LCG","campaignType":"5ASIDE"}14:39:38.136 INFO  [scheduling-1] com.entain.oxygen.showdown.service.CRMUpdateService - 5AShowdown CRM publish for unique request id :: 2147607982-619650b3e1df502ae6486f96, crmAckMessage:{"uniqueRequestId":"2147607982-619650b3e1df502ae6486f96","contestId":"619650b3e1df502ae6486f96","betId":"2147607982","accountName":"ld_Gouth1","rewardType":"CASH","rewardValue":17.0,"rewardCurrency":"GBP","communicationTemplateId":"/id/904d944Tc-c7e5-43e4-a788-9e1e23479c30","commmuncationTypes":["OVERLAY","TOASTER","INBOX"],"communicationReplaceableParams":{},"source":"LCG","campaignType":"5ASIDE"}
        """
        pass

    def test_003_now_verify_the_prize_allocation_for_entries_which_have_same_prize_type_with_different_prize_value(self):
        """
        DESCRIPTION: Now verify the prize allocation for entries which have same prize type with different prize value
        EXPECTED: Higher prize value should be allocated for entry which has same prize type with different values.
        EXPECTED: For example:
        EXPECTED: Freebet of 5 value for entry 1
        EXPECTED: Freebet of 10 value for entry 1
        EXPECTED: In the above case entry 1 should get freebet of 10 value and there should be a request and response seen only for Freebet value 10 not for 5 value.
        """
        pass
