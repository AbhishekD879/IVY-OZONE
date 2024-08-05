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
class Test_C10397559_Verify_Sports_Tab_name_editing(Common):
    """
    TR_ID: C10397559
    NAME: Verify 'Sports Tab' name editing
    DESCRIPTION: This test case verifies 'Sports Tab' name editing
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - Info about tabs displaying depends on Platforms or Tier Type could be found here: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-TabsdisplayingfordifferentPlatformsandTierTypes
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the following <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/121534814)
    PRECONDITIONS: ![](index.php?/attachments/get/100268078)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'Sports Landing Page'
    """
    keep_browser_open = True

    def test_001_verify_sports_tabs_displaying_according_to_received_data_from_cms(self):
        """
        DESCRIPTION: Verify 'Sports Tabs' displaying according to received data from CMS
        EXPECTED: * The 'Sports Tabs' are displayed on the 'Sports Landing Page'
        EXPECTED: * Set of 'Sports Tabs' corresponds to data in <sport-config> response received from CMS
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass

    def test_002__navigate_to_cms_edit_the_name_of_any_sports_tab_save_the_changes(self):
        """
        DESCRIPTION: * Navigate to CMS.
        DESCRIPTION: * Edit the name of any 'Sports Tab'.
        DESCRIPTION: * Save the changes.
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_003__back_to_the_app_refresh_the_page_verify_the_sports_tab_name(self):
        """
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        DESCRIPTION: * Verify the 'Sports Tab' name.
        EXPECTED: * The 'Sports Tab' name is changed according to editions made in CMS
        EXPECTED: * 'Sports Tab' name corresponds to 'label' parameter in <sport-config> response received from CMS
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass
