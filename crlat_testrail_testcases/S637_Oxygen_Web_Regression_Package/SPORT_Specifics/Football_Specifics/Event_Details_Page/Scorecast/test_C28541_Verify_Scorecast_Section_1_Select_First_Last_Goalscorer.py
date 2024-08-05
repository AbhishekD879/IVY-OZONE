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
class Test_C28541_Verify_Scorecast_Section_1_Select_First_Last_Goalscorer(Common):
    """
    TR_ID: C28541
    NAME: Verify Scorecast Section 1 (Select First/Last Goalscorer)
    DESCRIPTION: This test case verifies the functionality of Scorecast market section within Football event details page.
    PRECONDITIONS: 1) In order to run this test scenario select event with market name "First Goal Scorecast" and/or "Last Goal Scorecast"
    PRECONDITIONS: 2) To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First Goalscorer"
    PRECONDITIONS: *   PROD: name="First Goal Scorer"
    """
    keep_browser_open = True

    def test_001_open_football_event_detail_page(self):
        """
        DESCRIPTION: Open Football Event Detail Page
        EXPECTED: Football Event Details page is opened
        """
        pass

    def test_002_go_to_scorecast_market_section(self):
        """
        DESCRIPTION: Go to Scorecast market section
        EXPECTED: Scorecast market section is present and shown after 'Correct Score' market
        """
        pass

    def test_003_verify_section_1_select_firstlast_goalscorer(self):
        """
        DESCRIPTION: Verify section 1 (Select First/Last Goalscorer)
        EXPECTED: Section 1 consists of:
        EXPECTED: *   Scorer selector (two switchers)
        EXPECTED: *   Team selector (two buttons)
        EXPECTED: *   Player selector (drop-down list)
        """
        pass

    def test_004_verify_scorer_selector(self):
        """
        DESCRIPTION: Verify Scorer selector
        EXPECTED: *   Two options: **'First Scorer'** and **'Last Scorer'** are shown
        EXPECTED: *   'First Scorer' option is selected by default
        EXPECTED: *   Selected option is highlighted
        EXPECTED: *   Just one option is displayed when only one market is available in SS
        """
        pass

    def test_005_verify_team_selector(self):
        """
        DESCRIPTION: Verify Team selector
        EXPECTED: *   Two options: <Home Team> (first in the event name) and <Away Team> (second in the event name) are shown
        EXPECTED: *   <Home Team> is selected by default
        EXPECTED: *   Selected option is highlighted
        """
        pass

    def test_006_verify_firstplayer_to_scorelast_player_to_score_player_selectorname_depends_on_which_market_is_selected_in_scorer_selector_and_which_team_is_selected_in_team_selector_(self):
        """
        DESCRIPTION: Verify '**First Player to Score**'/'**Last Player to Score**' player selector
        DESCRIPTION: (name depends on which market is selected in Scorer selector and which team is selected in Team selector )
        EXPECTED: *   Drop-down contains the list of all players belonging to the selected team
        EXPECTED: *   Outcomes are ordered by **Price/Odds in ascending** order (lowest to highest), check SS (as price/odds are not visible on front end)
        EXPECTED: *   If Price/Odds are the same then list **alphabetically by player surname**
        """
        pass

    def test_007_verify_drop_down_content_whenfirst_scorer_option_is_selected(self):
        """
        DESCRIPTION: Verify drop-down content when** 'First Scorer' **option is selected
        EXPECTED: All outcomes with attribute:
        EXPECTED: *   **outcomeMeaningMinorCode="H"** (if <Home Team> is selected)
        EXPECTED: OR
        EXPECTED: *   **outcomeMeaningMinorCode="A" **(if <Away Team> is selected)
        EXPECTED: of **'First Goalscorer'** market are shown
        """
        pass

    def test_008_verify_drop_down_content_whenlast_scoreroption_is_selected(self):
        """
        DESCRIPTION: Verify drop-down content when** 'Last Scorer' **option is selected
        EXPECTED: All outcomes with attribute:
        EXPECTED: *   **outcomeMeaningMinorCode="H"** (if <Home Team> is selected)
        EXPECTED: OR
        EXPECTED: *   **outcomeMeaningMinorCode="A" **(if <Away Team> is selected)
        EXPECTED: of **'Last Goalscorer'** market are shown
        """
        pass

    def test_009_verify_selections_in_drop_down(self):
        """
        DESCRIPTION: Verify selections in drop-down
        EXPECTED: *   Each selection name corresponds to '**name**' attribute on the outcome level of verified Market
        """
        pass
