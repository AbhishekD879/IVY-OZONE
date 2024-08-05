import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2876229_To_Delete_Verify_Country_segment_is_removed_from_Featured_when_all_meetings_in_it_are_resulted(Common):
    """
    TR_ID: C2876229
    NAME: [To Delete] Verify Country segment is removed from Featured when all meetings in it are resulted
    DESCRIPTION: **This functionality was descoped and not implemented.**
    DESCRIPTION: This test case verifies that International Races country segment is removed from Featured tab when all meetings in it were resulted.
    PRECONDITIONS: * TI tool: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: * International Horse Racing events are available
    PRECONDITIONS: 'Is Intenational' checkbox is marked in TI on a type level (typeFlagCodes:INT)
    PRECONDITIONS: * At least 1 meetings exist for one country segment
    PRECONDITIONS: * Note: Business will use only ONE location flag (UK/US/ZA/AE/CL/IN/AU/FR/INT/IE/VR)
    PRECONDITIONS: * Look at the attributes:
    PRECONDITIONS: * isFinished = 'true' on event level - to check whether event is finished
    PRECONDITIONS: * isResulted='true' on event level - to check whether event is resulted
    PRECONDITIONS: * User is on Horse Racing landing page
    """
    keep_browser_open = True

    def test_001_in_ti_tool_result_all_events_in_all_meetings_from_preconditions(self):
        """
        DESCRIPTION: In TI tool result all events in all meetings from preconditions
        EXPECTED: 
        """
        pass

    def test_002_in_app_refresh_page_and_verify_resulted_meeting_on_hr_featured_tab(self):
        """
        DESCRIPTION: In app refresh page and verify resulted meeting on HR Featured tab
        EXPECTED: The country segment where all meetings were resulted is not displayed on Featured tab
        """
        pass
