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
class Test_C2538045_Results_Widget_View_on_Desktop(Common):
    """
    TR_ID: C2538045
    NAME: Results Widget View on Desktop
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_every_date_section_is_expandablecollapsible(self):
        """
        DESCRIPTION: Every date section is expandable/collapsible
        EXPECTED: 
        """
        pass

    def test_002_choose_competitions_tab(self):
        """
        DESCRIPTION: Choose 'Competitions' tab
        EXPECTED: 'Competitions' tab is selected
        """
        pass

    def test_003_choose_some_competition_from_expanded_class_accordion_and_tap_on_it(self):
        """
        DESCRIPTION: Choose some competition from expanded 'Class' accordion and tap on it
        EXPECTED: Competitions Details page is opened
        EXPECTED: 'Matches' tab is selected by default
        """
        pass

    def test_004_verify_results_tab_displaying(self):
        """
        DESCRIPTION: Verify 'Results' tab displaying
        EXPECTED: *  'Results' widget is displayed in 3-rd column or at the bottom of page below the main content, it depends on page width
        EXPECTED: *  'Results' widget is expanded by default
        EXPECTED: *  'Results' widget is expandable/collapsible
        """
        pass

    def test_005_verify_content(self):
        """
        DESCRIPTION: Verify content
        EXPECTED: Date Section is NOT expandable/collapsible
        """
        pass
