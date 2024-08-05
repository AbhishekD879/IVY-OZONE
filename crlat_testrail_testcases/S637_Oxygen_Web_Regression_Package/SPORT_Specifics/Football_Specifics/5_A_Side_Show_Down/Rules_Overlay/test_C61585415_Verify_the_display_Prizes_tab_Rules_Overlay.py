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
class Test_C61585415_Verify_the_display_Prizes_tab_Rules_Overlay(Common):
    """
    TR_ID: C61585415
    NAME: Verify the display Prizes tab Rules Overlay
    DESCRIPTION: This Test case verifies the display of Rules section in 5 -A Side Showdown
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

    def test_001_launch_ladbrokes(self):
        """
        DESCRIPTION: Launch Ladbrokes
        EXPECTED: User should be able to access the Ladbrokes application
        """
        pass

    def test_002_navigate_to_leaderboard_page(self):
        """
        DESCRIPTION: Navigate to Leaderboard page
        EXPECTED: User should be navigated to Leaderboard page
        """
        pass

    def test_003_verify_the_display_of_rules_button(self):
        """
        DESCRIPTION: Verify the display of Rules button
        EXPECTED: User should be able to view the Rules button as per the Designs
        """
        pass

    def test_004_click_on_rules_button(self):
        """
        DESCRIPTION: Click on Rules button
        EXPECTED: * Rules overlay should be displayed
        """
        pass

    def test_005_verify_the_display_of_header_and_blurb_in_rules_overlay(self):
        """
        DESCRIPTION: Verify the display of Header and Blurb in Rules overlay
        EXPECTED: * 5-A Side Logo should be displayed ( Uploaded in Image Manager)
        EXPECTED: * Teams Playing should be displayed - The two teams playing and their associated images from the asset manager. (Text stacks if team name is too long)
        EXPECTED: Follows BMA-58158 (Asset Management) logic
        EXPECTED: * Green grassy background should be displayed to the header (please view styles in terms of shadows and gradients)
        EXPECTED: * Title should be displayed as  '5-A-Side Showdown' header
        EXPECTED: * Game blurb should be displayed as configured in CMS (CMS > Contest Details page > 'Blurb' ) (it can be multiple lines)
        EXPECTED: * Rules Icons and Text should be displayed as configured in CMS and displayed in a list
        EXPECTED: ![](index.php?/attachments/get/134285632)
        """
        pass

    def test_006_verify_the_prizes_tab(self):
        """
        DESCRIPTION: Verify the **Prizes** Tab
        EXPECTED: * Pay Table information should be displayed as on Pre-Event Leaderboard
        EXPECTED: * Prizes tab should be the default tab
        EXPECTED: Click on Prize tab
        EXPECTED: * Prize tab should be GA tagged
        """
        pass

    def test_007_validate_cms_configurations_for_faqs_and_tcs(self):
        """
        DESCRIPTION: Validate CMS configurations for **FAQs** and **T&Cs**
        EXPECTED: * Rules section should be displayed under 5-A-Side Showdown Tab
        EXPECTED: * FAQs section should be displayed where content user can
        EXPECTED: * Create Questions and add rich text
        EXPECTED: * Create Answers related to the Questions and add rich text
        EXPECTED: * Edit and Delete Questions and Answers
        EXPECTED: * Set priority order of these Questions
        EXPECTED: * Terms & Conditions should be displayed that has a single rich text box for content user to add rules text
        """
        pass

    def test_008_verify_the_faqs_tab(self):
        """
        DESCRIPTION: Verify the **FAQs** Tab
        EXPECTED: * Click on FAQs tab
        EXPECTED: * FAQs should be displayed as configured in CMS(5-A Side Showdown > FAQs)
        EXPECTED: * FAQs order should be as set in CMS
        EXPECTED: * All FAQs should be collapsed and on clicking any FAQ drop down arrow it should be expanded and answer should be displayed as configured in CMS
        EXPECTED: * FAQs tab should be GA tagged
        """
        pass

    def test_009_verify_the_tcs_tab(self):
        """
        DESCRIPTION: Verify the **T&Cs** tab
        EXPECTED: * T&Cs should be displayed as configured in CMS
        EXPECTED: * T&Cs tab should be GA tagged
        """
        pass

    def test_010_click_on_close_button(self):
        """
        DESCRIPTION: Click on **Close** button
        EXPECTED: * Overlay should be closed
        EXPECTED: * User should remain on page prior to opening the Rules overlay
        """
        pass
