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
class Test_C49375536_Verify_Crests_colors_on_Players_List_Overlay_CMS_setting(Common):
    """
    TR_ID: C49375536
    NAME: Verify Crests colors on Players List Overlay (CMS setting)
    DESCRIPTION: This test case verifies Players List Overlay.
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP, '5 A Side' sub tab (event type described above)-> User selected player position from pitch overlay-> User on the Players List View
    """
    keep_browser_open = True

    def test_001_open_cms_byb__asset_management__team_selected_primarysecondary_colors_and_set_colors_for_the_team(self):
        """
        DESCRIPTION: Open CMS (BYB-> Asset Management-> Team selected: Primary/Secondary colors) and set colors for the team.
        EXPECTED: Colors are saved accordingly in CMS.
        """
        pass

    def test_002_load_app_open_players_list_view_and_verify_crests_colors_which_were_set_in_the_first_step(self):
        """
        DESCRIPTION: Load App, Open Players List View and verify crests' colors which were set in the first step
        EXPECTED: Colors on UI correspond to the ones set in CMS
        EXPECTED: ![](index.php?/attachments/get/59323450)
        """
        pass

    def test_003_check_the_call_to_cms_asset_management_in_network___all(self):
        """
        DESCRIPTION: Check the call to CMS (asset-management) in 'Network' -> 'All'
        EXPECTED: Corresponding 'primaryColour'/'secondaryColour' are sent from CMS
        EXPECTED: ![](index.php?/attachments/get/74407416)
        """
        pass

    def test_004_open_cms_and_change_colors_for_the_teams_one_more_time(self):
        """
        DESCRIPTION: Open CMS and change colors for the teams one more time.
        EXPECTED: Colors saved accordingly in CMS.
        """
        pass

    def test_005_return_to_the_app_open_players_list_view_and_refresh_page(self):
        """
        DESCRIPTION: Return to the app, open Players List View and refresh page.
        EXPECTED: Colors on the UI are the same which were set on the CMS
        """
        pass
