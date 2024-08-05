import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C1049082_Verify_Event_Details_Page(Common):
    """
    TR_ID: C1049082
    NAME: Verify Event Details Page
    DESCRIPTION: This test case verifies <Horse Racing> Event Details Page
    DESCRIPTION: Applies to mobile, tablet & desktop
    DESCRIPTION: AUTOTEST: [C1500841]
    PRECONDITIONS: **JIRA Tickets**:
    PRECONDITIONS: *   BMA-6587 'Racecard Layout Update - Race Information'
    PRECONDITIONS: *   BMA-6584 'Racecard Layout Update - Horse Information'
    PRECONDITIONS: *   BMA-347 'As a user I would like to see the statuses of racing events on the Horse Racing/Greyhounds Event Page'
    PRECONDITIONS: *   BMA-10747 V2 - Horse Racing Events Details Page - Meeting Event Times
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing Page
        EXPECTED: 'Horse Racing' Landing Page is opened
        """
        pass

    def test_002_verify_breadcrumbs_on_event_details_page_when_navigating_from_next_races_module(self):
        """
        DESCRIPTION: Verify Breadcrumbs on event details page when navigating from 'Next Races' module
        EXPECTED: **Mobile&Tablet**:
        EXPECTED: * Breadcrumbs are displayed on a subheader in the format: 'Horse Racing / Next Races'
        EXPECTED: * 'Down' arrow right next to 'Next Races' in breadcrumbs is available
        EXPECTED: **Desktop**:
        EXPECTED: Breadcrumbs are displayed on a subheader in the format: 'Home' / 'Horse racing' / '[Event Name]'
        """
        pass

    def test_003_verify_breadcrumbs_on_event_details_page_when_navigating_not_from_next_races_module(self):
        """
        DESCRIPTION: Verify Breadcrumbs on event details page when navigating NOT from 'Next Races' module
        EXPECTED: **Mobile&Tablet**:
        EXPECTED: * Breadcrumbs are displayed on a subheader in the format: 'Horse Racing / [Event Name]'
        EXPECTED: * 'Down' arrow right next to '[Event Name]' in breadcrumbs is available
        EXPECTED: **Desktop**:
        EXPECTED: Breadcrumbs are displayed on a subheader in the format: 'Home' / 'Horse racing' / '[Event Name]'
        """
        pass

    def test_004_verify_event_details_page_subheader_for_desktop(self):
        """
        DESCRIPTION: Verify Event details page subheader for DESKTOP
        EXPECTED: * Event name consists of two parts: "event name" + "day of the week, day and month" (e.g. Cheltenham Wednesday 12th November) is left-alligned on the page subheader
        EXPECTED: * 'Meetings' link and 'up' & 'down' arrows are shown right-aligned on the page subheader
        """
        pass

    def test_005_verify_distance(self):
        """
        DESCRIPTION: Verify Distance
        EXPECTED: * Race distance is present below the times ribbon
        EXPECTED: * **DESKTOP** The format of Race distance is: 'Distance: Xm Yf Zy'
        EXPECTED: * **Mobile** The format of Race distance is: 'Xm Yf Zy'(Ladbrokes)
        EXPECTED: * **Mobile** The format of Race distance is: 'Distance: Xm Yf Zy'(Coral)
        """
        pass

    def test_006_verify_horse_racing_event_status(self):
        """
        DESCRIPTION: Verify 'Horse Racing' Event Status
        EXPECTED: * Race Event Status is displayed next to Distance
        EXPECTED: * If Race Event Status is not available, no blank or additional space is left
        """
        pass

    def test_007_verify_racing_post__verdict_icon_if_available(self):
        """
        DESCRIPTION: Verify 'Racing Post | Verdict' icon (if available)
        EXPECTED: For **Mobile&Tablet:
        EXPECTED: **CORAL** 'Racing Post | Verdict' icon has left alignment and located under event status
        EXPECTED: **LADBROKES** 'Racing Post | Verdict' icon with arrow '>' has right alignment
        EXPECTED: For **Desktop:**
        EXPECTED: 'Racing Post | Verdict' icon has located in the second column of the display area
        """
        pass

    def test_008_verify_summary_if_available(self):
        """
        DESCRIPTION: Verify 'Summary' (if available)
        EXPECTED: **CORAL/LADBROKES**
        EXPECTED: For **Desktop&Tablet:**
        EXPECTED: *  Summary text is fully shown
        EXPECTED: **CORAL Only**
        EXPECTED: For **Mobile:**
        EXPECTED: *  100 symbols text is shown, the rest text is cut by '...'
        EXPECTED: *  'Show More' link is shown after '...' symbols
        EXPECTED: **LADBROKES Only**
        EXPECTED: For **Mobile**
        EXPECTED: * Pop up with summary of 'Racing Post | Verdict' info is displayed at the bottom of the page after tapping on 'Racing Post | Verdict >' link
        """
        pass

    def test_009_coral_only_tap_onshow_more_link_if_available(self):
        """
        DESCRIPTION: **CORAL Only** Tap on 'Show More' link (if available)
        EXPECTED: *   Race information section expanded
        EXPECTED: *   'Show More' link changed into 'Show Less' link after tapping on it
        """
        pass

    def test_010_coral_only_tap_on_show_less_link(self):
        """
        DESCRIPTION: **CORAL Only** Tap on 'Show Less' link
        EXPECTED: *   Race information section collapsed
        EXPECTED: *   'Show Less' link changed into 'Show More' link
        """
        pass
