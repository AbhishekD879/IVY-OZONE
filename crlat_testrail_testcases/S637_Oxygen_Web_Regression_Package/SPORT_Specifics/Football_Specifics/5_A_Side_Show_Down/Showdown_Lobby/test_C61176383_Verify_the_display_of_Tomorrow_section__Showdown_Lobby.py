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
class Test_C61176383_Verify_the_display_of_Tomorrow_section__Showdown_Lobby(Common):
    """
    TR_ID: C61176383
    NAME: Verify the display of Tomorrow section - Showdown Lobby
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
        EXPECTED: * Title should be displayed as "5-A-Side Showdown"
        """
        pass

    def test_004_verify_the_banner_displaybanner_carousel_is_toggled_onindexphpattachmentsget130405367(self):
        """
        DESCRIPTION: Verify the Banner display
        DESCRIPTION: **Banner Carousel is toggled ON**
        DESCRIPTION: ![](index.php?/attachments/get/130405367)
        EXPECTED: * Banner Carousel should be displayed at the top of the page
        """
        pass

    def test_005_verify_the_display_of_show_down_cards_with_tomorrows_dateshould_verify_with_ukgibraltar__vienna_time_zones_set_in_systemuser_did_not_enter_into_any_showdown_contestindexphpattachmentsget161000150(self):
        """
        DESCRIPTION: Verify the display of Show Down Cards with Tomorrow's date.
        DESCRIPTION: Should verify with UK,Gibraltar & Vienna time zones set in system.
        DESCRIPTION: **User did not enter into any Showdown Contest**
        DESCRIPTION: ![](index.php?/attachments/get/161000150)
        EXPECTED: * A list of 'Showdown Cards' of all contests created in the manager that are marked as 'Display = Yes'.
        EXPECTED: * Each day should have it's own section
        EXPECTED: IF Showdown Date is tomorrow = "Tomorrow"
        EXPECTED: **Footer Links**
        EXPECTED: *  Footer links are displayed at the foot of the page, configured in the CMS
        EXPECTED: * T&C's footer link and tutorial links should be GA tracked
        """
        pass

    def test_006_verify_the_display_of_showdown_cardwhen_contest_is_configured_in_cms_to_display__no(self):
        """
        DESCRIPTION: Verify the display of Showdown card
        DESCRIPTION: **when Contest is configured in CMS to Display = NO**
        EXPECTED: * Showdown card should no longer be displayed
        """
        pass

    def test_007_verify_the_display_of_showdown_cards_as_per_test_account_handling_bma_59539(self):
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
