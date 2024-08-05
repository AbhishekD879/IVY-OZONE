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
class Test_C61497016_Verify_the_display_of_Showdown_Cards_when_event_start_Today_Tomorrow_Future(Common):
    """
    TR_ID: C61497016
    NAME: Verify the display of Showdown Cards when event start Today/Tomorrow/Future.
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

    def test_004_verify_the_details_displayed_on_showdown_cards(self):
        """
        DESCRIPTION: Verify the details displayed on Showdown Cards
        EXPECTED: * Title of the Showdown Contest should be displayed
        EXPECTED: Contest Header – 'Icon' and 'Name' fields configured in CMS Contest details should be displayed
        EXPECTED: * Entry Fee should be displayed in £
        EXPECTED: 'Entry Stake'  configured in CMS Contest details should be displayed.
        EXPECTED: * '+' should be displayed after the stake.
        EXPECTED: * Prize Pool Total - 'Cash' field configured in CMS > Prize Pool should be displayed.
        EXPECTED: *Total represents how much total money can be won*
        EXPECTED: * Team Names should be displayed and Team flags should be displayed (Team Flags as configured in CMS > Asset Management)
        EXPECTED: Follows BMA-58158 (Asset Management) logic
        EXPECTED: * Scores should be displayed and updated dynamically when Event is Live
        EXPECTED: *score format should be same throughout the rest of the app ( ET and Penalties scenarios should be considered)*
        EXPECTED: * Event Sponsor should be displayed - If 'Sponsor Text' and 'Sponsor Logo' are configured in CMS.
        EXPECTED: * Maximum 3 Labels should be displayed on the Showdown card from the below CMS configurations following priority order as given
        EXPECTED: * Extra - "Summary" field in Prize Pool Total
        EXPECTED: * Entries in Contest - [Dynamic count of Entries already in contest]/ "Size" field in Contest Details
        EXPECTED: * Total Prizes - "Number of Prizes" field in Prize Pool Total
        EXPECTED: * Max Entries Per Customer - "Teams" field in Contest Details
        EXPECTED: * First Prize - "First Place" field in Prize Pool
        EXPECTED: * Total Vouchers - "Vouchers" field in Prize Pool
        EXPECTED: * Total Tickets - "Tickets" field in Prize Pool
        EXPECTED: * Total Free Bets - "Free Bets" field in Prize Pool
        EXPECTED: ![](index.php?/attachments/get/161000205)
        EXPECTED: ![](index.php?/attachments/get/130937057)
        """
        pass

    def test_005_verify_the_different_states_of_showdown_cards_where_the_event_starts__todaytomorrowfuture(self):
        """
        DESCRIPTION: Verify the different states of Showdown cards where the event starts  Today/Tomorrow/Future.
        EXPECTED: **PRE-EVENT**
        EXPECTED: * Event has not started then showdown card displayed is in Pre-event State
        EXPECTED: ![](index.php?/attachments/get/161000206)
        EXPECTED: Note : Ticket is descoped on the card.
        """
        pass

    def test_006_verify_the_date__time_display(self):
        """
        DESCRIPTION: Verify the date & Time display
        EXPECTED: **Today/TOMORROW/FUTURE DATE**
        EXPECTED: * When Event is not yet started but scheduled for Today
        EXPECTED: its should be displayed under Today Tab and Date/Time should be displayed as countdown timer 'KICK OFF HH/MM' that ticks down (When event starts within 24hrs its will show 'Starts In HH/MM')
        EXPECTED: ![](index.php?/attachments/get/161000206)
        """
        pass

    def test_007_tap_on_showdown_card(self):
        """
        DESCRIPTION: Tap on Showdown Card
        EXPECTED: * User should be redirected to Leaderboard
        EXPECTED: * Click on showdown card should be GA tracked
        """
        pass
