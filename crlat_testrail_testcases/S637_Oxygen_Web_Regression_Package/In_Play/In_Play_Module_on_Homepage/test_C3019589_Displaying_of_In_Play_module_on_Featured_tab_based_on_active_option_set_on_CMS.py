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
class Test_C3019589_Displaying_of_In_Play_module_on_Featured_tab_based_on_active_option_set_on_CMS(Common):
    """
    TR_ID: C3019589
    NAME: Displaying of 'In-Play' module on 'Featured' tab based on "active" option set on CMS
    DESCRIPTION: This test case verifies displaying of 'In-Play' module on 'Featured' tab based on "active" option set on CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - At least 1 Sport with Live event is added in CMS > Sports Pages > Homepage > In-Play module > Add Sport > Set number of events for Sport
    """
    keep_browser_open = True

    def test_001_verify_in_play_module_displaying(self):
        """
        DESCRIPTION: Verify 'In-Play' module displaying
        EXPECTED: 'In-Play' module with live events is displayed in 'Featured' tab
        """
        pass

    def test_002__in_cms__sport_pages__homepage__in_play_module___deactivate_the_in_play_module_in_application_do_not_refresh_the_page_and_verify_in_play_module(self):
        """
        DESCRIPTION: * In CMS > Sport Pages > Homepage > 'In-Play' module - deactivate the 'In-Play' module
        DESCRIPTION: * In application DO NOT refresh the page and verify 'In-Play' module
        EXPECTED: 'In-Play' module disappears from the page
        """
        pass

    def test_003__in_cms__sport_pages__homepage__in_play_module___activate_the_in_play_module_in_application_do_not_refresh_the_page_and_verify_in_play_module(self):
        """
        DESCRIPTION: * In CMS > Sport Pages > Homepage > 'In-Play' module - activate the 'In-Play' module
        DESCRIPTION: * In application DO NOT refresh the page and verify 'In-Play' module
        EXPECTED: 'In-Play' module appears on the page
        """
        pass
