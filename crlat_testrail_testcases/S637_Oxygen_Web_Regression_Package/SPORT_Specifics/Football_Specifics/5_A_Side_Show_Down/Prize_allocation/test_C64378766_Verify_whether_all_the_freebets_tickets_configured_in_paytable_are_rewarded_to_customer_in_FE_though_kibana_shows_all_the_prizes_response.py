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
class Test_C64378766_Verify_whether_all_the_freebets_tickets_configured_in_paytable_are_rewarded_to_customer_in_FE_though_kibana_shows_all_the_prizes_response(Common):
    """
    TR_ID: C64378766
    NAME: Verify whether all the freebets/tickets configured in paytable are rewarded to customer in FE though kibana shows all the prizes response
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
        DESCRIPTION: Login to sportsbook with user that satisfies pre conditions.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_the_contest_which_has_different_prize_combinations_created_as_per_pre_conditions_place_bets(self):
        """
        DESCRIPTION: Navigate to the contest Which has different prize combinations created as per pre conditions, place bets.
        EXPECTED: User should be able to navigate to contest specified in preconditions and place bets successfully.
        """
        pass

    def test_003_in_cms_create_a_contest_with_prizes_which_has_configurations_with_excluding_positions_and_user_should_place_bets_on_the_contest(self):
        """
        DESCRIPTION: In CMS, create a contest with prizes which has configurations with excluding positions and User should place bets on the contest.
        EXPECTED: Prizes should be allocated in leaderboard as per configurations.
        """
        pass

    def test_004_make_the_contest_live_and_navigate_to_live_leaderboard(self):
        """
        DESCRIPTION: Make the contest live and Navigate to live leaderboard.
        EXPECTED: User should be navigated to LLB.
        """
        pass

    def test_005_send_stats_from_postman(self):
        """
        DESCRIPTION: Send Stats from Postman.
        EXPECTED: Stats should be sent successfully.
        """
        pass

    def test_006_make_sure_that_event_is_settled_in_ob(self):
        """
        DESCRIPTION: Make sure that event is settled in OB.
        EXPECTED: User should able to see Post LB.
        """
        pass

    def test_007_verify_weather_prizes_are_rewarded_as_per_cms_configcheck_whether_kibana_shows_appropriate_success_requests_for_all_the_prizes_below_are_the_strings_to_search5ashowdown_crm_publish_for_unique_request_id5ashowdown_crm_consumed_for_unique_request_id(self):
        """
        DESCRIPTION: Verify weather prizes are rewarded as per CMS config.
        DESCRIPTION: Check whether kibana shows appropriate success requests for all the prizes. Below are the strings to search
        DESCRIPTION: "5AShowdown CRM publish for unique request id"
        DESCRIPTION: "5AShowdown CRM consumed for unique request id"
        EXPECTED: Kibana should show success requests for all the prizes in publish and consume string
        """
        pass

    def test_008_verify_weather_prizes_are_configured_in_paytable_cms_are_allocated_to_users(self):
        """
        DESCRIPTION: Verify weather Prizes are configured in Paytable CMS are allocated to users.
        EXPECTED: User should be rewarded with the prizes as per the CMS configration.
        """
        pass
