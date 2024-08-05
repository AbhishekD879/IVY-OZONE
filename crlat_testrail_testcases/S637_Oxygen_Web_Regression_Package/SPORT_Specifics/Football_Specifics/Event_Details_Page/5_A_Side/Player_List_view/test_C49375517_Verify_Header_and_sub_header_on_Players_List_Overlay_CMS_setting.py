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
class Test_C49375517_Verify_Header_and_sub_header_on_Players_List_Overlay_CMS_setting(Common):
    """
    TR_ID: C49375517
    NAME: Verify Header and sub-header on Players List Overlay (CMS setting)
    DESCRIPTION: This test case verifies Players List Overlay Header and sub header.
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP, '5 A Side' sub tab (event type described above) -> User selected player position from pitch overlay-> User on the Players List View
    """
    keep_browser_open = True

    def test_001_open_cms_byb__5a_side_select_formation_and_set_position_and_stat(self):
        """
        DESCRIPTION: Open CMS (BYB-> 5A side, select formation) and set Position and stat.
        EXPECTED: Position and stat are set accordingly.
        """
        pass

    def test_002_load_app_open_players_list_view_and_verify_position_and_stat_names_list_in_the_drop_down_which_were_set_in_the_first_step(self):
        """
        DESCRIPTION: Load App, Open Players List View and verify Position and stat names list in the drop down which were set in the first step
        EXPECTED: - Position and stat names correspond to those set in the CMS.
        EXPECTED: - On UI below Add a <Position> Stat name is displayed in blue with a chevron and on clicking the Chevron avaiable Stat names are displayed
        EXPECTED: - ' to Keep a Clean Sheet - {value}',
        EXPECTED: - ' to be Carded -  {value}',
        EXPECTED: - ' to Concede  {value} Goals',
        EXPECTED: - ' to win {value} Tackles',
        EXPECTED: - ' to have {value} Crosses',
        EXPECTED: - ' to make {value} Passes',
        EXPECTED: - ' to have {value} Assists',
        EXPECTED: - ' to have {value} Shots',
        EXPECTED: - ' to have {value} Offsides',
        EXPECTED: - ' to have {value} Shots On Target',
        EXPECTED: - ' to have {value} Shots Outside The Box',
        EXPECTED: - ' to score {value} Goals',
        EXPECTED: - ' to score {value} Goals Inside The Box',
        EXPECTED: - ' to score {value} Goals Outside The Box',
        EXPECTED: ![](index.php?/attachments/get/122292711)
        """
        pass

    def test_003_open_cms_and_change_position_and_stat_names_one_more_time(self):
        """
        DESCRIPTION: Open CMS and change Position and stat names one more time.
        EXPECTED: Position and stat names are changed.
        """
        pass

    def test_004_return_to_the_app_and_open_players_list_view_one_more_time(self):
        """
        DESCRIPTION: Return to the app and open Players List View one more time.
        EXPECTED: Position and stat on the UI are updated accordingly.
        """
        pass

    def test_005_in_cms_byb__5a_side_left_position_field_empty_save_changes(self):
        """
        DESCRIPTION: In CMS (BYB-> 5A side) left Position field empty, save changes.
        EXPECTED: Changes are saved.
        """
        pass

    def test_006_return_to_the_app_and_open_players_list_view_one_more_time(self):
        """
        DESCRIPTION: Return to the app and open Players List View one more time.
        EXPECTED: User sees Title 'Add Player'.
        EXPECTED: ![](index.php?/attachments/get/122292712)
        """
        pass
