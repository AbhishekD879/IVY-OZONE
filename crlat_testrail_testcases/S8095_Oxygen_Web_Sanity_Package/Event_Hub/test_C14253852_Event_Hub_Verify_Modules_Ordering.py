import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C14253852_Event_Hub_Verify_Modules_Ordering(Common):
    """
    TR_ID: C14253852
    NAME: Event Hub: Verify Modules Ordering
    DESCRIPTION: This test case verifies Modules Ordering on the 'Event Hub' tab (mobile/tablet)
    PRECONDITIONS: Need to create Event Hub in CMS:
    PRECONDITIONS: - Event hub is created in CMS > Sport Pages > Event Hubs (Max 6 Event Hubs could be created in CMS). You should create at least 2 modules for Event Hub (Click on the 'Add Sport Module' button (e.g. 'Featured events'))
    PRECONDITIONS: **NOTE:** Featured Modules order is set in CMS > Sport Page > Event Hub > Event Hub Edit page > drag and drop modules in the table
    PRECONDITIONS: - Module ribbon tab should also be created for Event Hub: CMS > Module ribbon tabs > Create Module ribbon tab > 'Directive Name' field (choose 'Event Hub') > 'Event Hub Name' field (choose created 'Event Hub' name in the first step from the drop-down list).
    PRECONDITIONS: It is scheduled to be displayed in current time.
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: - displayOrder of corresponding Module can be found in WS> ?module=featured&EIO=3&transport=websocket > "FEATURED_STRUCTURE_CHANGED"
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: -  User is on Homepage > Event Hub tab
    """
    keep_browser_open = True

    def test_001_verify_order_ofmodules(self):
        """
        DESCRIPTION: Verify order of Modules
        EXPECTED: Modules are ordered according to order set in the Modules table in CMS
        """
        pass
