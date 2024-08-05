import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C58752282_Verify_Sport_tabs_behavior_after_content_disappearing(Common):
    """
    TR_ID: C58752282
    NAME: Verify  Sport tabs behavior after content disappearing
    DESCRIPTION: This test case verifies Sport tabs behavior after content disappearing
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Please see the next test case https://ladbrokescoral.testrail.com/index.php?/cases/view/9776601 to make the necessary settings in CMS
    PRECONDITIONS: - To verify Sports Configs received from the CMS use the next link:
    PRECONDITIONS: https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/121534814)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page (except 'Matches)'
    PRECONDITIONS: 3. Choose the tab that has ticked 'Check Events' checkbox in CMS
    PRECONDITIONS: 4. Make sure that events are created for particular Sport tab
    """
    keep_browser_open = True

    def test_001__trigger_the_undisplaying_of_all_data_on_the_page_use_ob_system_verify_changes_reflection_on_the_page(self):
        """
        DESCRIPTION: * Trigger the undisplaying of all data on the page (Use OB system).
        DESCRIPTION: * Verify changes reflection on the page.
        EXPECTED: * Events disappear from the page immediately
        EXPECTED: * 'No events found' message is displayed on the page
        """
        pass

    def test_002__refresh_the_page_verify_which_tab_is_selected(self):
        """
        DESCRIPTION: * Refresh the page.
        DESCRIPTION: * Verify which tab is selected.
        EXPECTED: * The current chosen tab disappears
        EXPECTED: * The first available tab is selected
        """
        pass
