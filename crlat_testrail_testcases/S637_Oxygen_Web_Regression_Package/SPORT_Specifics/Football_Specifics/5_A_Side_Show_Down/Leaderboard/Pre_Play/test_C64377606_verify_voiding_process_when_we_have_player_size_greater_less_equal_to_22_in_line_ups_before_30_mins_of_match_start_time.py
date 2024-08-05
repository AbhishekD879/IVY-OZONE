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
class Test_C64377606_verify_voiding_process_when_we_have_player_size_greater_less_equal_to_22_in_line_ups_before_30_mins_of_match_start_time(Common):
    """
    TR_ID: C64377606
    NAME: verify voiding process when we have player size greater/less/equal to 22 in line-ups before 30 mins of match start time.
    DESCRIPTION: Bets will be voided when we have line-ups greater than, lesser than, equal to 22.
    DESCRIPTION: Bets will not be voided when we received player size : 0
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User's 5-A Side bets should enter into Showdown
    PRECONDITIONS: 4: Event should be in Pre-Play
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Item Label: FAQs
    PRECONDITIONS: Path: /five-a-side-showdown/faq
    PRECONDITIONS: Item Label: Terms & Conditions
    PRECONDITIONS: Path: /five-a-side-showdown/terms-and-conditions
    PRECONDITIONS: Contest Criteria
    PRECONDITIONS: 1: Contest should be created in CMS
    PRECONDITIONS: 2: 5-A Side Event ID should be configured for the Contest
    PRECONDITIONS: 3: Event should not Start (Can be future event)
    PRECONDITIONS: 4: Contest Description should be configured in CMS
    PRECONDITIONS: 5: Start Date in CMS should be same as Event Start Date in OB
    PRECONDITIONS: Asset Management
    PRECONDITIONS: 1: Team Flags can be configured in CMS &gt; BYB &gt; ASSET MANAGEMENT (Images can be added)
    PRECONDITIONS: 2: Both Teams flag Images should be configured in CMS - To display in Header Area (BMA-58158) https://jira.egalacoral.com/browse/BMA-58158
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    PRECONDITIONS: Unvoiding process:
    PRECONDITIONS: When there is change in line-ups, in such cases few bets which are supposed to be unvoided will be added back to the contest
    """
    keep_browser_open = True

    def test_001_verify_the_count_of_player_size_in_line_up_in_kibana_using_the_below_string5ashowdown_players_list_from_banach_eventidvoiding_process_should_be_triggered_when_we_have_player_size_greater_than_less_than_or_equal_to_22(self):
        """
        DESCRIPTION: Verify the count of player size in line-up in kibana using the below string
        DESCRIPTION: "5AShowdown players list from banach EventId"
        DESCRIPTION: Voiding process should be triggered when we have player size greater than, less than or equal to 22.
        EXPECTED: Bets should be voided and removed from Leaderboard
        EXPECTED: Bets will be voided only before 30 mins of start time of match in Leaderboard.
        """
        pass

    def test_002_verify_the_voiding_process_when_player_size_is_0(self):
        """
        DESCRIPTION: Verify the voiding process when player size is 0
        EXPECTED: Bets will not be voided.
        """
        pass
