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
class Test_C1500096_Promotions_configured_for_Big_Competitions(Common):
    """
    TR_ID: C1500096
    NAME: Promotions configured for Big Competitions
    DESCRIPTION: 
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: https://coral-cms-dev1.symphony-solutions.eu - Phoenix env
    PRECONDITIONS: https://coral-cms-dev0.symphony-solutions.eu - Develop
    PRECONDITIONS: A few Big Competitions should be created
    """
    keep_browser_open = True

    def test_001_load_cms_and_log_in(self):
        """
        DESCRIPTION: Load CMS and log in
        EXPECTED: CMS is loaded
        EXPECTED: User is logged in
        """
        pass

    def test_002_go_to_promotions_page___createchoose_promotion_from_the_list(self):
        """
        DESCRIPTION: Go to 'Promotions' page -> create\choose Promotion from the list
        EXPECTED: New 'Promotion' type is created
        """
        pass

    def test_003_click_on_promotion_name(self):
        """
        DESCRIPTION: Click on Promotion name
        EXPECTED: Promotion details page is displayed
        """
        pass

    def test_004_scroll_to_show_on_competitions_field(self):
        """
        DESCRIPTION: Scroll to 'Show on Competitions' field
        EXPECTED: 'Show on Competitions' filed is present
        EXPECTED: 'Competition' drop-down list is displayed
        """
        pass

    def test_005_expand_competition_dropdown_list(self):
        """
        DESCRIPTION: Expand 'Competition' dropdown list
        EXPECTED: List of all Competitions are displayed
        """
        pass

    def test_006_make_sure_that_all_competitions_that_are_created_on_big_competition_section_are_displayed(self):
        """
        DESCRIPTION: Make sure that all Competitions that are created on Big Competition section are displayed
        EXPECTED: All Competitions are displayed within 'Competition' drop-down
        """
        pass

    def test_007_check_all_checkbox_next_to_competitions_manes_and_press_save_changes_button(self):
        """
        DESCRIPTION: Check all checkbox next to Competitions manes and press 'Save Changes' button
        EXPECTED: User should be able to select all Competitions from the dropdown list  (check all checkboxes)
        EXPECTED: 'Are You Sure You Want to Save This: ''promotion name?' popup is displayed
        """
        pass

    def test_008_press_yes_and_then_ok_button(self):
        """
        DESCRIPTION: Press 'Yes' and then 'Ok' button
        EXPECTED: 'Promotion Changes are Saved.' popup is displayed
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_009_make_sure_that_all_competitions_names_are_displayed_next_to_show_on_competitions_field(self):
        """
        DESCRIPTION: Make sure that all Competitions names are displayed next to 'Show on Competitions' field
        EXPECTED: All names are displayed
        EXPECTED: If there are a lot of Competitions names  - 3 dots should be displayed at the end of the string
        """
        pass

    def test_010_expand_competition_dropdown_list_and_one_by_one_uncheck_all_checkboxes(self):
        """
        DESCRIPTION: Expand 'Competition' dropdown list and one by one uncheck all checkboxes
        EXPECTED: User should be able to uncheck all Competitions from the dropdown list
        """
        pass

    def test_011_press_save_changes_button(self):
        """
        DESCRIPTION: Press 'Save Changes' button
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_012_make_sure_that_all_competitions_names_are_not_displayed_next_to_show_on_competitions_field(self):
        """
        DESCRIPTION: Make sure that all Competitions names are not displayed next to 'Show on Competitions' field
        EXPECTED: Competitions names are not displayed
        """
        pass
