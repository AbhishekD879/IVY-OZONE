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
class Test_C9477071_Verify_Change_Competition_selector_on_Tennis_Competition_Details_page(Common):
    """
    TR_ID: C9477071
    NAME: Verify 'Change Competition' selector on Tennis Competition Details page
    DESCRIPTION: This test case verifies 'Change Competition' selector on Football competition details page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football landing page > Competitions tab
    PRECONDITIONS: 3. Expand any class accordion and click on any type
    PRECONDITIONS: 4. Select any competition within expanded class
    PRECONDITIONS: **NOTE!**
    PRECONDITIONS: * To verify competitions (classes) that are displayed within 'Change competition' selector check values in **OX.competitionsMainClasses_tennis** and **OX.competitionsAZClasses_tennis** keys in Local Storage
    PRECONDITIONS: * To verify types that are displayed within specific competition (class) in 'Change competition' selector check request
    PRECONDITIONS: https:{environment}/openbet-ssviewer/Drilldown/X.XX/ClassToSubTypeForClass/YY?translationLang=en&simpleFilter=type.hasOpenEvent:isTrue
    PRECONDITIONS: where
    PRECONDITIONS: X.XX - current openbet version
    PRECONDITIONS: YY - competition (class) ID
    """
    keep_browser_open = True

    def test_001_tap_change_competition_selector(self):
        """
        DESCRIPTION: Tap 'Change Competition' selector
        EXPECTED: * 'Change Competition' selector is a cascaded list of competitions (classes)
        EXPECTED: * The list animates down the page after user taps on it
        EXPECTED: * There is a white overlay underneath the list
        EXPECTED: * The list corresponds to values from **OX.competitionsMainClasses_tennis** key in Local Storage
        EXPECTED: * 'A-Z' is displayed at the end of the list
        """
        pass

    def test_002_select_any_competition_from_the_list_eg_england(self):
        """
        DESCRIPTION: Select any competition from the list e.g. England
        EXPECTED: * Types that belong to selected competition are shown
        EXPECTED: * Competition (class) name is at the top of the list of types
        EXPECTED: * '<Back' button is displayed at the top of the list
        """
        pass

    def test_003_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: * List of competitions (classes) is shown
        EXPECTED: * If loading the competitions list takes 1 second or more, spinning wheel is shown
        """
        pass

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 
        """
        pass

    def test_005_select_any_type_eg_premier_league(self):
        """
        DESCRIPTION: Select any type e.g. Premier League
        EXPECTED: Corresponding competition details page is opened
        """
        pass

    def test_006_tap_change_competition_selector__tap_a_z(self):
        """
        DESCRIPTION: Tap 'Change Competition' selector > tap 'A-Z'
        EXPECTED: * List corresponds to values from **OX.competitionsAZClasses_tennis** key in Local Storage
        EXPECTED: * '<Back' button is displayed at the top of the list
        EXPECTED: * 'A-Z' label is displayed at the top of the list
        """
        pass

    def test_007_repeat_step_2_4(self):
        """
        DESCRIPTION: Repeat step 2-4
        EXPECTED: 
        """
        pass
