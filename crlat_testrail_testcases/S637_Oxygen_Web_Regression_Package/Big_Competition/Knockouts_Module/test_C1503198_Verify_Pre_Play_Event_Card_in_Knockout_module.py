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
class Test_C1503198_Verify_Pre_Play_Event_Card_in_Knockout_module(Common):
    """
    TR_ID: C1503198
    NAME: Verify Pre-Play Event Card in Knockout module
    DESCRIPTION: This test case verifies displaying of Pre-Play Event Card when Event ID is configured in CMS
    PRECONDITIONS: * Knockout Round (e.g. Round of 16, Quarterfinals, Semifinals, Finals) are correctly configured in CMS. Use test case: https://ladbrokescoral.testrail.com/index.php?/cases/view/1473948
    PRECONDITIONS: * Match details are added in CMS (e.g. Event ID, Venue...). Use test case: https://ladbrokescoral.testrail.com/index.php?/cases/view/1501418
    PRECONDITIONS: * Participants are configured in CMS-> Big Competition -> World Cup -> Participans
    PRECONDITIONS: * Coral app is opened
    """
    keep_browser_open = True

    def test_001_navigate_to_world_cup__knockouts_tab(self):
        """
        DESCRIPTION: Navigate to World Cup > 'Knockouts' tab
        EXPECTED: Knockouts tab is opened
        """
        pass

    def test_002_verify_displaying_of_pre_play_knockout_card_waiting_the_winners_if_event_is_not_configured_in_cms(self):
        """
        DESCRIPTION: Verify displaying of Pre-Play Knockout card waiting the winners if event is not configured in CMS
        EXPECTED: Cards are available and displayed:
        EXPECTED: * Date of the Event
        EXPECTED: * Venue of the Event (If Venue is not configured in CMS empty in UI )
        EXPECTED: * Winner Quarter 1 along with waining space  (If Home Team Remark, Away Team Remark are not configured in CMS empty in UI)
        EXPECTED: * If Home Team Name, Away Team Name fields are not configured in CMS default value is shown in UI (e.g. '?')
        """
        pass

    def test_003_verify_displaying_of_pre_play_knockout_card__if_winners_are_already_known_and_configured_in_cms(self):
        """
        DESCRIPTION: Verify displaying of Pre-Play Knockout card  if winners are already known and configured in CMS
        EXPECTED: Cards are available and displayed:
        EXPECTED: * Date of the Event
        EXPECTED: * Venue of the Event
        EXPECTED: * Team Name along with their Flags (Abbreviation of team name and flags are displayed if name is the same as participant name)
        EXPECTED: * Link to Event Detail Page (Total № of Markets )
        EXPECTED: * Market and Selections (e.g. Match Betting or 'To Qualify')
        """
        pass

    def test_004_verify_that_pre_play_knockout_card_is_changed_if_winner_becomes_configured_in_cms(self):
        """
        DESCRIPTION: Verify that Pre-Play Knockout card is changed if winner becomes configured in CMS
        EXPECTED: Cards are available and displayed:
        EXPECTED: * Date of the Event
        EXPECTED: * Venue of the Event
        EXPECTED: * Team Name along with their Flags (Abbreviation of team name and flags are displayed if name is the same as participant name)
        EXPECTED: * Link to Event Detail Page (Total № of Markets )
        EXPECTED: * Market and Selections (e.g. Match Betting or 'To Qualify')
        """
        pass

    def test_005_verify_odds_section_on_for_two_cards_in_one_row_eg_if_first_has_odds_and_second_not(self):
        """
        DESCRIPTION: Verify odds section on for two cards in one row (e.g if first has odds and second not)
        EXPECTED: One of card that has not configured odds is shown with gray empty section
        """
        pass

    def test_006_verify_displayed_market_on_pre_play_knockout_card(self):
        """
        DESCRIPTION: Verify displayed market on Pre-Play Knockout card
        EXPECTED: Market is displayed with first Display order in Back Office TI
        """
        pass

    def test_007_verify_displaying_of_pre_play_knockout_card__if_winners_are_already_known_and_configured_in_cms_but_participant_for_this_name_is_not_configured_in_cms_participans(self):
        """
        DESCRIPTION: Verify displaying of Pre-Play Knockout card  if winners are already known and configured in CMS but participant for this name is not configured in CMS->Participans
        EXPECTED: * Abbreviation is shown as first 3 letters from team name
        EXPECTED: * Flags are not shown
        """
        pass

    def test_008_click_on_the_link_total__of_markets_(self):
        """
        DESCRIPTION: Click on the Link (Total № of Markets )
        EXPECTED: Event details page is opened
        """
        pass

    def test_009_click_on_the_selection_and_place_bet(self):
        """
        DESCRIPTION: Click on the selection and place bet
        EXPECTED: Quick bet (bet slip) is opened and bet is placed
        """
        pass

    def test_010_do_some_changes_in_back_office_ti_eg_market_selections_and_click_refresh_page_of_pre_play_knockout_card(self):
        """
        DESCRIPTION: Do some changes in Back office TI (e.g. market, selections) and click 'Refresh' page of Pre-Play Knockout card
        EXPECTED: Updated dated should be shown in Pre-Play Knockout card
        """
        pass

    def test_011_do_some_changes_in_cms_eg_venue_and_click_refresh_page_of_pre_play(self):
        """
        DESCRIPTION: Do some changes in CMS (e.g. Venue) and click 'Refresh' page of Pre-Play
        EXPECTED: Updated dated should be shown in Pre-Play Knockout card
        """
        pass
