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
class Test_C9240592_Displaying_of_In_Play_module_on_Featured_tab_and_SLP_based_on_enabled_option_set_on_CMS(Common):
    """
    TR_ID: C9240592
    NAME: Displaying of 'In-Play' module on 'Featured' tab and SLP based on "enabled" option set on CMS
    DESCRIPTION: This test case verifies the displaying of 'In-Play' module on 'Featured' tab and SLP based on "enabled" option set on CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: * To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: * CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: * TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: * 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module (for 'Featured' tab)
    PRECONDITIONS: * At least 1 Sport with Live event is added in CMS > Sports Pages > Homepage > In-Play module > Add Sport > Set number of events for Sport (for 'Featured' tab)
    PRECONDITIONS: * 'In-Play' module should be 'Active' in CMS > Sports Pages > Sport Categories > Sport > In-Play module and 'Inplay Event Count' should contain positive value (for SLP)
    """
    keep_browser_open = True

    def test_001__in_cms__system_configuration__structure__in_play_module___disable_the_in_play_module_in_application_refresh_the_page_and_verify_in_play_module_displaying(self):
        """
        DESCRIPTION: * In CMS > System configuration > Structure > In-Play module - disable the 'In-Play' module
        DESCRIPTION: * In application refresh the page and verify 'In-Play' module displaying
        EXPECTED: 'In-Play' module is NOT displayed on 'Featured' tab and on SLP
        """
        pass

    def test_002__in_cms__system_configuration__structure__in_play_module___enable_the_in_play_module_in_application_refresh_the_page_and_verify_in_play_module_displaying(self):
        """
        DESCRIPTION: * In CMS > System configuration > Structure > In-Play module - enable the 'In-Play' module
        DESCRIPTION: * In application refresh the page and verify 'In-Play' module displaying
        EXPECTED: 'In-Play' module is displayed on 'Featured' tab and on SLP
        """
        pass
