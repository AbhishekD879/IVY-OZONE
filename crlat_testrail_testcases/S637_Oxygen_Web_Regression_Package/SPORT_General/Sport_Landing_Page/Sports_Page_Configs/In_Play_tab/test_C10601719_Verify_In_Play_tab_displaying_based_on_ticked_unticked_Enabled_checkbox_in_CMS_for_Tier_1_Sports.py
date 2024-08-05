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
class Test_C10601719_Verify_In_Play_tab_displaying_based_on_ticked_unticked_Enabled_checkbox_in_CMS_for_Tier_1_Sports(Common):
    """
    TR_ID: C10601719
    NAME: Verify 'In-Play' tab displaying based on ticked/unticked 'Enabled' checkbox in CMS  for Tier 1 Sports
    DESCRIPTION: This test case verifies 'In-Play' tab displaying based on ticked/unticked 'Enabled' checkbox in CMS for Tier 1 Sports
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Tier1 Sport Landing page where 'In-Play' tab is enabled in CMS > Sport Pages > Sport Categories > Tier1 sport > 'In-play' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'In-Play' tab is available in CMS for Tier 1 only (but for DESKTOP 'In-Play' tab is available for all Tier types on front-end of app)
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/100267212)
    PRECONDITIONS: ![](index.php?/attachments/get/100267213)
    PRECONDITIONS: - To verify events availability please navigate to Dev Tools > Network > WS > wss://inplay-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket
    """
    keep_browser_open = True

    def test_001_verify_in_play_tab_displaying_if_enabled_checkbox_is_ticked(self):
        """
        DESCRIPTION: Verify 'In-Play' tab displaying if 'Enabled' checkbox is ticked
        EXPECTED: * 'In-Play' tab is present on Sports Landing page
        EXPECTED: * 'In-Play' tab is received in <sport-config> response with **'hidden: false'** parameter
        EXPECTED: * Events received in WS are displayed on the page
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass

    def test_002_verify_in_play_tabs_displaying_if_enabled_checkbox_is_unticked(self):
        """
        DESCRIPTION: Verify 'In-Play' tabs displaying if 'Enabled' checkbox is unticked
        EXPECTED: * 'In-Play' tab is NOT present on Sports Landing page
        EXPECTED: * 'In-Play' tab is received in <sport-config> response with **'hidden: true'** parameter
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        EXPECTED: **For Desktop:**
        EXPECTED: 'In-Play' tab is available all the time. It doesn't depend on ticked or unticked 'Enabled' checkbox.
        """
        pass
