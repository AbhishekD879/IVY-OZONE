import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C2696889_Verify_displaying_Upcoming_tokens_section_on_Odds_Boost_details_page(Common):
    """
    TR_ID: C2696889
    NAME: Verify displaying Upcoming tokens section on Odds Boost details page
    DESCRIPTION: This test case verifies displaying Upcoming tokens section on Odds Boost details page
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Add Odds Boost token to user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: How to create Upcoming Boosts https://confluence.egalacoral.com/display/SPI/How+to+create+Upcoming+Boosts
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    """
    keep_browser_open = True

    def test_001_navigate_to_odds_boost_details_pageverify_displaying_upcoming_tokens_section_on_odds_boost_details_page(self):
        """
        DESCRIPTION: Navigate to Odds Boost details page
        DESCRIPTION: Verify displaying Upcoming tokens section on Odds Boost details page
        EXPECTED: - The 'UPCOMING BOOSTS' title is shown
        EXPECTED: - Text: "Look out for boosts appearing here for upcoming events!' is shown
        EXPECTED: - A countdown timer 'Next boost available' is displayed in format HH:MM:SS
        EXPECTED: - Time countdown starts from the time the user loads the page to the time the token will become active
        EXPECTED: - Respective Upcoming Boosts which will be available on upcoming events are displayed below in this area
        """
        pass
