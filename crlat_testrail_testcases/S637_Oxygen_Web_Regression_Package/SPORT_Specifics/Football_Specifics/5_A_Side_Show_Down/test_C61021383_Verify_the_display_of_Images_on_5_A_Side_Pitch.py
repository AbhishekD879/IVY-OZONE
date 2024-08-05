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
class Test_C61021383_Verify_the_display_of_Images_on_5_A_Side_Pitch(Common):
    """
    TR_ID: C61021383
    NAME: Verify the display of Images on 5-A Side Pitch
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

    def test_002_asset_management_is_created_for_both_teams_with_image_click_on_build_team_and_validate_the_crestimage_display_click_on_add_player_plus_icon_and_validate_the_display_in_player_lists_add_player_and_validate_player_icons_on_pitch_view(self):
        """
        DESCRIPTION: **Asset Management is created for both Teams (With Image)**
        DESCRIPTION: * Click on Build Team and Validate the crest/Image display
        DESCRIPTION: * Click on Add Player (+) icon and Validate the display in Player Lists
        DESCRIPTION: * Add Player and Validate Player icons on Pitch View
        EXPECTED: **Display on Five A Side= ON**
        EXPECTED: (Both Teams should be ON)
        EXPECTED: * User should be displayed with Images uploaded in CMS on Pitch View Header, Player List & Player Icons
        EXPECTED: * Images should be displayed as per designs
        EXPECTED: **Display on Five A Side= OFF**
        EXPECTED: (If any one Team is OFF or both Teams OFF)
        EXPECTED: * User should be displayed with Crest Colors configured in CMS (Primary & Secondary Colors) on Pitch View Header, Player List & Player Icons
        """
        pass
