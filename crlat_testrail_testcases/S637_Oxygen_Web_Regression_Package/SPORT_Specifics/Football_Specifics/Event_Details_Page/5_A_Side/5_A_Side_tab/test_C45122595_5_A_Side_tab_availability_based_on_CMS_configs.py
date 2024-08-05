import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C45122595_5_A_Side_tab_availability_based_on_CMS_configs(Common):
    """
    TR_ID: C45122595
    NAME: '5-A-Side' tab availability based on CMS configs
    DESCRIPTION: This test case verifies '5-A-Side' tab availability based on CMS configs (feature toggle and league being enabled for 5-A-Side)
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request  to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To verify the settings for '5-A-Side' tab made in CMS use the following link:
    PRECONDITIONS: https://<particular env e.g. cms-hl.ladbrokes.com>/cms/api/<brand>/initial-data/desktop -> systemConfiguration -> FiveASide
    PRECONDITIONS: ![](index.php?/attachments/get/74407491)
    PRECONDITIONS: * To verify the activated leagues for '5-A-Side' tab in CMS use the following link:
    PRECONDITIONS: https://<particular env e.g. cms-hl.ladbrokes.com>/api/<brand>/yc-leagues -> <type> -> activeFor5aSide
    PRECONDITIONS: ![](index.php?/attachments/get/75401430)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    """
    keep_browser_open = True

    def test_001_verify_5_a_side_tab_availability(self):
        """
        DESCRIPTION: Verify '5-A-Side' tab availability
        EXPECTED: * '5-A-Side' tab is displayed on event details page
        EXPECTED: * <initial-data> response -> systemConfiguration -> FiveASide -> enabled: true
        """
        pass

    def test_002__disable_fiveaside_in_cms__system_configuration___structure_and_save_changes_refresh_event_details_page_on_frontend(self):
        """
        DESCRIPTION: * Disable FiveASide in CMS > System Configuration -> Structure and save changes
        DESCRIPTION: * Refresh event details page on frontend
        EXPECTED: * '5-A-Side' tab is NOT displayed on event details page
        EXPECTED: * <initial-data> response -> systemConfiguration -> FiveASide -> enabled: false
        """
        pass

    def test_003__enable_fiveaside_in_cms__system_configuration___structure_and_save_changes_untick_active_for_5_a_side_in_cms___byb___banach_leagues___select_league_under_test_refresh_event_details_page_on_frontend(self):
        """
        DESCRIPTION: * Enable FiveASide in CMS > System Configuration -> Structure and save changes
        DESCRIPTION: * Untick 'Active for 5 A Side' in CMS -> BYB -> Banach Leagues -> select league under test
        DESCRIPTION: * Refresh event details page on frontend
        EXPECTED: * '5-A-Side' tab is NOT displayed on event details page
        EXPECTED: * <initial-data> response -> systemConfiguration -> FiveASide -> enabled: true
        EXPECTED: * <yc-leagues> response -> <type> -> activeFor5aSide: false
        """
        pass
