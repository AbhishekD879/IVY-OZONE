import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.5_a_side
@vtest
class Test_C62700694_Verify_the_behaviour_of_invitational_contest_when_same_event_has_multiple_contests(Common):
    """
    TR_ID: C62700694
    NAME: Verify the behaviour of invitational contest when same event has multiple contests
    DESCRIPTION: This test case verifies the behaviour of the contest when disabled invitation toggle
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Contest should be created in CMS
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
    PRECONDITIONS: Set up 5 or more contests in CMS as metioned above with same event ID,out of them few should be invitational contest.
    PRECONDITIONS: User should place bets on all the contests created for the same event ID.
    PRECONDITIONS: How to enter team into a Invitational contest :
    PRECONDITIONS: 1. Navigate to CMS, Standard Leaderboard URL will be available in the contest created.
    PRECONDITIONS: 2. Copy the Standard Leaderboard URL and navgate through it.
    PRECONDITIONS: 3. User will be navigated to Pre- Leaderboard (if the event is not yet started).
    PRECONDITIONS: 4. Click on build team(will be available when logged in) and build a team and place bet will elligible stake.
    PRECONDITIONS: 5. Entry confirmation message is available and the team is entered into the contest.
    """
    keep_browser_open = True

    def test_001_1_login_to_fe_ladbrokes_application(self):
        """
        DESCRIPTION: 1. Login to FE Ladbrokes application
        EXPECTED: 1. User should be able to login successfully
        """
        pass

    def test_002_2_click_on_5_a_side_leader_board_button_on_my_bets_for_the_above_mentioned_event_bets_placing_mentioned_in_pre_conditions(self):
        """
        DESCRIPTION: 2. Click on '5-A Side leader board' button on My bets for the above mentioned event. (Bets placing mentioned in Pre-conditions)
        EXPECTED: 2. User will be navigated to Pre-leader board of that particular event.
        """
        pass

    def test_003_3_click_on_return_to_lobby_cta(self):
        """
        DESCRIPTION: 3. Click on "Return to Lobby" CTA
        EXPECTED: 3. User will be navigated back to lobby, with all the eligible showdown cards(contests) in lobby displayed according to the CMS priority.
        """
        pass

    def test_004_4_verify_the_contests_created_for_the_same_event_as_mention_in_pre_conditions(self):
        """
        DESCRIPTION: 4. Verify the contests created for the same event as mention in Pre-conditions
        EXPECTED: 4. As user placed bets on all the contests for the event, all the contests are displayed in Lobby.
        """
        pass

    def test_005_navigate_to_each_contest_and_verify_all_the_leaderboards_in_prelivepost_states(self):
        """
        DESCRIPTION: Navigate to each contest and verify all the leaderboards in Pre/Live/Post states.
        EXPECTED: All the contests should load properly in Pre/Live/Post states.
        EXPECTED: Pre-Leaderboard:
        EXPECTED: 1. User should be displayed with the below details:
        EXPECTED: * Header Area
        EXPECTED: * Entry Area
        EXPECTED: * Prize Pool Breakdown
        EXPECTED: * Entry Information
        EXPECTED: Header area should be displayed at top of the page with the below contents
        EXPECTED: Contest Description - This is pulled from the Description' field from CMS
        EXPECTED: Event Start - This is pulled from 'Event Date' indicating when that event starts. IF event starts on that day, show countdown clock HH:MM format with clock counting down every minute.
        EXPECTED: IF event does not start on that day, show date/time If event starts today KO In : HH:MM
        EXPECTED: If event starts in Future 14:00 12th June 2021
        EXPECTED: Logo - 5-A Side logo should be displayed
        EXPECTED: Background - Green grassy background to the header (please view styles in terms of shadows and gradients) or If image is uploaded in contest level.
        EXPECTED: Teams Playing - The two teams playing and their associated images.
        EXPECTED: * My Entry should be displayed
        EXPECTED: * User Entry should be displayed
        EXPECTED: * Position should be displayed as 1
        EXPECTED: * Progress bar should be displayed as 0%
        EXPECTED: * Username should be displayed with last three characters marked as ***
        EXPECTED: * Price /Odds should be displayed @2/1 below Username
        EXPECTED: Live- Leaderboard:
        EXPECTED: User should be displayed Leaderboard
        EXPECTED: Leaderboard should be displayed showing the leading entries in the contest
        EXPECTED: Header text should be Leaderboard Top [X]' where X = 100
        EXPECTED: Below should be displayed for the entries,
        EXPECTED: * Position and Image - Image pulled from CMS &gt; Image
        EXPECTED: Manager
        EXPECTED: * Username
        EXPECTED: * Odds
        EXPECTED: * Prize and Signposting
        EXPECTED: * Progress bar
        EXPECTED: Username of the user who the entry belongs to should be displayed
        EXPECTED: Username should be truncated and displayed with last three characters replaced by ***
        EXPECTED: User should be able to view the progress bar and % indicating the progress of the bet as per the Progress Logic
        EXPECTED: Progress bar should be updated dynamically as per the update rules
        EXPECTED: Prize Information should be displayed
        EXPECTED: Signposting should be displayed
        EXPECTED: If two or more entries are tied then the Prizes will be split based on the tie logic
        EXPECTED: Post-Leaderboard:
        EXPECTED: The following should be displayed when event is completed Live-Event Leaderboard changes to Post-Event Leaderboard.
        EXPECTED: * Header Area
        EXPECTED: * Rules
        EXPECTED: * My Entries Widget
        EXPECTED: * Leaderboard with Entries
        EXPECTED: * Leaderboard is available to view and customers can interact with it as per normal, but live updates are no longer required and can be switched off 15 minutes after the event is complete
        EXPECTED: * Contest Description - This is pulled from the 'Description' field (It should truncate if flows into Event Date)
        EXPECTED: * Logo - This is uploaded in the Image Manager
        EXPECTED: * Background - Green grassy background to the header (please view styles in terms of shadows and gradients)
        EXPECTED: * Teams Playing - The two teams playing and their associated images from the asset manager. (Text stacks if team name is too long)
        EXPECTED: * Final Score - This is the final score in the match.
        EXPECTED: NOTE: If match goes to Penalties then Score line should reflect the score at the end of extra time.
        EXPECTED: * Full Time - Clear signposting of 'Full Time' indicating that the event is over
        EXPECTED: * Header area should be collapsed and remains sticky
        EXPECTED: NOTE: Same behaviour as Live Leaderboard
        EXPECTED: Rules button should be displayed as per designs
        EXPECTED: On tapping Rules button, Rules overlay should be opened
        EXPECTED: * Leaderboard should be displayed showing the leading entries in the contest along with the prizes
        EXPECTED: * Display limit rules are still followed
        EXPECTED: * Team summary should be displayed on tapping on each entry
        EXPECTED: My Entry or My Entries widget should be displayed
        EXPECTED: * ALL the customer's teams should be stacked in order of finishing position with prizes at right most side like in LB for each entry
        EXPECTED: User should be able to Expand teams as per leaderboard
        EXPECTED: * Positions summary widget should be displayed
        """
        pass
