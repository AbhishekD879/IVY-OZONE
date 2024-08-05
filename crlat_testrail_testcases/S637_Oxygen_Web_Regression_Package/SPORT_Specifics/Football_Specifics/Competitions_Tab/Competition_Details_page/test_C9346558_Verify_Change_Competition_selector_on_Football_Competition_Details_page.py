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
class Test_C9346558_Verify_Change_Competition_selector_on_Football_Competition_Details_page(Common):
    """
    TR_ID: C9346558
    NAME: Verify 'Change Competition' selector on Football Competition Details page
    DESCRIPTION: This test case verifies 'Change Competition' selector on Football competition details page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football landing page > Competitions tab
    PRECONDITIONS: 3. Expand any class accordion and click on any type
    PRECONDITIONS: **NOTE!**
    PRECONDITIONS: * To verify competitions (classes) that are displayed within 'Change competition' selector check values in **OX.competitionsMainClasses_football** and **OX.competitionsAZClasses_football** keys in Local Storage
    PRECONDITIONS: * To verify types that are displayed within specific competition (class) in 'Change competition' selector check request
    PRECONDITIONS: https:{environment}/openbet-ssviewer/Drilldown/X.XX/ClassToSubTypeForClass/YY?translationLang=en&simpleFilter=type.hasOpenEvent:isTrue
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - current openbet version
    PRECONDITIONS: YY - competition (class) ID
    """
    keep_browser_open = True

    def test_001_verify_displaying_change_competitions_selector(self):
        """
        DESCRIPTION: Verify displaying 'Change Competitions' selector
        EXPECTED: * Change Competitions' selector is displayed in the type name header
        EXPECTED: * Change Competitions' selector is tappable
        """
        pass

    def test_002_tap_change_competition_selector(self):
        """
        DESCRIPTION: Tap 'Change Competition' selector
        EXPECTED: * The chevron of the 'Change Competitions' selector changed
        EXPECTED: * 'Change Competition' selector is a cascaded list of competitions (classes)
        EXPECTED: * The list animates down the page after user taps on it
        EXPECTED: * The list corresponds to values from **OX.competitionsMainClasses_football** key in Local Storage
        EXPECTED: * Classes are displayed in Openbet display order
        EXPECTED: * 'A-Z Competitions' is displayed at the end of the list
        EXPECTED: * The class is tappable (to open/close accordion)
        EXPECTED: * The types are tappable
        EXPECTED: * The page is scrollable where there is more content available
        """
        pass

    def test_003_select_any_competitionclass_from_the_list_eg_england(self):
        """
        DESCRIPTION: Select any competition(class) from the list e.g. England
        EXPECTED: * Selected accordion is expanded
        EXPECTED: * Types that belong to selected competition are shown in Openbet display order
        """
        pass

    def test_004_select_any_type_eg_premier_league(self):
        """
        DESCRIPTION: Select any type e.g. Premier League
        EXPECTED: * 'Change Competitions' page is closed
        EXPECTED: * Corresponding competition details page is opened
        """
        pass

    def test_005_tap_change_competition_selector_again(self):
        """
        DESCRIPTION: Tap 'Change Competition' selector again
        EXPECTED: * 'Change Competitions' page is closed
        EXPECTED: * The chevron of the 'Change Competitions' selector changed
        EXPECTED: * The underlying page is displayed
        """
        pass

    def test_006_tap_change_competition_selector_gt_tap_a_z(self):
        """
        DESCRIPTION: Tap 'Change Competition' selector &gt; tap 'A-Z'
        EXPECTED: * List corresponds to values from **OX.competitionsAZClasses_football** key in Local Storage
        """
        pass
