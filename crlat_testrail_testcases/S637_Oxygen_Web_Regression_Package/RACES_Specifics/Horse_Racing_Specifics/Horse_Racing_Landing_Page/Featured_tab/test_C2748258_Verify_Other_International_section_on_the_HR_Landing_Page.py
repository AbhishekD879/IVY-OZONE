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
class Test_C2748258_Verify_Other_International_section_on_the_HR_Landing_Page(Common):
    """
    TR_ID: C2748258
    NAME: Verify Other International section on the HR Landing Page
    DESCRIPTION: This test case verifies displaying 'Other International' section with their relevant races within the Horse Racing Landing Page
    PRECONDITIONS: International Horse Racing events are available
    PRECONDITIONS: 'Is Intenational' checkbox is marked in TI on a type level (typeFlagCodes:INT)
    PRECONDITIONS: To get the UK/Irish/International daily races events check modules (modules name can be changed in CMS) in 'FEATURED_STRUCTURE_CHANGED' request from websocket (wss://featured-sports)
    PRECONDITIONS: Example of event structure:
    PRECONDITIONS: **flag:** "UK",
    PRECONDITIONS: **data:** [{
    PRECONDITIONS: **id:** "230549330",
    PRECONDITIONS: **categoryId:** "21",
    PRECONDITIONS: **categoryName:** "Horse Racing",
    PRECONDITIONS: **className:** "Horse Racing - Live",
    PRECONDITIONS: **name:** "Southwell",
    PRECONDITIONS: **typeName:** "Southwell",
    PRECONDITIONS: **startTime:** 1593614400000,
    PRECONDITIONS: **classId:** "285",
    PRECONDITIONS: **cashoutAvail:** "Y",
    PRECONDITIONS: **poolTypes:**  ["UPLP", "UQDP"],
    PRECONDITIONS: **liveStreamAvailable:** true,
    PRECONDITIONS: **isResulted:** false,
    PRECONDITIONS: **isStarted:** false,
    PRECONDITIONS: **eventIsLive:** false,
    PRECONDITIONS: **isFinished:** false,
    PRECONDITIONS: **isBogAvailable:** false,
    PRECONDITIONS: **isLpAvailable:** false,
    PRECONDITIONS: **drilldownTagNames:** "EVFLAG_BL,EVFLAG_AVA,",
    PRECONDITIONS: **localTime:** "15:40"
    PRECONDITIONS: **markets:** [{
    PRECONDITIONS: **drilldownTagNames:** 'MKTFLAG_EPR',
    PRECONDITIONS: **eachWayFactorNum:** 1,
    PRECONDITIONS: **eachWayFactorDen:** 2,
    PRECONDITIONS: **eachWayPlaces:** 3,
    PRECONDITIONS: **isEachWayAvailable:** true
    PRECONDITIONS: **Note:** Business will use only ONE location flag (UK/US/ZA/AE/CL/IN/AU/FR/INT/IE/VR)
    PRECONDITIONS: **User is on Horse Racing landing page**
    """
    keep_browser_open = True

    def test_001_verify_displaying_relevant_races_within_other_international_section(self):
        """
        DESCRIPTION: Verify displaying relevant races within 'Other International' section
        EXPECTED: Races with **typeFlagCodes: INT** should be displayed within 'Other International' section
        """
        pass

    def test_002_verify_ordering_of_accordions(self):
        """
        DESCRIPTION: Verify ordering of accordions
        EXPECTED: 'Other International' section should be displaying after all subregions and before Virtual(if such exists)
        """
        pass
