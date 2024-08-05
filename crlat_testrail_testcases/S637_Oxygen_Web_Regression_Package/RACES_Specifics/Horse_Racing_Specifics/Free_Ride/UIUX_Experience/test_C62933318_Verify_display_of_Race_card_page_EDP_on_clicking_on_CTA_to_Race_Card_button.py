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
class Test_C62933318_Verify_display_of_Race_card_page_EDP_on_clicking_on_CTA_to_Race_Card_button(Common):
    """
    TR_ID: C62933318
    NAME: Verify display of Race card page (EDP) on clicking on 'CTA to Race Card' button
    DESCRIPTION: This test case verifies display of Race card page on clicking on 'CTA to Race Card' button
    PRECONDITIONS: 1. Third question with Answers(option1,Option2 and Option3) are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
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
        EXPECTED: * "CTA TO RACECARD" button should be displayed
        """
        pass

    def test_003_click_on_cta_to_racecard_button(self):
        """
        DESCRIPTION: Click on 'CTA TO RACECARD' button
        EXPECTED: * User should be navigated to race card page of the allocated horse (EDP)
        EXPECTED: * User should be able to see the ongoing journey(s) in the race card page
        """
        pass
