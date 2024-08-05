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
class Test_C9627815_Races_grouping_by_sub_regions(Common):
    """
    TR_ID: C9627815
    NAME: <Races>: grouping by sub regions
    DESCRIPTION: This test case verifies displaying of <Race> events grouped by sub region
    PRECONDITIONS: 1) To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: 2) TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 3) You should have <Race> events from different types and types should be assigned to different sub regions
    PRECONDITIONS: 4) **Check boxes in 'Flags' section in TI on type level:**
    PRECONDITIONS: - Is in UK - typeFlagCodes="UK"
    PRECONDITIONS: - Is Irish - typeFlagCodes="IE"
    PRECONDITIONS: - South Africa - typeFlagCodes="ZA"
    PRECONDITIONS: - UAE - typeFlagCodes="AE"
    PRECONDITIONS: - Chile - typeFlagCodes="CL"
    PRECONDITIONS: - India - typeFlagCodes="IN"
    PRECONDITIONS: - Australia - typeFlagCodes="AU"
    PRECONDITIONS: - US - typeFlagCodes="US"
    PRECONDITIONS: - France - typeFlagCodes="FR"
    PRECONDITIONS: - Is International - typeFlagCodes="INT"
    PRECONDITIONS: - Virtual Racing - typeFlagCodes="VR"
    PRECONDITIONS: 5) You should be on <Race> landing page
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_events_by_sub_regions(self):
        """
        DESCRIPTION: Verify displaying of events by sub regions
        EXPECTED: Events are grouped and displayed under respective sub regions sections according to the types configurations:
        EXPECTED: - Is in UK (typeFlagCodes="UK") - displayed within 'UK & IRE' section
        EXPECTED: - Is Irish (typeFlagCodes="IE") - displayed within 'UK & IRE' section
        EXPECTED: - Virtual Racing (typeFlagCode="VR") - displayed within 'Ladbrokes/Coral Legends' section
        EXPECTED: - South Africa (typeFlagCodes="ZA") - displayed within 'South Africa' section
        EXPECTED: - UAE (typeFlagCodes="AE") - displayed within 'UAE' section
        EXPECTED: - Chile (typeFlagCodes="CL") - displayed within 'Chile' section
        EXPECTED: - India (typeFlagCodes="IN") - displayed within 'India' section
        EXPECTED: - Australia (typeFlagCodes="AU") - displayed within 'Austria' section
        EXPECTED: - US (typeFlagCodes="US") - displayed within 'USA' section
        EXPECTED: - France (typeFlagCodes="FR") - displayed within 'France' section
        EXPECTED: - Is International (typeFlagCodes="INT") - displayed within 'Other International' section
        """
        pass
