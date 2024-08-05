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
class Test_C85599_Verify_Price_Odds_Template_Type_on_Sport_Landing_page(Common):
    """
    TR_ID: C85599
    NAME: Verify Price Odds Template Type on Sport Landing page
    DESCRIPTION: This Test Case verified Price Odds Template Type on Sport Landing page
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**:
    PRECONDITIONS: Price Odds Template Type is CMS configurable (https://invictus.coral.co.uk/keystone/sports -> <Sport> -> 'Template Type 1')
    PRECONDITIONS: NOte: do not run this test case on Football
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_sport_where_primary_market_with_price_odds_template_type_home_draw_away_typetap__sport__icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: <Sport> where Primary Market with Price Odds Template Type 'Home Draw Away' Type
        DESCRIPTION: Tap  <Sport>  icon on the Sports Menu Ribbon
        EXPECTED: <Sport> Landing Page is opened
        EXPECTED: <Matches> ('Matches'/'Events'/'Races'/'Figths'/'Tournaments') -> tab is opened by default
        EXPECTED: 'Home Draw Away' Price Odds Template Type is shown
        """
        pass

    def test_003_change_price_odds_template_type_to_the_one_two_type_in_the_cms_and_save_changes(self):
        """
        DESCRIPTION: Change Price Odds Template Type to the 'One Two Type' in the CMS and save changes
        EXPECTED: 
        """
        pass

    def test_004_navigate_to_the_relevant_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to the relevant <Sport> landing page
        EXPECTED: <Sport> Landing Page is opened
        EXPECTED: <Matches> ('Matches'/'Events'/'Races'/'Fights'/'Tournaments')->  tab is opened by default
        EXPECTED: 'One Two' Price Odds Template Type is shown
        """
        pass

    def test_005_tap_anywhere_on_event_section(self):
        """
        DESCRIPTION: Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        pass

    def test_006_navigate_back_to_the_sport_landing_page_by_back_button(self):
        """
        DESCRIPTION: Navigate back to the <Sport> landing page by Back button
        EXPECTED: <Sport> Landing Page is opened
        EXPECTED: <Matches> ('Matches'/'Events'/'Races'/'Fights'/'Tournaments')-> tab is opened by default
        EXPECTED: 'One Two' Price Odds Template Type is shown
        """
        pass

    def test_007_repeat_steps_2_6_for___sport_in_play_tab___in_play_page___live_stream___featured_tab_module_by_type_id___featured_tab_module_by_selection_id(self):
        """
        DESCRIPTION: Repeat steps 2-6 for:
        DESCRIPTION: *   <Sport> In-Play tab
        DESCRIPTION: *   In-Play page
        DESCRIPTION: *   Live Stream
        DESCRIPTION: *   Featured Tab module by Type ID
        DESCRIPTION: *   Featured Tab module by Selection ID
        EXPECTED: 
        """
        pass
