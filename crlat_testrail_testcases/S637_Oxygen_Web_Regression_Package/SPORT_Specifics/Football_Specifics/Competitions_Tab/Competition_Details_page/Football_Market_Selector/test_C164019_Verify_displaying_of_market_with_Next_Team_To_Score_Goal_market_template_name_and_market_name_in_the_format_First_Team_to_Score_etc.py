import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C164019_Verify_displaying_of_market_with_Next_Team_To_Score_Goal_market_template_name_and_market_name_in_the_format_First_Team_to_Score_etc(Common):
    """
    TR_ID: C164019
    NAME: Verify displaying of market with 'Next Team To Score Goal' market template name and market name in the format  "First Team to Score" etc.
    DESCRIPTION: This test case verifies displaying of market with 'Next Team To Score Goal' market template name and market name in the format  "First Team to Score" etc.
    PRECONDITIONS: 1. Add market for any Football event using 'Next Team To Score' market template and 'First Team to Score' market name in TI
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Go to Football Landing page
    PRECONDITIONS: 4. Click/Tap on Competition Module header
    PRECONDITIONS: 5. Click/Tap on sub-category (Class ID) with Type ID's
    PRECONDITIONS: 6. Choose Competitions (Type ID) that contains event from step 1
    PRECONDITIONS: Notes:
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_verify_if_value_is_available_for_football_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify if value is available for Football in the Market selector drop down
        EXPECTED: 'Next Team To Score' item is present in the Market selector drop down
        """
        pass

    def test_002_choose_next_team_to_score_item_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Choose 'Next Team To Score' item in the Market selector drop down
        EXPECTED: * Only event that contains 'Next Team To Score' market is displayed
        EXPECTED: * The fixture header for this market contains following titles:
        EXPECTED: * Home
        EXPECTED: * Away
        EXPECTED: * No Goal
        """
        pass

    def test_003_verify_if_goals_number_is_displayed_on_sports_card_under_priceodds_button_before_plus__markets_link(self):
        """
        DESCRIPTION: Verify if goals number is displayed on Sports card under Price/Odds button before "+ # Markets" link
        EXPECTED: Goals number is displayed on Sports card
        """
        pass

    def test_004_repeat_steps_1_3_for_different_number_of_goals_for_example_second_third_etc(self):
        """
        DESCRIPTION: Repeat steps 1-3 for different number of goals, for example, Second, Third, etc.
        EXPECTED: 
        """
        pass
