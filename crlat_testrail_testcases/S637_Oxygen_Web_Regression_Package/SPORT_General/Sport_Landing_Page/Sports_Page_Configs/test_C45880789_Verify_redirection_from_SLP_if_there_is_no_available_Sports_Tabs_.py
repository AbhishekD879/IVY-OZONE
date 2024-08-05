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
class Test_C45880789_Verify_redirection_from_SLP_if_there_is_no_available_Sports_Tabs_(Common):
    """
    TR_ID: C45880789
    NAME: Verify redirection from 'SLP' if there is no available ' Sports Tabs '
    DESCRIPTION: This test case verifies redirection from 'Sports Landing Page' if there is no available 'Sports Tabs' (Sport Tabs are hidden according to the response)
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
    PRECONDITIONS: ![](index.php?/attachments/get/100267212)
    PRECONDITIONS: ![](index.php?/attachments/get/100267213)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 1) Sport Tabs with active 'Check Events' and active 'Has Events' are enabled in CMS for <Sport> (CMS > Sports Pages > Sports Categories > Sport > Sport Tab)
    PRECONDITIONS: 2) At least one Sport Tab with inactive 'Check Events' is enabled in CMS for <Sport> (CMS > Sports Pages > Sports Categories > Sport > Sport Tab)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to <Sport> Landing page
    """
    keep_browser_open = True

    def test_001_verify_sports_tabs_displaying_according_to_received_data_from_cms(self):
        """
        DESCRIPTION: Verify 'Sports Tabs' displaying according to received data from CMS
        EXPECTED: * The 'Sports Tabs' are displayed on the <Sport> Landing Page'
        EXPECTED: * Set of 'Sports Tabs' is displayed according to tabs received from CMS in <sport-config> response (displayed tabs should have **'hidden: false'** parameter)
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass

    def test_002__navigate_to_cms__sport_pages__sport_categories__sport__sport_tab_disable_all_sports_tab_save_the_changes(self):
        """
        DESCRIPTION: * Navigate to CMS > Sport Pages > Sport Categories > Sport > Sport Tab.
        DESCRIPTION: * Disable all 'Sports Tab'.
        DESCRIPTION: * Save the changes.
        EXPECTED: The changes are saved successfully
        """
        pass

    def test_003__back_to_the_app_refresh_the_page(self):
        """
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        EXPECTED: * User redirects to the 'Homepage'
        EXPECTED: * All 'Sports Tabs' received from CMS in <sport-config> response have **'hidden: true'** parameter
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        EXPECTED: *Note:*
        EXPECTED: For Desktop 'In-Play' and 'Matches' tabs are visible all the time
        """
        pass

    def test_004_navigate_to_the_sport_where_no_available_data_on_all_sports_tabs_has_events_for_all_sport_tabs_are_inactive(self):
        """
        DESCRIPTION: Navigate to the <Sport> where no available data on all 'Sports Tabs' ('Has Events' for all Sport Tabs are inactive)
        EXPECTED: * User redirects to the 'Homepage'
        EXPECTED: * All 'Sports Tabs' received from CMS in <sport-config> response have **'hidden: true'** parameter
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        EXPECTED: *Note:*
        EXPECTED: For Desktop 'In-Play' and 'Matches' tabs are visible all the time
        """
        pass
