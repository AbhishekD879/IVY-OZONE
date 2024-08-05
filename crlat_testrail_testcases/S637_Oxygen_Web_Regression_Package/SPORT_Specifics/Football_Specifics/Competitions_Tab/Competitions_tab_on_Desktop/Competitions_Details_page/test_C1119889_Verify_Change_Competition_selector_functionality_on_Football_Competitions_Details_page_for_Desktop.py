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
class Test_C1119889_Verify_Change_Competition_selector_functionality_on_Football_Competitions_Details_page_for_Desktop(Common):
    """
    TR_ID: C1119889
    NAME: Verify 'Change Competition' selector functionality on Football Competitions Details page for Desktop
    DESCRIPTION: This test case verifies 'Change Competition' selector functionality on Football Competitions Details page for Desktop
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_football_landing_page__gt_competitions_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -&gt; 'Competitions' tab
        EXPECTED: Competitions Landing page is opened
        """
        pass

    def test_003_expand_any_classes_accordion_and_select_any_type_competition(self):
        """
        DESCRIPTION: Expand any Classes accordion and select any Type (Competition)
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_004_verify_the_displaying_of_change_competition_selector_on_competition_details_page(self):
        """
        DESCRIPTION: Verify the displaying of 'Change Competition' selector on Competition Details page
        EXPECTED: * 'Change Competition' selector is displayed on the right side of Competitions header
        EXPECTED: * 'Change Competition' inscription is displayed in selector by default
        EXPECTED: * Up and down arrows (chevrons) are shown next to 'Change Competition' inscription in selector
        """
        pass

    def test_005_hover_the_mouse_over_the_change_competition_selector(self):
        """
        DESCRIPTION: Hover the mouse over the 'Change Competition' selector
        EXPECTED: * Background color is changed
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        pass

    def test_006_click_on_change_competition_selector(self):
        """
        DESCRIPTION: Click on 'Change Competition' selector
        EXPECTED: * Distance between Up and Down arrows (chevrons) on 'Change Competition' selector is increased
        EXPECTED: * '1st Level' drop-down list with 'Country' accordions and Down arrow (chevron) on each of them is opened
        EXPECTED: * 'Country' accordions inside 'Change Competition selector' drop-down list are expandable/collapsible
        EXPECTED: * All 'Country' accordions are collapsed by default
        """
        pass

    def test_007_hover_the_mouse_over_the_countries_accordions_in_expanded_change_competition_selector(self):
        """
        DESCRIPTION: Hover the mouse over the 'Countries' accordions in expanded 'Change Competition' selector
        EXPECTED: * Background and text color is changed
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        pass

    def test_008_click_on_one_of_country_accordion_in_expanded_1st_level_drop_down(self):
        """
        DESCRIPTION: Click on one of 'Country' accordion in expanded '1st Level' drop-down
        EXPECTED: * Up arrow (chevron) is displayed on expanded 'Country' accordion
        EXPECTED: * Red vertical line appears on the left side of expanded 'Country' accordion
        EXPECTED: * '2nd Level' drop-down list of available Competitions is opened
        """
        pass

    def test_009_hover_the_mouse_over_the_competitions_item_from_2nd_level_drop_down_in_expanded_countries_accordion(self):
        """
        DESCRIPTION: Hover the mouse over the Competitions item from '2nd Level' drop-down in expanded 'Countries' accordion
        EXPECTED: * Background and text color is changed
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        pass

    def test_010_click_on_another_country_accordion_in_expanded_1st_level_drop_down_than_in_step_8(self):
        """
        DESCRIPTION: Click on another 'Country' accordion in expanded '1st Level' drop-down than in step 8
        EXPECTED: * Previously selected 'Country' accordion is collapsed and '2nd Level' drop-down list of available Competitions is not displayed anymore (from step 8)
        EXPECTED: * Up arrow (chevron) is displayed on expanded 'Country' accordion
        EXPECTED: * Red vertical line appears on the left side of expanded 'Country' accordion
        EXPECTED: * '2nd Level' drop-down list of available Competitions is opened
        EXPECTED: * Scrollbar appears when list contails more than 6 items inside
        """
        pass

    def test_011_click_on_one_of_the_competitions_in_expanded_2nd_level_drop_down_list(self):
        """
        DESCRIPTION: Click on one of the Competitions in expanded '2nd Level' drop-down list
        EXPECTED: * User navigates to the Сompetition Details page
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_012_click_on_the_back_button_at_the_competitions_header(self):
        """
        DESCRIPTION: Click on the 'Back' button at the Competitions header
        EXPECTED: * User navigates to the previously selected Сompetition Details page
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_013_repeat_steps_6_8(self):
        """
        DESCRIPTION: Repeat steps 6-8
        EXPECTED: * Up arrow (chevron) is displayed on expanded 'Country' accordion
        EXPECTED: * Red vertical line appears on the left side of expanded 'Country' accordion
        EXPECTED: * '2nd Level' drop-down list of available Competitions is opened
        """
        pass

    def test_014_click_on_change_competition_selector_again(self):
        """
        DESCRIPTION: Click on 'Change Competition' selector again
        EXPECTED: * Distance between Up and Down arrows (chevrons) on 'Change Competition' selector is decreased
        EXPECTED: * 'Change Competition' selector drop-down list is collapsed
        """
        pass

    def test_015_chose_outright_switcher_on_competitions_details_page(self):
        """
        DESCRIPTION: Chose 'Outright' switcher on Competitions Details page
        EXPECTED: * 'Outrights' switcher is displayed as selected
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_016_repeat_steps_4_14(self):
        """
        DESCRIPTION: Repeat steps 4-14
        EXPECTED: 
        """
        pass
