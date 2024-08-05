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
class Test_C28692447_Verify_team_kits_displaying_in_HC_if_both_kits_are_mapped_to_team_names_configured_by_EventID(Common):
    """
    TR_ID: C28692447
    NAME: Verify team kits displaying in HC if both kits are mapped to team names configured by EventID
    DESCRIPTION: This test case verifies that team kits are displayed if Highlights Carousel configured by Event ID
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage(Featured/Highlights tab and Event Hub)
    PRECONDITIONS: 3. Navigate Sports Landing pages(Ex: Football)
    PRECONDITIONS: CMS configurations:
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS:
    PRECONDITIONS: * Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: * Sport Pages > Sport Categories > Sport > Highlights Carousel
    PRECONDITIONS: * Event Hub > Highlights carousel
    PRECONDITIONS: - Make sure that Highlights Carousel configured by EventID and it must be from Premier League or Championship League to display the team kits
    PRECONDITIONS: KITS:
    PRECONDITIONS: - Premier League Kits - https://app.zeplin.io/project/5d357b69841d61b2f0ce58de/screen/5f4684364e957d293bb44d61
    PRECONDITIONS: - Championship kits - https://zpl.io/V0KoKpo
    PRECONDITIONS: Note:
    PRECONDITIONS: Consider below updated kits for the below teams (Ignore these teams kits from premier league and Championship league)
    PRECONDITIONS: Coventry : https://jira.egalacoral.com/secure/attachment/1579253/1579253_coventry.svg
    PRECONDITIONS: Bournemouth:  https://jira.egalacoral.com/secure/attachment/1569037/1569037_Bournemouth_test.svg
    PRECONDITIONS: Bristol-City : https://jira.egalacoral.com/secure/attachment/1569038/1569038_Bristol-City_test.svg
    PRECONDITIONS: sheff-wed: https://jira.egalacoral.com/secure/attachment/1578596/1578596_sheff-wed.svg
    PRECONDITIONS: watford - consider kit from Championship League (Ignore from premier league)
    """
    keep_browser_open = True

    def test_001_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_if_team_name_has_mapped_team_kit(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels if team name has mapped team kit
        EXPECTED: Team kits are displayed correctly according to mapped teams in Highlights Carousel configured by EventID
        """
        pass

    def test_002_navigate_to_the_sports_landing_page_and_event_hub_and_repeat_the_step_1(self):
        """
        DESCRIPTION: Navigate to the Sports Landing page and Event Hub and repeat the step 1
        EXPECTED: 
        """
        pass

    def test_003_verify_kits_for_all_the_teams_in_premier_league_and_championship_from_the_preconditions_and_repeat_step_1(self):
        """
        DESCRIPTION: Verify Kits for all the teams in premier league and Championship from the preconditions and repeat step 1
        EXPECTED: 
        """
        pass

    def test_004_in_cms_edit_highlights_carousels_with_eventid_from_another_competition_not_from_premier_league_or_championship_league_and_save_the_changes(self):
        """
        DESCRIPTION: In CMS edit Highlights Carousels with EventID from another competition (not from Premier League or Championship League) and save the changes
        EXPECTED: The changes are saved successfully
        """
        pass

    def test_005_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_not_from_premier_league_or_championship_league(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels NOT from Premier League or Championship League
        EXPECTED: Team kits are NOT displayed on the event card in Highlights Carousel configured by EventID
        """
        pass
