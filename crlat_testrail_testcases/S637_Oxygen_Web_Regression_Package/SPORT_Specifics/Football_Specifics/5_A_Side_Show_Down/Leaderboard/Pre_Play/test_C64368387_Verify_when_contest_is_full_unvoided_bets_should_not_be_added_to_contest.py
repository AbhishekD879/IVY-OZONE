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
class Test_C64368387_Verify_when_contest_is_full_unvoided_bets_should_not_be_added_to_contest(Common):
    """
    TR_ID: C64368387
    NAME: Verify when contest is full, unvoided bets should not be added to contest.
    DESCRIPTION: This test case verifies the unvoiding of bets, when contest is full
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

    def test_001_navigate_to_pre_leaderboard_and_verify_voided_playersnote__few_bets_should_be_placed_on_both_teams_playersnow_place_more_bets_on_the_contest_so_that_the_contest_is_full(self):
        """
        DESCRIPTION: Navigate to pre-leaderboard and verify voided players.
        DESCRIPTION: Note : Few bets should be placed on both teams players.
        DESCRIPTION: Now place more bets on the contest, so that the contest is full.
        EXPECTED: Voided players entries should be removed.
        EXPECTED: Contest is full and no teams can be entered into the contest.
        """
        pass

    def test_002_modify_line_upsmodifying_line_ups_is_only_possible_in_test0_add_players_whose_bets_are_voided_previouslynote__line_ups_should_be_received_where_there_are_changes_with_player_dataexample_1st_line_upsabcdefghiuvxyz_player_bets_are_voided_in_the_above_case2nd_line_upsabcdefghiuvxyz(self):
        """
        DESCRIPTION: Modify line ups(modifying line-ups is only possible in test0), add players whose bets are voided previously
        DESCRIPTION: Note : Line-ups should be received where there are changes with player data.
        DESCRIPTION: Example :
        DESCRIPTION: 1st line ups:
        DESCRIPTION: A,B,C,D,E,F,G,H,I......
        DESCRIPTION: (U,V,X,Y,Z player bets are voided in the above case)
        DESCRIPTION: 2nd line-ups:
        DESCRIPTION: A,B,C,D,E,F,G,H,I,U,V,X,Y,Z
        EXPECTED: Unvoiding process should not be triggered as the contest size is full.
        EXPECTED: Check the below strings in Kibana
        EXPECTED: "5AShowdown Un-Voided entrei EventId"
        EXPECTED: should not return anything
        EXPECTED: "5AShowdown UN-VOIDING contest is full EventId"
        EXPECTED: return data when contest if full and unvoiding did not happen.
        """
        pass
