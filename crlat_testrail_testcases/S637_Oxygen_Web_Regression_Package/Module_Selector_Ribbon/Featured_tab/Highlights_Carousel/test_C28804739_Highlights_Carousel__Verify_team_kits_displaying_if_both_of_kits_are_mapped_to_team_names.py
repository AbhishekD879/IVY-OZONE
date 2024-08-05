import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C28804739_Highlights_Carousel__Verify_team_kits_displaying_if_both_of_kits_are_mapped_to_team_names(Common):
    """
    TR_ID: C28804739
    NAME: Highlights Carousel - Verify team kits displaying if both of kits are mapped to team names
    DESCRIPTION: This test case verifies displaying of team kits of events cards in Highlights Carousels if both of kits are mapped to team names
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS:
    PRECONDITIONS: * Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: * Sport Pages > Sport Categories > Sport > Highlights Carousel
    PRECONDITIONS: - You should have active Highlights Carousels with active events in CMS. Make sure that Highlights Carousel configured by TypeID
    PRECONDITIONS: - Team kits are mapped to teams by names (e.g. to show team kit for Manchester United team name should be "Man-United"). Refer to the attached files to see team names for mapping
    PRECONDITIONS: - TypeID must be from Premier League or Champions League to display the team kits
    """
    keep_browser_open = True

    def test_001_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_if_team_name_has_mapped_team_kit(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels if team name has mapped team kit
        EXPECTED: Team kits are displayed correctly according to mapped teams in Highlights Carousel configured by TypeID
        """
        pass

    def test_002_navigate_to_the_some_sports_landing_page_and_repeat_the_step_1(self):
        """
        DESCRIPTION: Navigate to the some Sports Landing page and repeat the step 1
        EXPECTED: 
        """
        pass
