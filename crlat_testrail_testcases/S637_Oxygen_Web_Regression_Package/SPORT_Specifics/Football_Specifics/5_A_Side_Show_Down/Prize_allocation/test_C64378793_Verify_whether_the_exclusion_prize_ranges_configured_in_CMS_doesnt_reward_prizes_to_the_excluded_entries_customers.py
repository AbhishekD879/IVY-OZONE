import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C64378793_Verify_whether_the_exclusion_prize_ranges_configured_in_CMS_doesnt_reward_prizes_to_the_excluded_entries_customers(Common):
    """
    TR_ID: C64378793
    NAME: Verify whether the exclusion prize ranges configured in CMS doesn't reward prizes to the excluded entries/customers
    DESCRIPTION: This test case verifies, if excluded prizes for respective positions are seen request and response for prize allocation in kibana
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

    def test_001_in_cms_create_a_contest_with_prizes_which_has_configurations_with_excluding_positions_and_user_should_place_bets_on_the_contest(self):
        """
        DESCRIPTION: In CMS, create a contest with prizes which has configurations with excluding positions and User should place bets on the contest.
        EXPECTED: Prizes should be allocated in leaderboard as per configurations.
        """
        pass

    def test_002_once_event_is_live_and_after_90_mins_ert_should_be_receivedafter_10_mins_header_should_be_received_and_prize_allocation_process_should_be_started(self):
        """
        DESCRIPTION: Once event is live and after 90 mins, ERT should be received.
        DESCRIPTION: After 10 mins, header should be received and prize allocation process should be started.
        EXPECTED: - ERT is received and the  post leaderboard is seen.
        EXPECTED: - ERT grace header is received and can check in Kibana with the below string.
        EXPECTED: "ERT flag from kafka"
        EXPECTED: - Once post leaderboard is received check for the below string in Kibana.
        EXPECTED: "5AShowdown started postmatch process for"
        EXPECTED: - Once post match process is completed, search for the below string in Kibana, so that a request from Leaderboard is sent to CRM for prize allocation process.
        EXPECTED: "5AShowdown CRM publish for unique request id"
        EXPECTED: - Response for the above request can be verified with the below string.
        EXPECTED: "5AShowdown CRM consumed for unique request id"
        EXPECTED: Each and every prize has a response along with reward values, transaction IDs.
        EXPECTED: Example of request that is seen in Kibana:
        EXPECTED: 14:39:38.136 INFO  [scheduling-1] com.entain.oxygen.showdown.service.CRMUpdateService 5AShowdown CRM publish for unique request id :: 2147607982-619650b3e1df502ae6486f96, crmAckMessage:{"uniqueRequestId":"2147607982-619650b3e1df502ae6486f96","contestId":"619650b3e1df502ae6486f96","betId":"2147607982","accountName":"ld_Gouth1","rewardType":"CASH","rewardValue":17.0,"rewardCurrency":"GBP","communicationTemplateId":"/id/904d944Tc-c7e5-43e4-a788-9e1e23479c30","commmuncationTypes":["OVERLAY","TOASTER","INBOX"],"communicationReplaceableParams":{},"source":"LCG","campaignType":"5ASIDE"}14:39:38.136 INFO  [scheduling-1] com.entain.oxygen.showdown.service.CRMUpdateService 5AShowdown CRM publish for unique request id :: 2147607982-619650b3e1df502ae6486f96, crmAckMessage:{"uniqueRequestId":"2147607982-619650b3e1df502ae6486f96","contestId":"619650b3e1df502ae6486f96","betId":"2147607982","accountName":"ld_Gouth1","rewardType":"CASH","rewardValue":17.0,"rewardCurrency":"GBP","communicationTemplateId":"/id/904d944Tc-c7e5-43e4-a788-9e1e23479c30","commmuncationTypes":["OVERLAY","TOASTER","INBOX"],"communicationReplaceableParams":{},"source":"LCG","campaignType":"5ASIDE"}
        EXPECTED: Response for the above request :
        EXPECTED: 14:39:40.274 INFO  [org.springframework.kafka.KafkaListenerEndpointContainer#4-5-C-1] com.entain.oxygen.showdown.service.CRMUpdateService 5AShowdown CRM consumed for unique request id :: 2147607982-619650b3e1df502ae6486f96, TransactionId:300079888214760798288647, response:RewardAckResponse(uniqueRequestId=2147607982-619650b3e1df502ae6486f96, contestId=619650b3e1df502ae6486f96, betId=2147607982, accountName=ld_Gouth1, transactionId=300079888214760798288647, reason=Wallet status is SUCCESS, source=LCG, campaignType=5ASIDE, communicationStatus={OVERLAY=SUCCESS, TOASTER=SUCCESS, INBOX=SUCCESS}, rewardType=OB_FREEBET, rewardStatus=SUCCESS, errorCode=0)
        """
        pass

    def test_003_now_verify_the_excluding_positions_in_cms_if_they_have_prizes_from_that_are_excluded_in_prize_manager(self):
        """
        DESCRIPTION: Now verify the excluding positions in CMS, if they have prizes from that are excluded in Prize manager.
        EXPECTED: The prizes from the excluded positions should not have a request or response in Kibana.
        EXPECTED: For example :
        EXPECTED: Cash 100 : 1-10,*5
        EXPECTED: In the above case, for position 5, cash 100 request or response should not be seen n Kibana.
        """
        pass
