import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C2696904_Verify_next_boost_countdown_timer(Common):
    """
    TR_ID: C2696904
    NAME: Verify next boost countdown timer
    DESCRIPTION: This test case verifies Verify on the odds boost details page
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Add Odds Boost token to user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Generate Upcoming token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to create Upcoming Boosts https://confluence.egalacoral.com/display/SPI/How+to+create+Upcoming+Boosts
    PRECONDITIONS: User should have few upcoming tokens with the different start time
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    """
    keep_browser_open = True

    def test_001_verify_that_upcoming_boost_is_available_on_the_odds_boost_details_page(self):
        """
        DESCRIPTION: Verify that upcoming boost is available on the odds boost details page
        EXPECTED: Upcoming boosts section is available
        """
        pass

    def test_002_verify_that_next_boost_available_text_is_displayed(self):
        """
        DESCRIPTION: Verify that 'NEXT BOOST AVAILABLE' text is displayed
        EXPECTED: 'NEXT BOOST AVAILABLE' text is displayed
        """
        pass

    def test_003_verify_that_a_countdown_timer_is_displayed(self):
        """
        DESCRIPTION: Verify that a countdown timer is displayed
        EXPECTED: - A countdown timer for the next available upcoming boost is displayed
        EXPECTED: - The countdown timer counts down in the format HH:MM:SS
        EXPECTED: - Time countdown starts from the time the user loads the page to the time the earliest upcoming token will become active
        """
        pass

    def test_004_check_when_the_countdown_timer_reaches_000000(self):
        """
        DESCRIPTION: Check when the countdown timer reaches 00:00:00
        EXPECTED: The countdown timer remains at 00:00:00
        """
        pass

    def test_005_erfresh_the_page(self):
        """
        DESCRIPTION: erfresh the page
        EXPECTED: - Page is updated on refresh
        EXPECTED: - The earliest upcoming token from step #3 is shown under the 'Boosts AvailableNow' section
        EXPECTED: - 'Next boost available' is displayed
        EXPECTED: -  Time countdown starts from the time the user loads the page to the time the new earliest token will become active
        """
        pass
