import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C8146749_Count_of_live_events_displayed_on_In_Play_module_on_SLP_based_on_CMS_config(Common):
    """
    TR_ID: C8146749
    NAME: Count of live events displayed on 'In-Play' module on SLP based on CMS config
    DESCRIPTION: This test case verifies that number of live events, displayed within 'In-Play' module on SLP, is based on CMS config
    DESCRIPTION: AUTOTEST [C10621022]
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: - 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: - 'In-Play' module is created in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: - 'In-play' module is set to 'Active'
    PRECONDITIONS: - 'Inplay event count' is set to e.g. 5
    PRECONDITIONS: 2) Sport (e.g. Football) with available live events within several types created in OB e.g.:
    PRECONDITIONS: * Championship (e.g."typeDisplayOrder": 1), events available: 4
    PRECONDITIONS: * Premier League (e.g. "typeDisplayOrder": 2), events available: 3
    PRECONDITIONS: * League Two (e.g. "typeDisplayOrder": 3), events available: 3
    PRECONDITIONS: Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: Open 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_total_count_of_live_events_displayed_within_in_play_module(self):
        """
        DESCRIPTION: Verify total count of live events displayed within 'In-Play' module
        EXPECTED: 5 in-play events are displayed (corresponds to number, set in 'Inplay event count' field in CMS)
        """
        pass

    def test_002_verify_events_grouping(self):
        """
        DESCRIPTION: Verify events grouping
        EXPECTED: * Events are grouped by OB Class/TypeID and sorted by Class 'displayOrder' and type 'DisplayOrder' in ascending
        """
        pass

    def test_003_verify_events_displayed_within_in_play_module_based_on_set_up_from_pre_conditions(self):
        """
        DESCRIPTION: Verify events displayed within 'In-Play' module (based on set up from pre-conditions)
        EXPECTED: * 4 events of 'Championship' type are displayed
        EXPECTED: * 1 event of 'Premier League' type is displayed
        EXPECTED: * 0 events of 'League Two' type
        """
        pass

    def test_004__in_cms_set_inplay_event_count_to_20_in_application_refresh_the_page_and_verify_count_of_live_events_displayed(self):
        """
        DESCRIPTION: * In CMS set 'Inplay event count' to 20
        DESCRIPTION: * In application refresh the page and verify count of live events displayed
        EXPECTED: All available live events are displayed i.e. 10 (based on set up from pre-conditions)
        """
        pass
