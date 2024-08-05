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
class Test_C61667234_Verify_the_display_of_Showdown_Lobby(Common):
    """
    TR_ID: C61667234
    NAME: Verify the display of Showdown Lobby
    DESCRIPTION: This Test case verifies the display of Showdown Lobby with all the Contest details
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
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

    def test_001_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_5_a_side_showdown_lobby(self):
        """
        DESCRIPTION: Navigate to 5-A Side Showdown Lobby
        EXPECTED: * The page should have its own URL so can be linked to from quick links, banners, CRM etc.  '/5-a-side/lobby'
        EXPECTED: * Loading screen should be with 5-A-Side crest
        EXPECTED: * After 2 seconds (or however it takes to load) show open animation (see prototype and attached video)
        EXPECTED: * Showdown lobby content should be fully loaded
        EXPECTED: https://jira.egalacoral.com/secure/attachment/1607978/20210205_160239000_iOS_Trim.mp4
        """
        pass

    def test_003_verify_the_page_header_display(self):
        """
        DESCRIPTION: Verify the Page Header display
        EXPECTED: * Title should be displayed as "5-A-Side"
        """
        pass

    def test_004_verify_the_banner_displaybanner_carousel_is_toggled_onindexphpattachmentsget130405367(self):
        """
        DESCRIPTION: Verify the Banner display
        DESCRIPTION: **Banner Carousel is toggled ON**
        DESCRIPTION: ![](index.php?/attachments/get/130405367)
        EXPECTED: * Banner Carousel should be displayed at the top of the page
        EXPECTED: * Target banners and then default banners should show.
        """
        pass

    def test_005_verify_the_display_of_show_down_cardsuser_did_not_enter_into_any_showdown_contestindexphpattachmentsget161000131(self):
        """
        DESCRIPTION: Verify the display of Show Down Cards
        DESCRIPTION: **User did not enter into any Showdown Contest**
        DESCRIPTION: ![](index.php?/attachments/get/161000131)
        EXPECTED: * A list of 'Showdown Cards' of all contests created in the manager that are marked as 'Display = Yes'.
        EXPECTED: * Showdown Cards are split up by day
        EXPECTED: * Showdown contents must be upcoming or Live, completes.
        EXPECTED: * Each day should have it's own section
        EXPECTED: **NOTE:**
        EXPECTED: IF Showdown is today = "Today"
        EXPECTED: IF Showdown Date is tomorrow = "Tomorrow"
        EXPECTED: IF Showdown Date is further in the future = "Day / Month" e.g. Tuesday 23th Feb
        EXPECTED: **Last 7 Days**
        EXPECTED: * At least one Showdown Card is set to Display=YES in the CMS
        EXPECTED: * There should be a sub-section at the bottom of the lobby  titled 'Last 7 Days'
        EXPECTED: * Any Showdown Cards of contests that have completed in the last 7 days should be displayed underneath (The customer does not have had to enter).
        EXPECTED: * They should be in order of start date with the most recent at the top
        EXPECTED: **Footer Links**
        EXPECTED: *  Footer links are displayed at the foot of the page, configured in the CMS
        EXPECTED: * T&C's footer link and tutorial links should be GA tracked
        """
        pass

    def test_006_verify_the_display_of_my_leaderboarduser_has_entered_into_atleast_one_showdown_contestindexphpattachmentsget161000136(self):
        """
        DESCRIPTION: Verify the display of My Leaderboard
        DESCRIPTION: **User has entered into atleast one Showdown Contest**
        DESCRIPTION: ![](index.php?/attachments/get/161000136)
        EXPECTED: **My Leaderboard**
        EXPECTED: * User has entered one of these Showdowns
        EXPECTED: * There be a sub-section at the top of the lobby titled 'My Leaderboard(X)'
        EXPECTED: The number of Showdowns cards displayed in this area = (X)
        EXPECTED: * Showdown Cards that the customer has entered should be displayed in a list underneath
        EXPECTED: * They should be in order of ... LIVE, upcoming, completes.
        EXPECTED: In ascending order of Time.
        EXPECTED: *  When isSettled flag is true then the Showdown card should be removed from the My Showdowns area.
        EXPECTED: **NOTE:** If a Showdown Card is included in the My Showdown section it SHOULD ALSO be included in the regular list. It is expected to have duplicate Showdown cards here.
        """
        pass

    def test_007_verify_that_showdown_card_is_removed_from_my_leaderboardx_after_event_completion(self):
        """
        DESCRIPTION: Verify that Showdown Card is removed from My Leaderboard(X) after event completion
        EXPECTED: * Showdown Card should be removed from My Leaderboard(X) section and X should be also updated
        """
        pass

    def test_008_verify_the_display_of_showdown_cardwhen_contest_is_configured_in_cms_to_display__no(self):
        """
        DESCRIPTION: Verify the display of Showdown card
        DESCRIPTION: **when Contest is configured in CMS to Display = NO**
        EXPECTED: * Showdown card should no longer be displayed
        """
        pass

    def test_009_verify_the_display_of_showdown_cards_as_per_test_account_handling_bma_59539(self):
        """
        DESCRIPTION: Verify the display of Showdown Cards as per Test Account Handling (BMA-59539)
        EXPECTED: **Real Account Enabled**
        EXPECTED: * Showdown Card for that Contest is displayed to all User types (Real/Test) and also to logged out user
        EXPECTED: **Test Account Enabled**
        EXPECTED: * Showdown Card for that Contest is displayed to all ONLY Test User
        EXPECTED: * Logged out User - Card will not be displayed
        EXPECTED: * Real User- Card will not be displayed
        EXPECTED: **Real & Test Account Enabled**
        EXPECTED: * Showdown Card for that Contest is displayed to all User types (Real/Test) and also to logged out user
        """
        pass
