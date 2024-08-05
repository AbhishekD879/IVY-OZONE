import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59551038_Verify_Betradar_scoreboard_Dimensions_and_CSS_styles_pitch_screen(Common):
    """
    TR_ID: C59551038
    NAME: Verify Betradar scoreboard Dimensions and CSS styles : pitch screen
    DESCRIPTION: Test case verifies Betradar scoreboard Dimensions and CSS styles for the pitch screen
    PRECONDITIONS: 1. Table Tennis event(s) should subscribe to Betradar Scoreboards
    PRECONDITIONS: 2. Event should be in InPlay state
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_inplay_table_tennis_edp_froma_z_menu_table_tennis___inplayorhome___table_tennis___inplay(self):
        """
        DESCRIPTION: Navigate to Inplay Table Tennis EDP from
        DESCRIPTION: A-Z menu table tennis - inplay
        DESCRIPTION: or
        DESCRIPTION: Home - table tennis - inplay
        EXPECTED: Event details page should be open
        """
        pass

    def test_002_click_on_header__table_tennis_league_layout(self):
        """
        DESCRIPTION: click on header : Table tennis league layout
        EXPECTED: 
        """
        pass

    def test_003_click_on_pitch_and_verify_dimensions_and_css_of_header(self):
        """
        DESCRIPTION: click on pitch and verify dimensions and css of header
        EXPECTED: 
        """
        pass

    def test_004_verify_overall_dimension_of_the_screen____click_on_player_name_on_pitch(self):
        """
        DESCRIPTION: verify overall dimension of the screen -  click on player name on pitch
        EXPECTED: 
        """
        pass

    def test_005_verify_font_styles_in_header___click_on_table_tennis_league_text(self):
        """
        DESCRIPTION: Verify font styles in header - click on table tennis league text
        EXPECTED: 
        """
        pass
