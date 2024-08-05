import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1503358_Verify_Participants_names_flags_translations(Common):
    """
    TR_ID: C1503358
    NAME: Verify Participant's names & flags translations
    DESCRIPTION: This test case verifies Participant's names & flags translations
    PRECONDITIONS: * Competition (e.g. World Cup) should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Participants should be configured in CMS within the created Competition. Please follow the next test case for more detailed info: https://ladbrokescoral.testrail.com/index.php?/cases/view/1446975
    PRECONDITIONS: * To check received participants via MS > Go to Network> {compettion (e.g. world-cup)} (response) > competitionParticipants: > 'participants':
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_competition_eg_world_cup(self):
        """
        DESCRIPTION: Navigate to Competition (e.g. World Cup)
        EXPECTED: * Competition page is opened
        EXPECTED: * Featured tab is opened by default
        """
        pass

    def test_003_scroll_down_to_the_hero_next_events_module_for_live_eventsoutright_modules(self):
        """
        DESCRIPTION: Scroll down to the Hero (Next Events Module for Live Events)/Outright Modules
        EXPECTED: 
        """
        pass

    def test_004_check_teams_abbreviation_if_the_participant_is_being_matched_in_cms(self):
        """
        DESCRIPTION: Check team's Abbreviation if the participant is being matched in CMS
        EXPECTED: Matched country's(team's) abbreviation in CMS is displayed on UI
        """
        pass

    def test_005_check_teams_flaglogo_if_the_participant_is_being_matched_in_cms(self):
        """
        DESCRIPTION: Check team's Flag/Logo if the participant is being matched in CMS
        EXPECTED: Uploaded a country's(team's) flag in CMS is displayed on UI
        """
        pass

    def test_006_check_teams_abbreviation_if_the_participant_is_not_being_matched_in_cms(self):
        """
        DESCRIPTION: Check team's Abbreviation if the participant is not being matched in CMS
        EXPECTED: The first 3 letters of the received OB team name in SS response are dipslayed on UI
        """
        pass

    def test_007_check_teams_flaglogo_if_the_participant_is_not_being_matched_in_cms(self):
        """
        DESCRIPTION: Check team's Flag/Logo if the participant is not being matched in CMS
        EXPECTED: No image or missing image logo is displayed on UI
        """
        pass

    def test_008_perform_5_7_steps_for_all_the_tabssub_tabs_where_team_name_abbreviations__flags_are_using__featured_tab__group_tab__all_sub_tabs__knockouts_tab(self):
        """
        DESCRIPTION: Perform 5-7 steps for all the Tabs/Sub Tabs where Team Name Abbreviations / Flags are using:
        DESCRIPTION: - Featured Tab;
        DESCRIPTION: - Group Tab > All Sub Tabs
        DESCRIPTION: - Knockouts Tab;
        EXPECTED: 
        """
        pass
