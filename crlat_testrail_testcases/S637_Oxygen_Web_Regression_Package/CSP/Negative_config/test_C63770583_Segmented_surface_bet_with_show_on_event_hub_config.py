import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C63770583_Segmented_surface_bet_with_show_on_event_hub_config(Common):
    """
    TR_ID: C63770583
    NAME: Segmented surface bet with show on event hub config
    DESCRIPTION: Ideally while configuring any Surfacebet as segmented we should not select anything in show on eventhub
    DESCRIPTION: This tc verify what happen if we config segmented Surfacebet with show on eventhub
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 2) Create or Edit surfacebet with segment =  CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 3) Select one or multiple eventhubs in show on eventhub Make sure suracebet should be in valid date range and all other proper config and save
    """
    keep_browser_open = True

    def test_001_launch_coral_and_lads_appmobile_web_and_verify_universal_view(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web and verify universal view
        EXPECTED: Home - featured or highlights tab should load with as per CMS universal config
        """
        pass

    def test_002_login_with_user_who_mapped_to_segment_as_preconditions(self):
        """
        DESCRIPTION: Login with user who mapped to segment as preconditions
        EXPECTED: Home - featured or highlights tab should load with as per CMS segment config
        """
        pass

    def test_003_navigate_to_eventhub_which_is_selected_while_creating_surface_bet_as_in_pre_condition(self):
        """
        DESCRIPTION: Navigate to eventhub which is selected while creating surface bet as in pre condition
        EXPECTED: 1) Segmented surfacebet in pre condition should not display in eventhub as CSP is not applicable to eventhub
        EXPECTED: 2) Eventhub should display universal surfacebet if it has show in eventhub
        EXPECTED: 3) If we don't have any universal surfacebet with show on eventhub, no surfacebet should display
        EXPECTED: 4) Other content in eventhub should display as per config
        """
        pass
