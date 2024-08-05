import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C8211978_Events_ordering_in_Sports_accordion_within_In_Play_module_on_the_Featured_tab(Common):
    """
    TR_ID: C8211978
    NAME: Events ordering in 'Sports' accordion within 'In-Play' module on the 'Featured' tab
    DESCRIPTION: This test case verifies events ordering in 'Sports' accordion within 'In-Play' module on the 'Featured' tab
    DESCRIPTION: Autotest [C10559418]
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: 3. 'In-Play' module with live events is displayed in 'Featured' tab
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - At least 2 Sports with Live event from different Types are added in CMS > Sports Pages > Homepage > In-Play module > Add Sport > Set number of events for Sport
    PRECONDITIONS: - To check data received in featured-sports MS open Dev Tools > Network > WS > featured-sports
    """
    keep_browser_open = True

    def test_001_verify_events_ordering_in_sports_accordion_within_in_play_module(self):
        """
        DESCRIPTION: Verify Events ordering in 'Sports' accordion within 'In-Play' module
        EXPECTED: Ordering is as follows:
        EXPECTED: * Sport <Classes> are ordered based on 'classDisplayOrder' attribute from TI in ascending where minus ordinals are displayed first
        EXPECTED: * Sport <Types> within each class are ordered based on 'typeDisplayOrder' attribute from TI in ascending
        EXPECTED: * The events from the same <Type>(Competition) are ordered in the following way:
        EXPECTED: * 'startTime' - chronological order in the first instance
        EXPECTED: * Event 'displayOrder' in ascending
        EXPECTED: * Alphabetical order
        """
        pass
