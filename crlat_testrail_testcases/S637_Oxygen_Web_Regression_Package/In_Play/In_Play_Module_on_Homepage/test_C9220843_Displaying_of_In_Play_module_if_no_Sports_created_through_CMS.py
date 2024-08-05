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
class Test_C9220843_Displaying_of_In_Play_module_if_no_Sports_created_through_CMS(Common):
    """
    TR_ID: C9220843
    NAME: Displaying of 'In-Play' module if no Sports created through CMS
    DESCRIPTION: This test case verifies 'In-Play' module displaying if no Sports created through CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    """
    keep_browser_open = True

    def test_001_in_cms__sport_pages__homepage__in_play_module_set_some_positive_value_to_in_play_event_count_field_do_not_add_any_sports_save_changes(self):
        """
        DESCRIPTION: In CMS > Sport Pages > Homepage > 'In-Play' module:
        DESCRIPTION: * Set some positive value to 'In-Play Event Count' field
        DESCRIPTION: * Do NOT add any Sports
        DESCRIPTION: * Save Changes
        EXPECTED: Changes for In-Play module are saved
        """
        pass

    def test_002_verify_in_play_module_displaying(self):
        """
        DESCRIPTION: Verify 'In-Play' module displaying
        EXPECTED: 'In-Play' module is NOT displayed
        """
        pass
