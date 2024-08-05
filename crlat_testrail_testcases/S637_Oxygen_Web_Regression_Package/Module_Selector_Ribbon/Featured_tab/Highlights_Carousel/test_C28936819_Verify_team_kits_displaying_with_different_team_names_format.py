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
class Test_C28936819_Verify_team_kits_displaying_with_different_team_names_format(Common):
    """
    TR_ID: C28936819
    NAME: Verify team kits displaying with different team names format
    DESCRIPTION: This test case verifies displaying of team kits on events cards in Highlights Carousels with different team names format(short and Long names)
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage(Featured/Highlights tab and Event Hub)
    PRECONDITIONS: 3. Navigate Sports Landing pages
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS:
    PRECONDITIONS: * Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: * Sport Pages > Sport Categories > Sport > Highlights Carousel
    PRECONDITIONS: * Event Hub > Highlights carousel
    PRECONDITIONS: - You should have active Highlights Carousels with active events in CMS. Make sure that Highlights Carousel configured by TypeID and EventID
    PRECONDITIONS: - Team kits are mapped to teams by names (e.g.West Brom or West Bromwich ,Newcastle Utd or Newcastle ,Leicester City or Leicester in premier league and Birmingham City or Birmingham ,Blackburn Rovers or Blackburn , Cardiff City or Cardiff , Derby County or Derby ,Huddersfield Town or Huddersfield, Luton Town or Luton, Nottingham Forest or Nottm Forest, Preston North End or Preston ,Rotherham United or Rotherham , Sheff Wednesday or Sheff Wed , Stoke City or Stoke , Swansea City or Swansea , Wycombe Wanderers or Wycombe)
    PRECONDITIONS: - TypeID and Event ID must be from Premier League or Championship League to display the team kits
    """
    keep_browser_open = True

    def test_001_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_if_team_names_are_full_for_example_west_bromwich_vs_newcastle_utd(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels if team names are full, for example: |West Bromwich| |vs| |Newcastle Utd|
        EXPECTED: Team kits are displayed correctly according to mapped teams in Highlights Carousel configured by TypeID and EventID
        """
        pass

    def test_002_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_if_team_names_are_shortened_for_example_west_brom_vs_newcastle(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels if team names are shortened, for example: |West Brom| |vs| |Newcastle|
        EXPECTED: Team kits are displayed correctly according to mapped teams in Highlights Carousel configured by TypeID and EventID
        """
        pass

    def test_003_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_if_team_names_have_a_different_format_full_and_shortened_for_example_rotherham_united_vs_swansea(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels if team names have a different format (full and shortened), for example: |Rotherham United| |vs| |Swansea|
        EXPECTED: Team kits are displayed correctly according to mapped teams in Highlights Carousel configured by TypeID and EventID
        """
        pass

    def test_004_navigate_to_the_some_sports_landing_page_and_event_hub_and_repeat_the_steps_1_3(self):
        """
        DESCRIPTION: Navigate to the some Sports Landing page and Event Hub and repeat the steps 1-3
        EXPECTED: 
        """
        pass
