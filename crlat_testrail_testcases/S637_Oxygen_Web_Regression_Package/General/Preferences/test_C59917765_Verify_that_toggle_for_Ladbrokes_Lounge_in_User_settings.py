import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.timeline
@vtest
class Test_C59917765_Verify_that_toggle_for_Ladbrokes_Lounge_in_User_settings(Common):
    """
    TR_ID: C59917765
    NAME: Verify that toggle for Ladbrokes Lounge in User settings
    DESCRIPTION: This test case verifies toggle to switch timeline on/off in User settings
    PRECONDITIONS: - Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox )
    PRECONDITIONS: - Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: - Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: - Live Campaign is created
    PRECONDITIONS: - User is logged In
    """
    keep_browser_open = True

    def test_001_tap_on_avatar_icon_or_balance_button___settings___betting_settings(self):
        """
        DESCRIPTION: Tap on avatar icon or balance button -> Settings -> Betting Settings
        EXPECTED: - Settings page is opened
        EXPECTED: - 'Ladbrokes Lounge' option is present
        EXPECTED: - Text 'Display Ladbrokes Lounge when I login.' is present
        EXPECTED: ![](index.php?/attachments/get/119423187)
        """
        pass

    def test_002_verify_default_value_set_for_ladbrokes_lounge_option(self):
        """
        DESCRIPTION: Verify default value set for 'Ladbrokes Lounge' option
        EXPECTED: Default value is 'ON'
        """
        pass

    def test_003_go_to_page_where_timeline_ladbrokes_lounge_is_configured(self):
        """
        DESCRIPTION: Go to page where Timeline (Ladbrokes Lounge) is configured
        EXPECTED: - Ladbrokes Lounge should be visible on page above the footer
        """
        pass

    def test_004_tap_on_avatar_icon_or_balance_button___settings___betting_settingsand_turn_off_ladbrokes_lounge(self):
        """
        DESCRIPTION: Tap on avatar icon or balance button -> Settings -> Betting Settings
        DESCRIPTION: and Turn Off 'Ladbrokes Lounge'
        EXPECTED: - Ladbrokes Lounge should NOT be visible on page above the footer
        """
        pass
