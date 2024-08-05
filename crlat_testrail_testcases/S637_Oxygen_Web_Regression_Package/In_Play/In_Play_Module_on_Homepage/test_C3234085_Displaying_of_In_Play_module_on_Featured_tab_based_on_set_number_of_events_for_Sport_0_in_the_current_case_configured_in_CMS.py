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
class Test_C3234085_Displaying_of_In_Play_module_on_Featured_tab_based_on_set_number_of_events_for_Sport_0_in_the_current_case_configured_in_CMS(Common):
    """
    TR_ID: C3234085
    NAME: Displaying of 'In Play' module on 'Featured' tab based on set number of events for Sport ('0' in the current case) configured in CMS
    DESCRIPTION: This test case verifies displaying of 'In Play' module on 'Featured' tab based on set number of events for Sport ('0' in the current case) configured in CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - Set some positive value for 'In-Play Event Count' in CMS > Sports Pages > Homepage > In-Play module
    """
    keep_browser_open = True

    def test_001_in_cms__sports_pages__homepage__in_play_module_set_sport_event_count_for_all_sports_to_0_and_save_changes(self):
        """
        DESCRIPTION: In CMS > Sports Pages > Homepage > 'In-Play' module:
        DESCRIPTION: * Set Sport Event Count for ALL SPORTS to 0 and save changes
        EXPECTED: Changes for 'In-Play' module are saved
        """
        pass

    def test_002_verify_in_play_module_displaying_note__it_usually_syncs_in_few_seconds_but_cms_sync_be_delayed_even_by_15_minutes_in_worst_cases_(self):
        """
        DESCRIPTION: Verify 'In-Play' module displaying (note: _it usually syncs in few seconds but CMS sync be delayed even by 15 minutes in worst cases_)
        EXPECTED: 'In-Play' module is NOT displayed
        """
        pass
