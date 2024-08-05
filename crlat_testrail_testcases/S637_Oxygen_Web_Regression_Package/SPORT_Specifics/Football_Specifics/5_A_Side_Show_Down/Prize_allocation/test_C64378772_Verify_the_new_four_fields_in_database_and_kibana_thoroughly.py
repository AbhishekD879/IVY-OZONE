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
class Test_C64378772_Verify_the_new_four_fields_in_database_and_kibana_thoroughly(Common):
    """
    TR_ID: C64378772
    NAME: Verify the new four fields in database and kibana thoroughly
    DESCRIPTION: 
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

    def test_001_login_to_sportsbook_with_user_that_satisfies_pre_conditions(self):
        """
        DESCRIPTION: Login to sportsbook with user that satisfies pre conditions
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_the_contest_which_has_different_prize_combinations_created_as_per_pre_conditions_and_place_bets(self):
        """
        DESCRIPTION: Navigate to the contest Which has different prize combinations created as per pre conditions and place bets
        EXPECTED: User should be able to navigate to contest specified in preconditions and place bets successfully
        """
        pass

    def test_003_make_the_contest_live_and_navigate_to_live_leaderboard(self):
        """
        DESCRIPTION: Make the contest live and Navigate to live leaderboard
        EXPECTED: User should be navigated to LLB
        """
        pass

    def test_004_send_ertwhich_is_replay_incident___replay_stat_in_tst0_wait_until_event_is_finishedhlv0(self):
        """
        DESCRIPTION: Send ERT(which is replay incident _ replay stat in tst0)/ wait until event is finished(hlv0)
        EXPECTED: ERT should be received
        """
        pass

    def test_005_from_the_time_ert_sent_after_10_min_send_1_more_stat_in_tst0_observe_header_is_receivedverify_using_validate_header_flag_string_in_kibana(self):
        """
        DESCRIPTION: From the time ERT sent after 10 min, (send 1 more stat in tst0) observe header is received
        DESCRIPTION: Verify using "Validate header flag" string in kibana
        EXPECTED: Header should be true in kibana for that event
        """
        pass

    def test_006_send_1_more_stat_from_post_man(self):
        """
        DESCRIPTION: Send 1 more stat from post man
        EXPECTED: stat should be sent
        """
        pass

    def test_007_observe_stats_is_not_consumed(self):
        """
        DESCRIPTION: Observe stats is not consumed
        EXPECTED: Stats should not be consumed
        """
        pass

    def test_008_verify_whether_the_prize_allocation_is_done_after_ertplus10_automatically(self):
        """
        DESCRIPTION: Verify whether the prize allocation is done after ERT+10 automatically
        EXPECTED: Prize allocation should be done after ERT+10 automatically
        """
        pass

    def test_009_check_whether_kibana_shows_appropriate_success_requests_for_all_the_prizes_below_are_the_strings_to_search5ashowdown_crm_publish_for_unique_request_id5ashowdown_crm_consumed_for_unique_request_id5ashowdown_started_postmatch_process_for(self):
        """
        DESCRIPTION: Check whether kibana shows appropriate success requests for all the prizes. Below are the strings to search
        DESCRIPTION: "5AShowdown CRM publish for unique request id"
        DESCRIPTION: "5AShowdown CRM consumed for unique request id"
        DESCRIPTION: "5AShowdown started postmatch process for"
        EXPECTED: Kibana should show success requests for all the prizes in publish and consume string
        """
        pass

    def test_010_check_the_below_fields_for_all_the_responses_in_5ashowdown_crm_consumed_for_unique_request_id_string1_transaction_id2_reward_status3_reason4_error_code(self):
        """
        DESCRIPTION: Check the below fields for all the responses in "5AShowdown CRM consumed for unique request id" string
        DESCRIPTION: 1. Transaction Id
        DESCRIPTION: 2. Reward Status
        DESCRIPTION: 3. Reason
        DESCRIPTION: 4. Error code
        EXPECTED: All the four fields should be correct and transaction id shouldn't be duplicated.
        """
        pass
