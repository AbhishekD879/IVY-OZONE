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
class Test_C10700370_Verify_In_Play_tab_on_Sports_Landing_page_for_Tier_2_Sports(Common):
    """
    TR_ID: C10700370
    NAME: Verify 'In-Play' tab on Sports Landing page for Tier 2 Sports
    DESCRIPTION: This test case verifies 'In-Play' tab on Sports Landing page for Tier 2 Sports
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'In-Play' tab is **NOT** available in CMS for **Tier 2** Sports
    PRECONDITIONS: - Be aware that 'In-Play' tab is hardcoded for Desktop and it's not CMS configurable. It means that 'In-Play' tab will be displayed all the time regardless of data availability.
    PRECONDITIONS: - To verify events availability please navigate to Dev Tools > Network > WS > wss://inplay-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Tier2 Sports Landing page
    """
    keep_browser_open = True

    def test_001_verify_in_play_tab_displaying_on_sports_landing_page_in_case_events_are_available(self):
        """
        DESCRIPTION: Verify 'In-Play' tab displaying on Sports Landing page in case events are available
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: 'In-Play' tab is NOT displayed on the Sports Landing page
        EXPECTED: **For Desktop:**
        EXPECTED: * 'In-Play' tab is present on Sports Landing page
        EXPECTED: * Events are received in WS are displayed on the page
        """
        pass

    def test_002_verify_in_play_tab_displaying_on_sports_landing_page_in_case_events_are_not_available(self):
        """
        DESCRIPTION: Verify 'In-Play' tab displaying on Sports Landing page in case events are NOT available
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: 'In-Play' tab is NOT displayed on the Sports Landing page
        EXPECTED: **For Desktop:**
        EXPECTED: * 'In-Play' tab is present on Sports Landing page
        EXPECTED: * Events are NOT received in WS and are NOT displayed on the page
        EXPECTED: * 'There are currently no Live events available'(For Live Now tab) or 'There are currently no upcoming Live events available'(for Upcoming tab) message is present
        """
        pass
