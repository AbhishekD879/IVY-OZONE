import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C1501591_Verify_Show_on_Competitions_option(Common):
    """
    TR_ID: C1501591
    NAME: Verify Show on Competitions option
    DESCRIPTION: This test case verified displaying promotions on Promotions and Big Competition promotions pages
    PRECONDITIONS: The Big Competitions module should created in CMS > Big Competition
    """
    keep_browser_open = True

    def test_001_load_cms_and_go_to_promotions_section(self):
        """
        DESCRIPTION: Load CMS and go to 'Promotions' section
        EXPECTED: - CMS is opened
        EXPECTED: - 'Promotions' section is opened
        """
        pass

    def test_002_create_a_new_promotion_or_choose_existing_promotion_from_the_list(self):
        """
        DESCRIPTION: Create a new promotion (or choose existing Promotion from the list)
        EXPECTED: A new Promotion is created
        """
        pass

    def test_003_click_on_promotion_name(self):
        """
        DESCRIPTION: Click on Promotion name
        EXPECTED: Promotion details page is displayed
        """
        pass

    def test_004_scroll_down_to_show_on_competitions_field(self):
        """
        DESCRIPTION: Scroll down to 'Show on Competitions' field
        EXPECTED: - 'Show on Competitions' filed is present
        EXPECTED: - 'Competition' drop-down list is displayed
        """
        pass

    def test_005_expand_competition_dropdown_list(self):
        """
        DESCRIPTION: Expand 'Competition' dropdown list
        EXPECTED: List of all created Competitions are displayed
        """
        pass

    def test_006_check_the_checkbox_next_to_competitions_name_and_click_on_save_changes_button(self):
        """
        DESCRIPTION: Check the checkbox next to Competitions name and click on 'Save Changes' button
        EXPECTED: Changes are saved
        """
        pass

    def test_007_load_oxygen_app__tap_promotions_icon_on_module_selector_ribbon(self):
        """
        DESCRIPTION: Load Oxygen app > Tap 'Promotions' icon on Module Selector ribbon
        EXPECTED: - Homepage is opened
        EXPECTED: - 'Promotions' page is opened
        """
        pass

    def test_008_verify_presence_of_promotions(self):
        """
        DESCRIPTION: Verify presence of Promotions
        EXPECTED: - All created Promotions are shown on 'Promotions' page (including these what were chosen for competitions)
        EXPECTED: - Promotion is displayed within the correct uploaded image
        EXPECTED: - All data is displayed according to CMS
        """
        pass

    def test_009_go_to_big_competition_eg_world_cup_page__promotions_tab(self):
        """
        DESCRIPTION: Go to Big Competition (e.g. World Cup) page > Promotions tab
        EXPECTED: 'Promotions' page is opened
        """
        pass

    def test_010_verify_presence_of_promotions(self):
        """
        DESCRIPTION: Verify presence of Promotions
        EXPECTED: - Only selected for Big Competettion Promotions are shown on 'Promotions' page
        EXPECTED: - Promotion is displayed within the correct uploaded image
        EXPECTED: - All data is displayed according to CMS
        """
        pass

    def test_011_back_to_cms__promotion_section(self):
        """
        DESCRIPTION: Back to CMS > Promotion section
        EXPECTED: 'Promotion' section is opened
        """
        pass

    def test_012_click_on_promotion_name_the_same_as_in_step3(self):
        """
        DESCRIPTION: Click on Promotion name (the same as in step3)
        EXPECTED: Promotion details page is displayed
        """
        pass

    def test_013_scroll_down_to_show_on_competitions_field__expand_competitions_dropdown_list__uncheck_competition__save(self):
        """
        DESCRIPTION: Scroll down to 'Show on Competitions' field > Expand 'Competitions' dropdown list > Uncheck Competition > Save
        EXPECTED: Changes are saved
        """
        pass

    def test_014_back_to_oxygen_app__tap_promotions_icon_on_module_selector_ribbon(self):
        """
        DESCRIPTION: Back to Oxygen app > Tap 'Promotions' icon on Module Selector ribbon
        EXPECTED: - 'Promotions' page is opened
        """
        pass

    def test_015_verify_presence_of_promotions(self):
        """
        DESCRIPTION: Verify presence of Promotions
        EXPECTED: - All created Promotions are shown on 'Promotions' page (including these what were unchosen for competitions)
        EXPECTED: - Promotion is displayed within the correct uploaded image
        EXPECTED: - All data is displayed according to CMS
        """
        pass

    def test_016_go_to_big_competition_eg_world_cup_page__promotions_tab(self):
        """
        DESCRIPTION: Go to Big Competition (e.g. World Cup) page > Promotions tab
        EXPECTED: 'Promotions' page is opened
        """
        pass

    def test_017_verify_presence_of_promotions(self):
        """
        DESCRIPTION: Verify presence of Promotions
        EXPECTED: - Unselected for Big Competition Promotion is not shown on 'Promotions' page
        """
        pass
