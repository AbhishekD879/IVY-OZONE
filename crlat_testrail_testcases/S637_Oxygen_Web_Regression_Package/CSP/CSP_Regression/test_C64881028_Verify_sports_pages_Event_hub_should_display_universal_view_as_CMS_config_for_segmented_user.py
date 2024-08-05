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
class Test_C64881028_Verify_sports_pages_Event_hub_should_display_universal_view_as_CMS_config_for_segmented_user(Common):
    """
    TR_ID: C64881028
    NAME: Verify sports pages/Event hub should display universal view as CMS config for segmented user
    DESCRIPTION: This test cases verifies all sports pages for segmented user
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_login_with_segmented_user_as_per_precondtion(self):
        """
        DESCRIPTION: Login with segmented user as per precondtion
        EXPECTED: Segmented data should displayed in HOME PAGE
        """
        pass

    def test_003_navigate_to_sports_pagesevent_hub_and_verify(self):
        """
        DESCRIPTION: Navigate to Sports pages/Event hub and verify
        EXPECTED: as CSP is not applicable for sports pages /Event hub,user should see Unviversal view.
        """
        pass
