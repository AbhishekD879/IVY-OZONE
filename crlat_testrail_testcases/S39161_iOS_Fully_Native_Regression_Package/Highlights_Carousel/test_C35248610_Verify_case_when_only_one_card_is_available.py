import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C35248610_Verify_case_when_only_one_card_is_available(Common):
    """
    TR_ID: C35248610
    NAME: Verify case when only one card is available
    DESCRIPTION: This test case verifies when only one card/slides/events is available
    PRECONDITIONS: The app is installed and launched
    PRECONDITIONS: "Featured" Tab is opened
    PRECONDITIONS: ["Highlights Carousel" is configured in CMS
    PRECONDITIONS: "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel] - will be available after functional implementation
    PRECONDITIONS: Only 1 card/slides/events available to be displayed
    """
    keep_browser_open = True

    def test_001_1_highlight_module_is_displaying(self):
        """
        DESCRIPTION: 1 Highlight module is displaying
        EXPECTED: One Highlight card/slide/event is displayed as per the design
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/17649974)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/13852939)
        """
        pass
