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
class Test_C28804738_Verify_team_kits_displaying_if_only_one_kit_is_mapped_to_team_name_with_TypeID(Common):
    """
    TR_ID: C28804738
    NAME: Verify team kits displaying if only one kit is mapped to team name with TypeID
    DESCRIPTION: This test case verifies displaying of team kits of events cards in Highlights Carousels if only one kit is mapped to team name with TypeID
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage(Featured/Highlights tab and Event Hub)
    PRECONDITIONS: 3. Navigate Sports Landing pages(Ex: Football)
    PRECONDITIONS: CMS configurations:
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS:
    PRECONDITIONS: * Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: * Sport Pages > Sport Categories > Sport > Highlights Carousel
    PRECONDITIONS: * Event Hub > Highlights carousel
    PRECONDITIONS: - Make sure that Highlights Carousel configured by TypeID and it must be from Premier League or Championship League to display the team kits
    PRECONDITIONS: KITS:
    PRECONDITIONS: - Premier League Kits - https://app.zeplin.io/project/5d357b69841d61b2f0ce58de/screen/5f4684364e957d293bb44d61
    PRECONDITIONS: - Championship kits - https://zpl.io/V0KoKpo
    """
    keep_browser_open = True

    def test_001_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_if_one_of_team_name_has_no_mapped_team_kit(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels if one of team name has NO mapped team kit
        EXPECTED: - Both team kits are NOT displayed on Highlights Carousel configured by TypeID
        EXPECTED: - If one of team name has NO mapped team kit - NO team kits are displayed at all
        """
        pass

    def test_002_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_if_both_of_team_names_have_no_mapped_team_kit(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels if both of team names have NO mapped team kit
        EXPECTED: Both team kits are NOT displayed on Highlights Carousel configured by TypeID
        """
        pass

    def test_003_navigate_to_the_sports_landing_page_and_event_hub_and_repeat_the_steps_1_2(self):
        """
        DESCRIPTION: Navigate to the Sports Landing page and Event Hub and repeat the steps 1-2
        EXPECTED: 
        """
        pass
