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
class Test_C28487_Verify_Correct_Score_selections_display(Common):
    """
    TR_ID: C28487
    NAME: Verify 'Correct Score' selections display
    DESCRIPTION: This test case verifies 'Correct Score' selections displaying.
    PRECONDITIONS: 1) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Please check the Selections Order for 'Correct Score' Market in the table using the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Generic+Sport+Template+-+Selections+Display+Rules
    PRECONDITIONS: 3) A valid market "Correct Score" must have** dispSortName="CS"**
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_ltsportgticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '&lt;Sport&gt;'  icon on the Sports Menu Ribbon
        EXPECTED: &lt;Sport&gt; Landing Page is opened
        """
        pass

    def test_003_tap_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name or 'More' link on the event section
        EXPECTED: &lt;Sport&gt; Event Details page is opened
        """
        pass

    def test_004_go_to_correct_score_market_section(self):
        """
        DESCRIPTION: Go to 'Correct Score' Market section
        EXPECTED: It is possible to collapse/expand Market section by tapping the section's header
        """
        pass

    def test_005_checkoutcomemeaningscores_attributes_of_selections_in_lteventidgtsimplefilter_response_eventchildrencorrect_score_marketchildrenoutcome_hierarchy(self):
        """
        DESCRIPTION: Check **outcomeMeaningScores **attributes of selections in '&lt;EventID&gt;?simpleFilter' response (Event/Children/Correct Score market/Children/Outcome hierarchy)
        EXPECTED: **outcomeMeaningScores **attributes of selections are present on the outcome level in format:
        EXPECTED: **outcomeMeaningScores="X,Y,"**
        EXPECTED: where X - score belongs to Home team, Y - to Away team
        """
        pass

    def test_006_check_number_of_columns_and_grouping_for_correct_score_market(self):
        """
        DESCRIPTION: Check number of columns and grouping for 'Correct Score' Market
        EXPECTED: *   **2 columns** if there are NO **outcomeMeaningScores **attributes where X=Y
        EXPECTED: Team/Player 1
        EXPECTED: ‘outcomeMeaningScores=( X&gt;Y )’ is a Home Win
        EXPECTED: Team/Player 2
        EXPECTED: ‘outcomeMeaningScores=( X&lt;Y )’ - is an Away Win
        EXPECTED: *   **3 columns **if there are **outcomeMeaningScores **attributes where X=Y
        EXPECTED: Team/Player 1
        EXPECTED: ‘outcomeMeaningScores=( X&gt;Y )’ is a Home Win
        EXPECTED: Draw
        EXPECTED: ‘outcomeMeaningScores=( X=Y )’ is a Draw
        EXPECTED: Team/Player 2
        EXPECTED: ‘outcomeMeaningScores=( X&lt;Y )’ - is an Away Win
        """
        pass

    def test_007_check_format_of_selections_names(self):
        """
        DESCRIPTION: Check format of **selections names **
        EXPECTED: Format of selections names is:
        EXPECTED: **'&lt;Score1&gt;-&lt;Score2&gt;'**
        """
        pass

    def test_008_check_selections_order_in_each_column(self):
        """
        DESCRIPTION: Check **selections order** in each column
        EXPECTED: Selections in each column are ordered by the **outcomeMeaningScores **value in ascending order (e.g. 1-0, 2-0, 2-1)
        """
        pass

    def test_009_verify_priceodds_buttons(self):
        """
        DESCRIPTION: Verify Price/Odds buttons
        EXPECTED: Price/Odds buttons are displayed below each selection name
        """
        pass
