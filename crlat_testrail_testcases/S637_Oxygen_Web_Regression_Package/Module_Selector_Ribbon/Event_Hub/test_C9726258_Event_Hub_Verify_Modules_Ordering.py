import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9726258_Event_Hub_Verify_Modules_Ordering(Common):
    """
    TR_ID: C9726258
    NAME: Event Hub: Verify Modules Ordering
    DESCRIPTION: This test case verifies Modules Ordering on Event hab tab (mobile/tablet).
    PRECONDITIONS: 1. AT least 1 Event Hub is created in CMS and it contains at least one instance of each module (Featured events, Quick links, Surface Bets, Highlights Carousel).
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 2. displayOrder of corresponding Module can be found in WS> ?module=featured&EIO=3&transport=websocket > "FEATURED_STRUCTURE_CHANGED"
    PRECONDITIONS: **NOTE:** Featured Modules order is set in CMS > Sport Page > Event Hub > Event Hub Edit page > drag and drop modules in the table
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 3. User is on Homepage > Event Hub tab
    """
    keep_browser_open = True

    def test_001_verify_order_ofmodules(self):
        """
        DESCRIPTION: Verify order of Modules
        EXPECTED: Modules are ordered according to order set in the Modules table in CMS
        """
        pass
