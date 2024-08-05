import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C355734_Verify_displaying_of_market_with_Next_Team_To_Score_Goal_market_template_name_and_market_name_in_the_format_First_Team_to_Score_etc_on_In_Play_page(Common):
    """
    TR_ID: C355734
    NAME: Verify displaying of market with 'Next Team To Score Goal' market template name and market name in the format  "First Team to Score" etc. on In-Play page
    DESCRIPTION: This test case verifies displaying of market with 'Next Team To Score Goal' market template name and market name in the format  "First Team to Score" etc. on In-Play page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Add market for any Football event using 'Next Team To Score' market template and 'First Team to Score' market name in TI
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Navigate to 'In-Play' page
    PRECONDITIONS: 3. Tap on 'Football' icon on Ribbon
    """
    keep_browser_open = True

    def test_001_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market selector'
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
        EXPECTED: Goals number is displayed on Sports card
        """
        pass

    def test_005_repeat_steps_1_3_for_an_incorect_number_of_goals_for_example_make_grammar_mistake_seconde_etc(self):
        """
        DESCRIPTION: Repeat steps 1-3 for an incorect number of goals, for example, make grammar mistake 'Seconde', etc.
        EXPECTED: Goals number is NOT displayed on Sports card
        """
        pass

    def test_006_repeat_steps_1_5_for_in_play_tab_on_football_landing_page(self):
        """
        DESCRIPTION: Repeat steps 1-5 for In-Play tab on Football Landing page
        EXPECTED: 
        """
        pass
