import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60026747_Verify_displaying_Matches_Outright_events_data_on_Competition_Details_page(Common):
    """
    TR_ID: C60026747
    NAME: Verify displaying Matches/Outright events data on Competition Details page
    DESCRIPTION: This test case verifies displaying Matches/Outright events data on Competition Details page.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football landing page > Competitions tab
    PRECONDITIONS: NOTE:
    PRECONDITIONS: Matches/Outright requests
    PRECONDITIONS: ![](index.php?/attachments/get/121267153)
    """
    keep_browser_open = True

    def test_001_click_on_the_competition_that_has_only_outright_events_available(self):
        """
        DESCRIPTION: Click on the Competition that has only Outright events available
        EXPECTED: * User is redirected to Selected Competition Details page
        EXPECTED: * Outright/Matches requests are received with relevant data
        EXPECTED: **Desktop**
        EXPECTED: * 'Matches' tab is displayed in tab switcher with "No events found" message present in the content area.
        EXPECTED: * 'Outrights' tab is displayed in tab switcher
        EXPECTED: * Outrights events data taken from Outright request is displayed on Outrighs tab
        EXPECTED: **Mobile**
        EXPECTED: * Tab switchers panel is NOT displayed
        EXPECTED: * Outrights events data taken from Outright request is displayed
        """
        pass

    def test_002_go_back_to_competitions_page___click_on_the_competition_that_has_only_matches_events_available(self):
        """
        DESCRIPTION: Go back to Competitions page -> Click on the Competition that has only Matches events available
        EXPECTED: 
        """
        pass

    def test_003_verify_displaying_of_matchesoutright_events_data_on_competition_details_page(self):
        """
        DESCRIPTION: Verify displaying of Matches/Outright events data on Competition Details page
        EXPECTED: * User is redirected to Selected Competition Details page
        EXPECTED: * Outright/Matches requests are received with relevant data
        EXPECTED: **Desktop**
        EXPECTED: * 'Matches' tab is displayed in tab switcher with Matches events data taken from Matches request.
        EXPECTED: * 'Outrights' tab is NOT displayed in tab switcher in case there is no data received Outright request
        EXPECTED: **Mobile**
        EXPECTED: * Tab switchers panel is NOT displayed
        EXPECTED: * Matches data taken from Matches request is displayed.
        """
        pass

    def test_004_go_back_to_competitions_page___click_on_the_competition_that_has_both_matches_and_outright_events_available(self):
        """
        DESCRIPTION: Go back to Competitions page -> Click on the Competition that has both Matches and Outright events available
        EXPECTED: 
        """
        pass

    def test_005_verify_displaying_of_matchesoutright_events_data_on_competition_details_page(self):
        """
        DESCRIPTION: Verify displaying of Matches/Outright events data on Competition Details page
        EXPECTED: * User is redirected to Selected Competition Details page
        EXPECTED: * Outright/Matches requests are received with relevant data
        EXPECTED: **Desktop**
        EXPECTED: * 'Matches' tab is displayed in tab switcher with Matches events data taken from Matches request.
        EXPECTED: * 'Outrights' tab is  displayed in tab switcher with Outrights events data taken from Outright request.
        EXPECTED: **Mobile**
        EXPECTED: * Tab switchers panel is displayed with 'Matches' and 'Outrights' tabs
        EXPECTED: * Matches data taken from Matches request is displayed under 'Matches' tab.
        EXPECTED: * Outrights data taken from Outright request is displayed under 'Outrights' tab.
        """
        pass
