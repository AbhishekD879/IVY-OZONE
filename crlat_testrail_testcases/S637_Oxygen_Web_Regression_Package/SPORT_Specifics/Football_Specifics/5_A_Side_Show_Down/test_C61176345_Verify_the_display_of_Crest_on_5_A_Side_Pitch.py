import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C61176345_Verify_the_display_of_Crest_on_5_A_Side_Pitch(Common):
    """
    TR_ID: C61176345
    NAME: Verify the display of Crest on 5-A Side Pitch
    DESCRIPTION: This test case verifies the display of Images/crest on
    DESCRIPTION: 1: Pitch View Header
    DESCRIPTION: 2: Player Icons
    DESCRIPTION: 3: Player Lists
    PRECONDITIONS: 1: User should have access to CMS
    PRECONDITIONS: **CMS CONFIGURATIONS**
    PRECONDITIONS: CMS > BYB > ASSET MANAGEMENT > CREATE ASSET MANAGAMENT
    """
    keep_browser_open = True

    def test_001_navigate_to_football_landing_page__football_event_details_page__5_a_side_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing Page > Football Event Details Page > 5-A Side tab
        EXPECTED: * User should be able to view Build Team Button
        """
        pass

    def test_002_asset_management_is_created_for_both_teams_only_one_team_has_image_click_on_build_team_and_validate_the_crestimage_display_click_on_add_player_plus_icon_and_validate_the_display_in_player_lists_add_player_and_validate_player_icons_on_pitch_view(self):
        """
        DESCRIPTION: **Asset Management is created for both Teams (Only One Team has Image)**
        DESCRIPTION: * Click on Build Team and Validate the crest/Image display
        DESCRIPTION: * Click on Add Player (+) icon and Validate the display in Player Lists
        DESCRIPTION: * Add Player and Validate Player icons on Pitch View
        EXPECTED: * User should be displayed with Crest Colors configured in CMS (Primary & Secondary Colors) on Pitch View Header, Player List & Player Icons
        """
        pass

    def test_003_asset_management_is_created_for_only_one_team_click_on_build_team_and_validate_the_crestimage_display_click_on_add_player_plus_icon_and_validate_the_display_in_player_lists_add_player_and_validate_player_icons_on_pitch_view(self):
        """
        DESCRIPTION: **Asset Management is created for only one Team**
        DESCRIPTION: * Click on Build Team and Validate the crest/Image display
        DESCRIPTION: * Click on Add Player (+) icon and Validate the display in Player Lists
        DESCRIPTION: * Add Player and Validate Player icons on Pitch View
        EXPECTED: * Default Crest colors should be displayed
        """
        pass

    def test_004_asset_management_is_created_for_both_teams_no_image_click_on_build_team_and_validate_the_crestimage_display_click_on_add_player_plus_icon_and_validate_the_display_in_player_lists_add_player_and_validate_player_icons_on_pitch_view(self):
        """
        DESCRIPTION: **Asset Management is created for both Teams (No Image)**
        DESCRIPTION: * Click on Build Team and Validate the crest/Image display
        DESCRIPTION: * Click on Add Player (+) icon and Validate the display in Player Lists
        DESCRIPTION: * Add Player and Validate Player icons on Pitch View
        EXPECTED: * User should be displayed with Crest Colors configured in CMS (Primary & Secondary Colors) on Pitch View Header, Player List & Player Icons
        """
        pass

    def test_005_asset_management_is_not_created_for_both_teams_click_on_build_team_and_validate_the_crestimage_display_click_on_add_player_plus_icon_and_validate_the_display_in_player_lists_add_player_and_validate_player_icons_on_pitch_view(self):
        """
        DESCRIPTION: **Asset Management is NOT created for both Teams**
        DESCRIPTION: * Click on Build Team and Validate the crest/Image display
        DESCRIPTION: * Click on Add Player (+) icon and Validate the display in Player Lists
        DESCRIPTION: * Add Player and Validate Player icons on Pitch View
        EXPECTED: * Default Crest colors should be displayed
        """
        pass
