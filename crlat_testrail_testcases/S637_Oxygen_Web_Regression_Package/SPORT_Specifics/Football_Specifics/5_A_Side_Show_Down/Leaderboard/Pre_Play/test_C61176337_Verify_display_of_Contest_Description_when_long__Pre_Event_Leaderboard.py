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
class Test_C61176337_Verify_display_of_Contest_Description_when_long__Pre_Event_Leaderboard(Common):
    """
    TR_ID: C61176337
    NAME: Verify display of Contest Description when long - Pre-Event Leaderboard
    DESCRIPTION: This test case verifies the display of Leaderboard Content when the event is Pre-Play
    DESCRIPTION: Header Area
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User has placed 5-A Side bet successfully
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Item Label: FAQs
    PRECONDITIONS: Path: /five-a-side-showdown/faq
    PRECONDITIONS: Item Label: Terms & Conditions
    PRECONDITIONS: Path: /five-a-side-showdown/terms-and-conditions
    PRECONDITIONS: **Contest Criteria**
    PRECONDITIONS: 1: Contest should be created in CMS
    PRECONDITIONS: 2: 5-A Side Event ID should be configured for the Contest
    PRECONDITIONS: 3: Event should not Start (Can be future event)
    PRECONDITIONS: 4: Contest Description should be configured in CMS
    PRECONDITIONS: 5: Start Date in CMS should be same as Event Start Date in OB
    PRECONDITIONS: **Asset Management**
    PRECONDITIONS: 1: Team Flags can be configured in CMS > BYB > ASSET MANAGEMENT (Images can be added)
    PRECONDITIONS: 2: Both Teams flag Images should be configured in CMS - To display in Header Area (BMA-58158) https://jira.egalacoral.com/browse/BMA-58158
    PRECONDITIONS: **To Qualify for Showdown**
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    """
    keep_browser_open = True

    def test_001_navigate_to_leaderboard_when_the_event_is_pre_play(self):
        """
        DESCRIPTION: Navigate to Leaderboard when the event is Pre-play
        EXPECTED: User should be navigated to Leaderboard when the event is Pre-Paly
        """
        pass

    def test_002_verify_the_content_in_leaderboard_when_the_event_pre_play(self):
        """
        DESCRIPTION: Verify the content in Leaderboard when the event Pre-Play
        EXPECTED: * User should be displayed with the below details:
        EXPECTED: * Header Area
        EXPECTED: * Entry Area
        EXPECTED: * Prize Pool Breakdown
        EXPECTED: * Entry Information
        """
        pass

    def test_003_verify_the_position_of_header_area_in_leaderboard_when_the_event_pre_play(self):
        """
        DESCRIPTION: Verify the position of Header area in Leaderboard when the event Pre-Play
        EXPECTED: * Header area should be displayed at top of the page with the below contents
        EXPECTED: * Contest Description - This is pulled from the 'Description' field from CMS
        EXPECTED: * Event Start - This is pulled from 'Event Date' indicating when that event starts. IF event starts on that day, show countdown clock HH:MM format with clock counting down every minute. IF event does not start on that day, show date/time
        EXPECTED: If event starts today
        EXPECTED: KO In : HH:MM
        EXPECTED: If event starts in Future
        EXPECTED: 14:00 12th June 2021
        EXPECTED: * Logo - This is uploaded in the Image Manager
        EXPECTED: * Background - Green grassy background to the header (please view styles in terms of shadows and gradients)
        EXPECTED: * Teams Playing - The two teams playing and their associated images from the asset manager. (Text stacks if team name is too long)
        EXPECTED: Follows BMA-58158 (Asset Management) logic
        EXPECTED: Desktop Design
        EXPECTED: ![](index.php?/attachments/get/140133625)
        EXPECTED: Mobile Design
        EXPECTED: ![](index.php?/attachments/get/140133631)
        """
        pass

    def test_004__verify_the_description_of_header_area_when_description_is_long__configured_in_cms__contest_details_page__description__enter_long_text_in_the_description_field_and_click_on_save(self):
        """
        DESCRIPTION: * Verify the description of Header area (When description is long)
        DESCRIPTION: *  [Configured in CMS > Contest Details page > 'Description']
        DESCRIPTION: *  Enter long text in the Description field and click on save
        EXPECTED: Contest Description should be truncated and it should not flow into Event Date
        """
        pass
