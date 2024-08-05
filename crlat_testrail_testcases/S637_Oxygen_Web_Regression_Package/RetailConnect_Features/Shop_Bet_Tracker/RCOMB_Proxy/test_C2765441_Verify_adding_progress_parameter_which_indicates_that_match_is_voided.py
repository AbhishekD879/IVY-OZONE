import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2765441_Verify_adding_progress_parameter_which_indicates_that_match_is_voided(Common):
    """
    TR_ID: C2765441
    NAME: Verify adding "progress" parameter which indicates that match is voided
    DESCRIPTION: This test case verify adding "progress" parameter which indicates that match is voided
    DESCRIPTION: JIRA ticked:
    DESCRIPTION: HMN-2994 Pass "progress" param to the front-end
    PRECONDITIONS: Request creation of coupon code with at list 3 (or more) events  in it
    PRECONDITIONS: one event should be voided
    PRECONDITIONS: second one should be avandoned
    PRECONDITIONS: and third game - just normal one
    """
    keep_browser_open = True

    def test_001__load_digital_barcode_details_viahttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbettrackerbetsusinggetuse_the_barcode_as_a_parameter_check_progress_value_in_otherattributes_section(self):
        """
        DESCRIPTION: * Load digital barcode details via
        DESCRIPTION: https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetTrackerBetsUsingGET
        DESCRIPTION: (Use the barcode as a parameter)
        DESCRIPTION: * Check "progress" value (in "otherAttributes" section)
        EXPECTED: * For voided event "progress" contains 'VOID MATCH' value
        EXPECTED: * For abandoned event "progress" contains  'ABANDONED MATCH' value
        EXPECTED: * Normal event - "progress" parameter contains empty value
        """
        pass
