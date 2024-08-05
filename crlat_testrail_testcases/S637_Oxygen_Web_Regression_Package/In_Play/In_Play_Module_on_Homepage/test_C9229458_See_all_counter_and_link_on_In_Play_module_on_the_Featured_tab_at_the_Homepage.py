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
class Test_C9229458_See_all_counter_and_link_on_In_Play_module_on_the_Featured_tab_at_the_Homepage(Common):
    """
    TR_ID: C9229458
    NAME: 'See all' counter and link on 'In-Play' module on the 'Featured' tab at the Homepage
    DESCRIPTION: This test case verifies 'See all' counter and link on 'In-Play' module on the 'Featured' tab at the Homepage
    DESCRIPTION: AUTOTEST [C10841418]
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: 3. 'In-Play' module with live events is displayed in 'Featured' tab
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - At least 2 Sports with Live event are added in CMS > Sports Pages > Homepage > In-Play module > Add Sport > Set number of events for Sport
    PRECONDITIONS: - To check data received in featured-sports MS open Dev Tools > Network > WS > featured-sports
    """
    keep_browser_open = True

    def test_001_verify_see_all_link_within_in_play_module(self):
        """
        DESCRIPTION: Verify 'See all' link within 'In-Play' module
        EXPECTED: 'See all' link is located in the header of 'In-Play' module
        """
        pass

    def test_002_verify_counter_within_see_all_link(self):
        """
        DESCRIPTION: Verify counter within 'See all' link
        EXPECTED: * Counter shows the total number of in-play events for all Sports
        EXPECTED: * Value in Counter corresponds to 'totalEvents' attribute in WS
        """
        pass

    def test_003_tap_on_see_all_link(self):
        """
        DESCRIPTION: Tap on 'See all' link
        EXPECTED: The user navigates to 'In-play' page the first Sports tab is selected by default e.g. In-play > Football
        """
        pass
