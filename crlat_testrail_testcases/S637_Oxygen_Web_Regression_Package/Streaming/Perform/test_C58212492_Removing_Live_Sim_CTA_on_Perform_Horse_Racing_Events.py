import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C58212492_Removing_Live_Sim_CTA_on_Perform_Horse_Racing_Events(Common):
    """
    TR_ID: C58212492
    NAME: Removing Live Sim CTA on Perform Horse Racing Events
    DESCRIPTION: This test case is verifying removing Live Sim CTA on Perform Horse Racing Events if **CSBIframeEnabled** is enabled in CMS
    PRECONDITIONS: * The PERFORM streams are mapped
    PRECONDITIONS: * In CMS (https://cms-api-ui-dev0.coralsports.dev.cloud.ladbrokescoral.com/system-configuration/structure)
    PRECONDITIONS: in section **performGroup** **CSBIframeEnabled** is enabled
    PRECONDITIONS: * App is loaded
    PRECONDITIONS: * User is logged in
    """
    keep_browser_open = True

    def test_001_navigate_to_the_horse_edp_with_perform_stream_for_uk_races_except_irish_races_and_uk_chelmsford_city_with_iframe(self):
        """
        DESCRIPTION: Navigate to the Horse EDP with Perform stream for UK races (except Irish races and UK Chelmsford City) with iFrame
        EXPECTED: **For Ladbrokes:**
        EXPECTED: * Only "Watch" button is available
        EXPECTED: * There is no button "Live sim"
        EXPECTED: ![](index.php?/attachments/get/101954467)
        EXPECTED: **For Coral:**
        EXPECTED: * Only "Live stream" button is available
        EXPECTED: * There is no button "Watch free"
        EXPECTED: ![](index.php?/attachments/get/101954468)
        """
        pass

    def test_002_in_other_cases_atr_etc(self):
        """
        DESCRIPTION: In other cases (ATR, etc)
        EXPECTED: **For Ladbrokes:**
        EXPECTED: * "Watch" and "Live sim" buttons are available
        EXPECTED: ![](index.php?/attachments/get/101954565)
        EXPECTED: **For Coral:**
        EXPECTED: * "Live stream" and "Watch free" buttons are available
        """
        pass
