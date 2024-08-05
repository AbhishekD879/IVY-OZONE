import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870201_Verify_that_if_user_taps_in_any_resulted_race_on_Race_landing_page_will_be_navigated_to_Results_tab_and_there_user_is_able_to_find_the_race_details_correct_and_complete_displayed_in_both_tabs_By_latest_Results_and_By_Meetings(Common):
    """
    TR_ID: C44870201
    NAME: Verify that if user taps in any resulted race on Race landing page will be navigated to Results tab and there user is able to find the race details correct and complete displayed, in both tabs, By latest Results and By Meetings
    DESCRIPTION: Verify that if user taps in any resulted race on Race landing page will be navigated to Results tab and there user is able to find the race details correct and complete displayed, in both tabs, By latest Results and By Meetings
    PRECONDITIONS: "User is in Race Landing page on Today tab or in EDP and event status is OFF or Resulted.
    PRECONDITIONS: 1. Horse Racing
    PRECONDITIONS: 2. Greyhounds"
    """
    keep_browser_open = True

    def test_001_load_the_siteapp(self):
        """
        DESCRIPTION: Load the site/app
        EXPECTED: User is on the Homepage
        """
        pass

    def test_002_navigate_to_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to Horse racing page
        EXPECTED: User is on the Featured page of Horse racing
        """
        pass

    def test_003_verify_the_results_icon_for_any_resulted_event_and_click_on_it(self):
        """
        DESCRIPTION: Verify the Results icon for any resulted event and click on it
        EXPECTED: User is taken to the resulted page of that particular event
        """
        pass

    def test_004_verify_the_results1st2nd3rd__dividends__non_runners_silks(self):
        """
        DESCRIPTION: Verify the results
        DESCRIPTION: 1st/2nd/3rd , dividends & Non runners, silks
        EXPECTED: Results are displayed with
        EXPECTED: 1st/2nd/3rd, dividends, non-runners and silks available
        EXPECTED: Screenshot for reference below:
        EXPECTED: ![](index.php?/attachments/get/103338360)
        """
        pass

    def test_005_verify_step_2_4_for_greyhounds(self):
        """
        DESCRIPTION: Verify Step 2-4 for Greyhounds
        EXPECTED: 
        """
        pass
