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
class Test_C61497017_Verify_the_display_of_Showdown_Cards_when_event_is_in_Last_7_days_section(Common):
    """
    TR_ID: C61497017
    NAME: Verify the display of Showdown Cards when event is in Last 7 days section.
    DESCRIPTION: This test case verifies the display of Showdown Cards
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Contest should be created in CMS
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
        EXPECTED: User should be navigated to Showdown Lobby
        """
        pass

    def test_003_verify_the_display_of_showdown_lobby(self):
        """
        DESCRIPTION: Verify the display of Showdown Lobby
        EXPECTED: * Banner Carousal should be displayed (If available from Sitecore)
        EXPECTED: * Showdown Cards should be displayed
        """
        pass

    def test_004_verify_the_details_displayed_on_showdown_cards_in_last_7_days_section(self):
        """
        DESCRIPTION: Verify the details displayed on Showdown Cards in Last 7 Days section.
        EXPECTED: * Title of the Showdown Contest should be displayed
        EXPECTED: Contest Header – 'Icon' and 'Name' fields configured in CMS Contest details should be displayed
        EXPECTED: * Team Names should be displayed and Team flags should be displayed (Team Flags as configured in CMS > Asset Management)
        EXPECTED: Follows BMA-58158 (Asset Management) logic
        EXPECTED: * Final Scores should be displayed and updated
        EXPECTED: * Event Sponsor should be displayed - If 'Sponsor Text' and 'Sponsor Logo' are configured in CMS.
        EXPECTED: * FT label should be shown.
        EXPECTED: ![](index.php?/attachments/get/150065388)
        EXPECTED: Note : "You won" has been descoped.
        """
        pass

    def test_005_verify_the_different_states_of_showdown_cards(self):
        """
        DESCRIPTION: Verify the different states of Showdown cards
        EXPECTED: **POST Event**
        EXPECTED: * Event has finished then showdown card displayed is in Post Event state
        EXPECTED: ![](index.php?/attachments/get/130937060)
        """
        pass

    def test_006_verify_the_date__time_display(self):
        """
        DESCRIPTION: Verify the date & Time display
        EXPECTED: **Last 7 Days**
        EXPECTED: * Display = Yes is configured in CMS for the Contest
        EXPECTED: * When Event has finished/ completed Showdown Card should be displayed in Last 7 Days section
        EXPECTED: * Date/Time should be displayed as '15th June 2020'
        EXPECTED: ![](index.php?/attachments/get/130937061)
        """
        pass

    def test_007_tap_on_showdown_card(self):
        """
        DESCRIPTION: Tap on Showdown Card
        EXPECTED: * User should be redirected to Leaderboard
        EXPECTED: * Click on showdown card should be GA tracked
        """
        pass
