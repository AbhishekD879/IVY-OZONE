import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C48975887_Verify_skeleton_feature_toggle(Common):
    """
    TR_ID: C48975887
    NAME: Verify skeleton feature toggle
    DESCRIPTION: This test case verifies skeleton feature toggle:
    DESCRIPTION: - when turned off, spinners appear across the application
    DESCRIPTION: - when turned on, skeletons should appear across application (for mobile/tablet only)
    DESCRIPTION: Epic related: https://jira.egalacoral.com/browse/BMA-45177
    DESCRIPTION: The following areas listed below (but not limited to) should display spinners/skeletons when toggle is off/on (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen'- unchecked).
    DESCRIPTION: - Landing pages (+ tabs)
    DESCRIPTION: - EDPs (+ tabs)
    DESCRIPTION: - Promotions pages (+ tabs)
    DESCRIPTION: - Virtuals (+ tabs)
    DESCRIPTION: - In play pages
    DESCRIPTION: - My Bets (+ tabs)
    DESCRIPTION: - Betslip opening
    DESCRIPTION: - Loading Bet Receipt
    DESCRIPTION: - Editing ‘My ACCA’ and saving changes
    DESCRIPTION: - Logging out (i.e redirect to home page after user is logged out)
    DESCRIPTION: - Virtuals
    DESCRIPTION: - Home page
    DESCRIPTION: - Banners
    DESCRIPTION: - Scoreboards
    PRECONDITIONS: - App is launched
    PRECONDITIONS: - Skeleton feature in CMS: System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen'
    PRECONDITIONS: - Feature is turned on
    PRECONDITIONS: Note: Desktop stays unaffected by this feature, which means only spinners are displayed for Desktop.
    """
    keep_browser_open = True

    def test_001_navigate_through_app_especially_areas_listed_in_pre_conditions_in_mobiletablet_view(self):
        """
        DESCRIPTION: Navigate through app (especially areas listed in pre-conditions) in mobile/tablet view
        EXPECTED: - Skeletons are displayed when page content loads
        EXPECTED: - No spinners are shown to the user
        """
        pass

    def test_002_turned_the_feature_off_in_cms_and_reload_the_app(self):
        """
        DESCRIPTION: Turned the feature off in CMS and reload the app
        EXPECTED: Feature is turned off
        """
        pass

    def test_003_navigate_through_app_especially_areas_listed_in_pre_conditions_in_mobiletablet_view(self):
        """
        DESCRIPTION: Navigate through app (especially areas listed in pre-conditions) in mobile/tablet view
        EXPECTED: - No skeletons are displayed to the user when page content loads
        EXPECTED: - Spinners are shown
        EXPECTED: - Spinners are not duplicated
        """
        pass
