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
class Test_C60546381_Verify_the_display_of_Pre_Event_Leaderboard__Prize_pool_information(Common):
    """
    TR_ID: C60546381
    NAME: Verify the display of Pre-Event Leaderboard - Prize pool information
    DESCRIPTION: This test case verifies the display of Prize pool information on Pre-Event Leaderboard
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

    def test_003_verify_the_display_of_prize_pool_headercms_configurations_cash_field_should_be_updated_in_cms__5_a_side_showdown__contest_details_page__prize_pool(self):
        """
        DESCRIPTION: Verify the display of Prize Pool Header
        DESCRIPTION: **CMS Configurations:**
        DESCRIPTION: * Cash field should be updated in CMS > 5-A Side showdown > Contest Details page > Prize Pool
        EXPECTED: * User should be displayed with Prize Pool Grid
        EXPECTED: * Prize Pool header = "[Cash] Prize Pool" where  [Cash] is taken from the 'Cash' field in the Prize Manager
        EXPECTED: ![](index.php?/attachments/get/130523307)
        """
        pass

    def test_004_verify_the_display_of_prize_pool_information_when_prizes_are_added_configured_in_cmscms_configurations_cash_field_should_be_updated_in_cms__5_a_side_showdown__contest_details_page__add_a_prize_prizes_should_be_configured_in_pay_table(self):
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

    def test_005_verify_the_display_of_prize_information_when_the_below_is_configured_in_cmscms_configurations_prize_type__cash_prize_signposting___image_uploaded_prize_name__prize_value_or_both___configured(self):
        """
        DESCRIPTION: Verify the display of prize information when the below is configured in CMS
        DESCRIPTION: **CMS Configurations**
        DESCRIPTION: * 'Prize Type' = "Cash"
        DESCRIPTION: * Prize signposting - Image Uploaded
        DESCRIPTION: * 'Prize Name' / 'Prize Value' or both - configured
        EXPECTED: **ONLY PRIZE VALUE**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * Prize Value should be displayed in £
        EXPECTED: **PRIZE VALUE & Prize signposting**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * Prize Value should be displayed in £
        EXPECTED: * Prize signposting should be followed by Prize Value in £
        EXPECTED: **PRIZE VALUE & Prize NAME**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * Prize Name should be displayed
        EXPECTED: **PRIZE NAME & Prize signposting**
        EXPECTED: * Prize Name should be displayed
        EXPECTED: * Prize Name should be displayed followed by Prize Signposting
        EXPECTED: **BOTH PRIZE VALUE , PRIZE NAME  & Prize signposting**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * Prize Name should be displayed
        EXPECTED: * Prize Name should also be followed by Prize Signposting
        """
        pass

    def test_006_verify_the_display_of_prize_information_when_the_below_is_configured_in_cmscms_configurations_prize_type__ticket_prize_signposting___image_uploaded_prize_name__prize_value_or_both___configured(self):
        """
        DESCRIPTION: Verify the display of prize information when the below is configured in CMS
        DESCRIPTION: **CMS Configurations**
        DESCRIPTION: * 'Prize Type' = "Ticket"
        DESCRIPTION: * Prize signposting - Image Uploaded
        DESCRIPTION: * 'Prize Name' / 'Prize Value' or both - configured
        EXPECTED: **ONLY PRIZE VALUE**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * 'Prize Value' in **£** should be displayed with **Ticket**
        EXPECTED: **PRIZE VALUE & Prize signposting**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * 'Prize Value' in **£** should be displayed with **
        EXPECTED: Signposting and Ticket**
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

    def test_007_verify_the_display_of_prize_information_when_the_below_is_configured_in_cmscms_configurations_prize_type__voucher_prize_signposting___image_uploaded_prize_name__prize_value_or_both___configured(self):
        """
        DESCRIPTION: Verify the display of prize information when the below is configured in CMS
        DESCRIPTION: **CMS Configurations**
        DESCRIPTION: * 'Prize Type' = "Voucher"
        DESCRIPTION: * Prize signposting - Image Uploaded
        DESCRIPTION: * 'Prize Name' / 'Prize Value' or both - configured
        EXPECTED: **ONLY PRIZE VALUE**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * 'Prize Value' in **£** should be displayed with
        EXPECTED: **Voucher**
        EXPECTED: **PRIZE VALUE & Prize signposting**
        EXPECTED: * Prize should be displayed on Grid
        EXPECTED: * 'Prize Value' in **£** should be displayed with **
        EXPECTED: Signposting and Voucher**
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

    def test_008_verify_the_display_of_prize_information_when_the_below_is_configured_in_cmscms_configurations_prize_type__free_bet_prize_signposting___image_uploaded_prize_name__prize_value_or_both___configured(self):
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

    def test_009_verify_the_display_of_prize_information_is_as_configured_in_cms(self):
        """
        DESCRIPTION: Verify the display of prize information is as configured in CMS
        EXPECTED: Example :
        EXPECTED: 1. CMS :  Position - 1, Prize type - Cash, Prize value - 1000
        EXPECTED: Display **1st - £1000**
        EXPECTED: 2. CMS : Position - 1, Prize type - Cash, Prize value - 1000 , Position - 1 to 100, Prize type - Ticket, Prize value - 5
        EXPECTED: Display **1st - £1000 +  £5 Ticket**
        EXPECTED: 3. CMS : Position - 1, Prize type - Cash, Prize value - 1000 , Position - 1 to 100, Prize type - Ticket, Prize value - 5 , Signposting Uploaded -Yes
        EXPECTED: Display **1st - £1000 +  Signposting £5 Ticket**
        EXPECTED: 4. CMS : Position - 1, Prize type - Cash, Prize value - 1000 , Position - 1 to 100, Prize type - Ticket, Prize value - 5 , Signposting Uploaded -Yes, Prize Name - Just Eat ticket
        EXPECTED: Display **1st -  £1000 +  Signposting Just Eat ticket**
        """
        pass
