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
class Test_C2861796_To_Delete_Verify_International_meeting_with_all_events_resulted_is_dropped_to_the_bottom_of_the_respective_country_segment(Common):
    """
    TR_ID: C2861796
    NAME: [To Delete] Verify International meeting with all events resulted is dropped to the bottom of the respective country segment
    DESCRIPTION: **This functionality was descoped and not implemented.**
    DESCRIPTION: This test case verifies that International meeting with all events resulted is drop to the bottom of the respective country segment
    PRECONDITIONS: * TI tool: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: * International Horse Racing events are available
    PRECONDITIONS: 'Is Intenational' checkbox is marked in TI on a type level (typeFlagCodes:INT)
    PRECONDITIONS: * At least 3 meetings exist for one country segment
    PRECONDITIONS: * Request on Horse Racing Landing page: EventToOutcomeForClass/{class_ids}1?simpleFilter=event.categoryId:intersects:21&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:UK,US,ZA,AE,CL,IN,AU,FR,INT,IE,VR
    PRECONDITIONS: * Request on EDP: PoolForEvent/ {event_id} ?&translationLang=en
    PRECONDITIONS: * Note: Business will use only ONE location flag (UK/US/ZA/AE/CL/IN/AU/FR/INT/IE/VR)
    PRECONDITIONS: * Look at the attributes:
    PRECONDITIONS: isFinished = 'true' on event level - to check whether event is finished
    PRECONDITIONS: isResulted='true' on event level - to check whether event is resulted
    PRECONDITIONS: * User is on Horse Racing landing page
    """
    keep_browser_open = True

    def test_001_in_ti_tool_result_all_events_in_2_of_the_meetings_from_preconditions(self):
        """
        DESCRIPTION: In TI tool result all events in 2 of the meetings from preconditions
        EXPECTED: 
        """
        pass

    def test_002_in_app_refresh_page_and_verify_resulted_meeting_on_hr_featured_tab(self):
        """
        DESCRIPTION: In app refresh page and verify resulted meeting on HR Featured tab
        EXPECTED: * Resulted meeting is dropped to the bottom of the respective country segment
        EXPECTED: * Resulted meeting displayed in Openbet display order
        """
        pass
