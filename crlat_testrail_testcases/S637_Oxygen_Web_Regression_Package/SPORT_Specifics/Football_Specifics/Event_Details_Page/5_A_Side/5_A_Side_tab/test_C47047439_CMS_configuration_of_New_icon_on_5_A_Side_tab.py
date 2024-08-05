import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.5_a_side
@vtest
class Test_C47047439_CMS_configuration_of_New_icon_on_5_A_Side_tab(Common):
    """
    TR_ID: C47047439
    NAME: CMS configuration of  'New' icon on  '5-A-Side' tab
    DESCRIPTION: This test case verifies CMS configuration of  'New' icon on  '5-A-Side' tab on Football event details page
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - ‘New’ icon in enabled in CMS > System Configuration > Structure > FiveASide
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To verify the settings for '5-A-Side' tab made in CMS use the following link:
    PRECONDITIONS: https://<particular env e.g. cms-hl.ladbrokes.com>/cms/api/<brand>/initial-data/desktop -> systemConfiguration -> FiveASide
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to event details page that has '5-A-Side' tab
    """
    keep_browser_open = True

    def test_001_verify_new_icon_displaying(self):
        """
        DESCRIPTION: Verify 'New' icon displaying
        EXPECTED: * 'New' icon is displayed on '5-A-Side' tab
        EXPECTED: * <initial-data> response -> systemConfiguration -> FiveASide -> newIcon: true
        """
        pass

    def test_002__navigate_to_cms__systemconfiguration__structure__fiveaside_untick_newicon_checkbox_and_save_changes_refresh_the_page_on_frontend_verify_new_icon_displaying(self):
        """
        DESCRIPTION: * Navigate to CMS > SystemConfiguration > Structure > FiveASide
        DESCRIPTION: * Untick 'newIcon' checkbox and save changes
        DESCRIPTION: * Refresh the page on frontend
        DESCRIPTION: * Verify 'New' icon displaying
        EXPECTED: * 'New' icon is NOT displayed on '5-A-Side' tab
        EXPECTED: * <initial-data> response -> systemConfiguration -> FiveASide -> newIcon: false
        """
        pass
