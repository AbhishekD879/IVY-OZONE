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
class Test_C60079291_Verify_Change_Competition_selector_functionality_on_Basketball_Competitions_Details_page_for_Desktop(Common):
    """
    TR_ID: C60079291
    NAME: Verify 'Change Competition' selector functionality on Basketball Competitions Details page for Desktop
    DESCRIPTION: This test case verifies 'Change Competition' selector functionality on Basketball Competition Details page for Desktop
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Basketball landing page > Competitions tab
    PRECONDITIONS: 3. Expand any class accordion and select any Type (Competition)
    PRECONDITIONS: **Note!**
    PRECONDITIONS: * To have classes/types displayed on frontend, put class ID's in **'InitialClassIDs' and/or 'A-ZClassIDs' fields** in **CMS>SystemConfiguration>Competitions Basketball**. Events for those classes should be present as well.
    PRECONDITIONS: * To verify competitions (classes) that are displayed within 'Change competition' selector check values in **OX.competitionsMainClasses_basketball** and **OX.competitionsAZClasses_basketball** keys in Local Storage
    PRECONDITIONS: * To verify types that are displayed within specific competition (class) in 'Change competition' selector check request
    PRECONDITIONS: https:{environment}/openbet-ssviewer/Drilldown/X.XX/ClassToSubTypeForClass/YY?translationLang=en&simpleFilter=type.hasOpenEvent:isTrue
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - current openbet version
    PRECONDITIONS: YY - competition (class) ID
    """
    keep_browser_open = True

    def test_001_verify_the_displaying_of_change_competition_selector_on_competition_details_page(self):
        """
        DESCRIPTION: Verify the displaying of 'Change Competition' selector on Competition Details page
        EXPECTED: * 'Change Competition' selector is displayed on the right side of Competitions header
        EXPECTED: * 'Change Competition' inscription is displayed in selector by default
        EXPECTED: * Up and down arrows (chevrons) are shown next to 'Change Competition' inscription in selector
        """
        pass

    def test_002_click_on_change_competition_selector(self):
        """
        DESCRIPTION: Click on 'Change Competition' selector
        EXPECTED: * Distance between Up and Down arrows (chevrons) on 'Change Competition' selector is increased
        EXPECTED: * '1st Level' drop-down list with class accordions and Down arrow (chevron) on each of them is opened
        EXPECTED: * Class accordions inside 'Change Competition selector' drop-down list are expandable/collapsible
        EXPECTED: * All class accordions are collapsed by default
        """
        pass

    def test_003_click_on_one_of_class_accordion(self):
        """
        DESCRIPTION: Click on one of class accordion
        EXPECTED: * Up arrow (chevron) is displayed on expanded class accordion
        EXPECTED: * Red vertical line appears on the left side of expanded class accordion
        EXPECTED: * '2nd Level' drop-down list of available Competitions (types) is opened
        """
        pass

    def test_004_click_on_another_class_accordion(self):
        """
        DESCRIPTION: Click on another class accordion
        EXPECTED: * Previously selected class accordion is collapsed
        EXPECTED: * Up arrow (chevron) is displayed on expanded class accordion
        EXPECTED: * Red vertical line appears on the left side of expanded class accordion
        EXPECTED: * '2nd Level' drop-down list of available Competitions (types) is opened
        EXPECTED: * Scrollbar appears when list contains more than 6 items inside
        """
        pass

    def test_005_click_on_one_of_the_competitions_types_in_expanded_2nd_level_drop_down_list(self):
        """
        DESCRIPTION: Click on one of the Competitions (types) in expanded '2nd Level' drop-down list
        EXPECTED: * User navigates to the Сompetition Details page
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_006_click_on_the_back_button_at_the_competitions_header(self):
        """
        DESCRIPTION: Click on the 'Back' button at the Competitions header
        EXPECTED: * User navigates to the previously selected Сompetition Details page
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_007_choose_outright_switcher_on_competitions_details_page(self):
        """
        DESCRIPTION: Choose 'Outright' switcher on Competitions Details page
        EXPECTED: * 'Outrights' switcher is displayed as selected
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_008_repeat_steps_1_6(self):
        """
        DESCRIPTION: Repeat steps 1-6
        EXPECTED: 
        """
        pass
