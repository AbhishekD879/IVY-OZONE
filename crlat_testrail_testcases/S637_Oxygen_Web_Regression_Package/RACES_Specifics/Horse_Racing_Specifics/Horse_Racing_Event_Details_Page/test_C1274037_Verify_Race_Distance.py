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
class Test_C1274037_Verify_Race_Distance(Common):
    """
    TR_ID: C1274037
    NAME: Verify Race Distance
    DESCRIPTION: This test case verifies Race Distance of individual race event on Event Details Page
    DESCRIPTION: Applies to mobile, tablet & desktop
    DESCRIPTION: AUTOTEST: [C1501628]
    PRECONDITIONS: update: After BMA-40744 implementation we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: ----
    PRECONDITIONS: **JIRA Ticket **: BMA-6587 'Racecard Layout Update - Race Information'
    PRECONDITIONS: 1) To get an info about race distance of event use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?racingForm=event&translationLang=LL
    PRECONDITIONS: Where,
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   *ZZZZ - an event id*
    PRECONDITIONS: *   *LL - language (e.g. en, ukr) *
    PRECONDITIONS: See attribute **distance="Yards,YYY,"**, where YYY - is distance always in yards, to see whether distance is available for selected event
    PRECONDITIONS: 2) To convert yards into miles, furlongs and yards please do the following:
    PRECONDITIONS: *   A = 'distance'/1760 - whole number is **number of miles**
    PRECONDITIONS: *   B = 'distance' - A*1760
    PRECONDITIONS: *   C = B/220 - whole number is **number of furlongs**
    PRECONDITIONS: *   D = B - C*220 - **number of yards**
    """
    keep_browser_open = True

    def test_001_go_to_event_details_page_of_event_with_race_distance_available(self):
        """
        DESCRIPTION: Go to event details page of event with race distance available
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_verify_distance_presence_format_and_correctness(self):
        """
        DESCRIPTION: Verify distance presence, format and correctness
        EXPECTED: Distance values are the same with values calculated in Preconditions
        EXPECTED: Race distance is present on the left side below time switcher tabs. The format of Race distance is :
        EXPECTED: **'Distance: Xm ****Yf**** Zy'**
        EXPECTED: where,
        EXPECTED: *   X - number of miles
        EXPECTED: *   Y - number of furlongs
        EXPECTED: *   Z - number of yards
        EXPECTED: **If any value is 0 - this part is not shown on front-end**
        """
        pass

    def test_003_go_to_event_details_page_of_event_with_no_race_distance_available_no_distance_attribute_in_ss_response(self):
        """
        DESCRIPTION: Go to event details page of event with NO race distance available (NO 'distance' attribute in SS response)
        EXPECTED: Distance label and values are not shown on Event details page
        """
        pass
