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
class Test_C28837_Verify_Event_Details_Page(Common):
    """
    TR_ID: C28837
    NAME: Verify Event Details Page
    DESCRIPTION: This test case verifies Greyhound Event Details Page
    PRECONDITIONS: update: After BMA-40744 implementation we'll use RDH feature toggle:
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - TimeForm info will NOT be displayed.
    PRECONDITIONS: we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: ------
    PRECONDITIONS: **JIRA Tickets**:
    PRECONDITIONS: *   BMA-6587 'Racecard Layout Update - Race Information'
    PRECONDITIONS: *   BMA-347 'As a user, I would like to see the statuses of racing events on the Horse Racing/Greyhounds Event Page'
    """
    keep_browser_open = True

    def test_001_navigate_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds landing page
        EXPECTED: Landing page is opened
        """
        pass

    def test_002_verify_breadcrumbs_on_next_races_event_details_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs on next races event details page
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: * Breadcrumbs are displayed on a subheader in format:
        EXPECTED: - For 'Next Races': 'Greyhound / Next Races'
        EXPECTED: * 'Down' arrow right next to '[Event Name]'/'Next Races' in breadcrumbs is available
        EXPECTED: **Desktop:**
        EXPECTED: * Breadcrumbs are displayed on a subheader in the format: 'Home' / 'Greyhound racing' / '[Event Name]'
        """
        pass

    def test_003_verify_event_details_page_subheader(self):
        """
        DESCRIPTION: Verify event details page subheader
        EXPECTED: **Mobile&Tablet:**
        EXPECTED: * Breadcrumbs are displayed on a subheader in format:
        EXPECTED: - For meetings: 'Greyhound / [Event Name]'
        EXPECTED: * 'Down' arrow right next to '[Event Name]'/'Next Races' in breadcrumbs is available
        EXPECTED: **Desktop:**
        EXPECTED: - Event name consists of two parts: "event name" + "day of the week, day and month" (e.g. Cheltenham Wednesday 12th November) is left-alligned on the page subheader
        EXPECTED: - 'Meetings' link and 'up' & 'down' arrows are shown right-aligned on the page subheader
        EXPECTED: - Breadcrumbs are displayed on a subheader in the format: 'Home' / 'Greyhound racing' / '[Event Name]'
        """
        pass

    def test_004_verify_distance(self):
        """
        DESCRIPTION: Verify distance
        EXPECTED: *   Race distance is present next to event name and displayed via '/'
        EXPECTED: *   The format of Race distance is: 'Distance: Xm'
        """
        pass

    def test_005_verify_race_event_status(self):
        """
        DESCRIPTION: Verify Race Event Status
        EXPECTED: **Coral:**
        EXPECTED: *   Race Grade is displayed under Event Name and distance
        EXPECTED: *   If Race Grade is not available, no blank or additional space is left
        EXPECTED: **Ladbrokes:**
        EXPECTED: *   Race Type is displayed under Event Name and to the right of race distance
        """
        pass

    def test_006_verify_timeform_label_if_available(self):
        """
        DESCRIPTION: Verify 'Timeform' label (if available)
        EXPECTED: For **mobile&tablet:
        EXPECTED: ** 'Timeform' label has left alignment and located under event status
        EXPECTED: For **desktop:**
        EXPECTED: 'Timeform' label has located in the second column of the display area
        """
        pass

    def test_007_verify_summary_if_available(self):
        """
        DESCRIPTION: Verify 'Summary' (if available)
        EXPECTED: For **Desktop&Tablet:**
        EXPECTED: *  Summary text is fully shown
        EXPECTED: For **Mobile:**
        EXPECTED: *  100 symbols text is shown, the rest text is cut by '...'
        EXPECTED: *  'Show More' link is shown after '...' symbols
        """
        pass

    def test_008_tap_onshow_more_link_if_available(self):
        """
        DESCRIPTION: Tap on 'Show More' link (if available)
        EXPECTED: *   Race information section expanded
        EXPECTED: *   'Show More' link changed into 'Show Less' link after tapping on it
        """
        pass

    def test_009_tap_on_show_less_link(self):
        """
        DESCRIPTION: Tap on 'Show Less' link
        EXPECTED: *   Race information section collapsed
        EXPECTED: *   'Show Less' link changed into 'Show More' link
        """
        pass
