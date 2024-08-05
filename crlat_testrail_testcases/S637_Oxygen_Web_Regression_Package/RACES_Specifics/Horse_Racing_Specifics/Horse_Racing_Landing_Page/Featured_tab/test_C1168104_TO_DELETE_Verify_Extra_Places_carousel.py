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
class Test_C1168104_TO_DELETE_Verify_Extra_Places_carousel(Common):
    """
    TR_ID: C1168104
    NAME: [TO DELETE] Verify Extra Places carousel
    DESCRIPTION: This test case verifies Extra Places carousel on Horse Racing 'Featured' tab.
    DESCRIPTION: Applies for mobile, tablet & desktop.
    DESCRIPTION: AUTOTEST: [C1592556]
    PRECONDITIONS: 1) In order to create HR Extra Place Race meeting use TI tool http://backoffice-tst2.coral.co.uk/ti/
    PRECONDITIONS: - 'Extra Place Race' flag should be checked on 'Win Or Each Way' market level ('drilldownTagNames'='MKTFLAG_EPR' in SS response)
    PRECONDITIONS: - 'Each Way' terms correspond to **'eachWayFactorNum'**, **'eachWayFactorDen'** and **'eachWayPlaces'** attributes from the Site Server.
    PRECONDITIONS: 2) For checking info regarding event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing landing page
        EXPECTED: - Horse Racing landing page is opened
        EXPECTED: - 'Featured' tab is opened by default
        """
        pass

    def test_003_verify_availability_of_enhanced_races_module(self):
        """
        DESCRIPTION: Verify availability of 'Enhanced Races' module
        EXPECTED: - 'Enhanced Races' module is displayed if at least one event is available that meets Preconditions, otherwise module is not displayed
        EXPECTED: - 'Enhanced Races' accordion is expanded by default
        EXPECTED: - If only one event is available that meets Preconditions, it is displayed in full width within the carousel
        EXPECTED: -  If more than one events are available that meets Preconditions, they may be swiped left/right within the carousel
        EXPECTED: - 'Enhanced Races' accordion is collapsible/expandable once tapped
        EXPECTED: **For tablet/desktop:**
        EXPECTED: - Module's title is 'Enhanced Races'
        EXPECTED: - 'Extra Place' meetings are displayed in two columns view (NOT in a carousel)
        """
        pass

    def test_004_verify_a_meeting_header_within_enhanced_races_module(self):
        """
        DESCRIPTION: Verify a meeting header within 'Enhanced Races' module
        EXPECTED: - 'Extra Place' header is displayed for each meeting within the carousel
        EXPECTED: - Countdown timer (MM:SS) is displayed in a header, if there are 45 and less minutes left to the start of an event
        EXPECTED: - [REMOVED FUNCTIONALITY] The countdown timer is replaced with correspondent badge when first race status is received
        EXPECTED: HR Statuses :
        EXPECTED: *   'race_stage'='**D**' correspond to 'Delayed' badge
        EXPECTED: *   'race_stage'='**B**' correspond to 'Going Down' badge
        EXPECTED: *   'race_stage'='**C**' correspond to 'At the Post' badge
        EXPECTED: *   'race_stage'='**E**' correspond to 'Going Behind' badge
        EXPECTED: *   'race_stage'='**O**' correspond to 'Off' badge (when this status is received, a meeting disappears from the carousel)
        """
        pass

    def test_005_verify_an_extra_place_meeting_content_area(self):
        """
        DESCRIPTION: Verify an Extra Place meeting content area
        EXPECTED: - ***Time of an event*** (corresponds to 'startDate' in SS response) and ***event name*** (taken from event 'name' from SS response)
        EXPECTED: - [num/den] the Odds, [e.g. 1 - 2 - 3 - ***4***] places the race is eligible and the extra place in bold (here ***4***), if Each Way terms are available (see Preconditions)
        EXPECTED: - ">" icon
        """
        pass

    def test_006_tap_on_extra_place_meeting_area(self):
        """
        DESCRIPTION: Tap on Extra Place meeting area
        EXPECTED: Meeting area is clickable and leads to the Race Card of a corresponding event once tapped
        """
        pass

    def test_007_verify_availability_of_event_what_is_displayed_on_the_carousel_in_the_horse__race_grid(self):
        """
        DESCRIPTION: Verify availability of event what is displayed on the carousel in the Horse  Race Grid
        EXPECTED: Event is displayed on the Horse Race Grid
        """
        pass
