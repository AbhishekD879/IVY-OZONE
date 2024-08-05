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
class Test_C61619050_Verify_the_display_of_Free_Bet_Prizes_in_Pre_Event_Leaderboard__Prize_pool_information(Common):
    """
    TR_ID: C61619050
    NAME: Verify the display of Free Bet Prizes in Pre-Event Leaderboard - Prize pool information
    DESCRIPTION: This test case verifies the display of Free Bet Prizes in Pre-Event Leaderboard
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
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

    def test_002_navigate_to_5_a_side_showdown__contest__leaderboard(self):
        """
        DESCRIPTION: Navigate to 5-A Side showdown > Contest > Leaderboard
        EXPECTED: User should be navigated to Leaderboard page
        """
        pass

    def test_003_verify_the_display_of_prize_pool_information_when_prizes_are_added_configured_in_cmscms_configurations_cash_field_should_be_updated_in_cms__5_a_side_showdown__contest_details_page__add_a_prize_prizes_should_be_configured_in_pay_table(self):
        """
        DESCRIPTION: Verify the display of Prize pool information when prizes are added /configured in CMS
        DESCRIPTION: **CMS Configurations:**
        DESCRIPTION: * Cash field should be updated in CMS > 5-A Side showdown > Contest Details page > Add a Prize
        DESCRIPTION: * Prizes should be configured in Pay Table
        EXPECTED: * Two Columns should be displayed
        EXPECTED: * Column 1 - Position (Single position or could be a range)
        EXPECTED: * Column 2 - Prize Information (See below display logic)
        EXPECTED: * Prizes should be displayed in order as they are configured in the CMS
        EXPECTED: ![](index.php?/attachments/get/130523319)
        EXPECTED: **Multiple prizes per position**
        EXPECTED: * "+" should be used to split them up and use CMS order to guide priority
        EXPECTED: ![](index.php?/attachments/get/130523318)
        """
        pass

    def test_004_verify_the_display_of_prize_information_when_the_below_is_configured_in_cmscms_configurations_prize_type__free_bet_prize_signposting___image_uploaded_prize_name__prize_value_or_both___configured(self):
        """
        DESCRIPTION: Verify the display of prize information when the below is configured in CMS
        DESCRIPTION: **CMS Configurations**
        DESCRIPTION: * 'Prize Type' = "Free Bet"
        DESCRIPTION: * Prize signposting - Image Uploaded
        DESCRIPTION: * 'Prize Name' / 'Prize Value' or both - configured
        EXPECTED: **ONLY PRIZE VALUE**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * 'Prize Value' in **£** should be displayed with
        EXPECTED: **Free Bet**
        EXPECTED: **PRIZE VALUE & Prize signposting**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * 'Prize Value' in **£** should be displayed with **
        EXPECTED: Signposting and Free Bet**
        EXPECTED: **PRIZE VALUE & Prize NAME**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * Prize Name should be displayed
        EXPECTED: **PRIZE NAME & Prize signposting**
        EXPECTED: * Prize Name should be displayed
        EXPECTED: * Prize Name should be displayed followed by Prize
        EXPECTED: Signposting
        EXPECTED: **BOTH PRIZE VALUE , PRIZE NAME  & Prize signposting**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * Prize Name should be displayed
        EXPECTED: * Prize Name should also be followed by Prize Signposting
        """
        pass
