import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C44870421_Verify_Tote_UK_International_Results(Common):
    """
    TR_ID: C44870421
    NAME: Verify Tote UK & International Results
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_httpsmsportsladbrokescom(self):
        """
        DESCRIPTION: Open https://msports.ladbrokes.com
        EXPECTED: Ladbrokes application open.
        """
        pass

    def test_002_click_on_international_tote(self):
        """
        DESCRIPTION: Click on International Tote
        EXPECTED: User navigated to International Tote LP
        """
        pass

    def test_003_click_on_results(self):
        """
        DESCRIPTION: Click on results
        EXPECTED: User is displayed list of Internatioal Tote meetings available for the day.
        """
        pass

    def test_004_verify_results_update_as_per_meeting_occurenceclick_on_a_few_meeting_accordions___expand_these_and_verify_the_results(self):
        """
        DESCRIPTION: Verify results update as per meeting occurence
        DESCRIPTION: Click on a few meeting accordions - expand these and verify the results
        EXPECTED: Results are updated as per time of the day
        EXPECTED: No results are present if race has not completed
        """
        pass

    def test_005_repeat_the_same_for_uk_horse_racing_tote_meetings(self):
        """
        DESCRIPTION: Repeat the same for UK Horse racing tote meetings
        EXPECTED: Expected results same as above
        """
        pass
