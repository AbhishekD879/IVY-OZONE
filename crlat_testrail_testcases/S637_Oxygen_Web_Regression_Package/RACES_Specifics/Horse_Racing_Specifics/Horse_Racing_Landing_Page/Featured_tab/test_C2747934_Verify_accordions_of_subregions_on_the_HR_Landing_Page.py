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
class Test_C2747934_Verify_accordions_of_subregions_on_the_HR_Landing_Page(Common):
    """
    TR_ID: C2747934
    NAME: Verify accordions of subregions on the HR Landing Page
    DESCRIPTION: This test case verifies displaying accordions of subregion with their relevant races within the Horse Racing Landing Page
    PRECONDITIONS: International Horse Racing events are available
    PRECONDITIONS: Respective Country flag are ticked in TI at "Type Level" (i.e is in UK / is Irish, etc)
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

    def test_001_verify_accordions_of_subregion_on_horse_racing_landing_page(self):
        """
        DESCRIPTION: Verify accordions of subregion on Horse Racing Landing Page
        EXPECTED: 1. Respective races should be displayed within their relevant subregion accordion.
        EXPECTED: According to the **typeFlagCodes** of races:
        EXPECTED: - UK - UK & IRE
        EXPECTED: - IE - UK & IRE
        EXPECTED: - US - USA
        EXPECTED: - ZA- South Africa
        EXPECTED: - AE - UAE
        EXPECTED: - CL - Chile
        EXPECTED: - IN - India
        EXPECTED: - AU - Australia
        EXPECTED: - FR -  France
        EXPECTED: - VS - Quantum Leap Virtual Races
        """
        pass

    def test_002_verify_ordering_of_accordions(self):
        """
        DESCRIPTION: Verify ordering of accordions
        EXPECTED: 1. Accordions of subregions within the Horse Racing Landing Page should be displayed in below order:
        EXPECTED: - UK and IRE
        EXPECTED: - France
        EXPECTED: - UAE
        EXPECTED: - South Africa
        EXPECTED: - India
        EXPECTED: - USA
        EXPECTED: - Australia
        EXPECTED: - Chile
        EXPECTED: Note: 'UK and IRE', 'International Tote', 'International Races', 'Virtual Races' and 'Ladbrokes/Coral Legends' display order can be set in CMS.
        """
        pass
