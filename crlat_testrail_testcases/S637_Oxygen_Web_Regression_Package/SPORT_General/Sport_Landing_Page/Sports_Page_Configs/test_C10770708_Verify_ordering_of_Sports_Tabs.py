import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C10770708_Verify_ordering_of_Sports_Tabs(Common):
    """
    TR_ID: C10770708
    NAME: Verify ordering of Sports Tabs
    DESCRIPTION: This test case verifies ordering of Sports Tabs
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - Please see the next test case https://ladbrokescoral.testrail.com/index.php?/cases/view/9776601 to make the necessary settings in CMS
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the next link:
    PRECONDITIONS: https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/121534814)
    PRECONDITIONS: ![](index.php?/attachments/get/100268081)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page
    """
    keep_browser_open = True

    def test_001_verify_sports_tabs_ordering_on_the_page(self):
        """
        DESCRIPTION: Verify Sports Tabs ordering on the page
        EXPECTED: * The Sports Tabs ordering corresponds to setting in CMS
        EXPECTED: * Ordering of Sports Tabs received in <sport-config> response corresponds to setting in CMS
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass

    def test_002__navigate_to_cms__sport_pages__sport_categories__sport_change_the_ordering_of_sports_tabs_by_drag_and_drop(self):
        """
        DESCRIPTION: * Navigate to CMS > Sport Pages > Sport Categories > Sport.
        DESCRIPTION: * Change the ordering of Sports Tabs by drag and drop.
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_003__back_to_the_app_refresh_the_page(self):
        """
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        EXPECTED: * The Sports Tabs ordering is changed
        EXPECTED: * The Sports Tabs ordering corresponds to setting in CMS
        EXPECTED: * Ordering of Sports Tabs received in <sport-config> response corresponds to setting in CMS
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass
