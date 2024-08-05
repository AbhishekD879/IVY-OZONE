import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29375_Featured_Verify_Modules_Ordering(Common):
    """
    TR_ID: C29375
    NAME: Featured: Verify Modules Ordering
    DESCRIPTION: This test case verifies Modules Ordering on Feature tab (mobile/tablet) Featured section (desktop)
    PRECONDITIONS: 1. AT least 2 Active Featured modules are created in CMS.
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2. displayOrder of corresponding Module can be found in WS> ?module=featured&EIO=3&transport=websocket > "FEATURED_STRUCTURE_CHANGED"
    PRECONDITIONS: **NOTE:** Featured Modules order is set in CMS > Featured tab Modules edit page > Module Order (less is more)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_module_selector_ribbon(self):
        """
        DESCRIPTION: Go to Module Selector Ribbon
        EXPECTED: **For mobile/tablet:**
        EXPECTED: 'Featured' tab is selected by default
        EXPECTED: **For desktop:**
        EXPECTED: Module Ribbon Tabs are transformed into sections, displayed in the following order:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play & Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        """
        pass

    def test_003_verify_order_ofmodules(self):
        """
        DESCRIPTION: Verify order of Modules
        EXPECTED: Modules are ordered according to "displayOrder" parameter in ascending order.
        """
        pass
