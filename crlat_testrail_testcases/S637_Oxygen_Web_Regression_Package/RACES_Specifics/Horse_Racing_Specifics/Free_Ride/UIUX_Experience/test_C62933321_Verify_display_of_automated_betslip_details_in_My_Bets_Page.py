import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C62933321_Verify_display_of_automated_betslip_details_in_My_Bets_Page(Common):
    """
    TR_ID: C62933321
    NAME: Verify display of automated betslip details in My Bets Page
    DESCRIPTION: This test case verifies display of automated betslip details in My Bets Page
    PRECONDITIONS: 1. Third question with Answers(option1,Option2 and Option3) and Summary message are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
    PRECONDITIONS: 2. Login to Ladbrokes application with eligible customers for Free Ride
    PRECONDITIONS: 3. Click on 'Launch Banner' in Homepage
    PRECONDITIONS: 4. Click on CTA Button in Splash Page
    PRECONDITIONS: 5. User should select answers for First, Second and Third questions
    """
    keep_browser_open = True

    def test_001_verify_display_of_automated_betslip(self):
        """
        DESCRIPTION: Verify display of automated betslip
        EXPECTED: Automated betslip should be successfully generated in Free Ride Overlay
        """
        pass

    def test_002_verify_the_fields_inautomated_betslip(self):
        """
        DESCRIPTION: Verify the fields in automated betslip
        EXPECTED: Below information should be displayed:
        EXPECTED: * That’s it! We made something for you:
        EXPECTED: * Name of the Horse:
        EXPECTED: * Name of the Jockey
        EXPECTED: * Event Time, Meeting place name
        EXPECTED: * Jockey(kits and crests) logo below to summary details
        EXPECTED: * "CTA TO RACECARD" CTA should be displayed
        """
        pass

    def test_003_navigate_to_my_bets_page(self):
        """
        DESCRIPTION: Navigate to My Bets page
        EXPECTED: Automated Betslip details should be displayed in My Bets page
        EXPECTED: * Single @Odds
        EXPECTED: * Receipt No:
        EXPECTED: * Selection Name
        EXPECTED: * Win or Each Way market
        EXPECTED: * Time, Meeting place name
        """
        pass

    def test_004_verify_display_offree_ride_signposting(self):
        """
        DESCRIPTION: Verify display of Free Ride signposting
        EXPECTED: Free Ride signposting should be displayed to be Betslip details in My Bets page
        EXPECTED: Note:
        EXPECTED: As mentioned by OpenBet, Free Ride signpost display will be available after Promo sign posting implementation.
        """
        pass
