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
class Test_C1296001_Add_new_Module(Common):
    """
    TR_ID: C1296001
    NAME: Add new Module
    DESCRIPTION: This test case verifies adding new Module in CMS
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: * https://coral-cms-dev0.symphony-solutions.eu
    PRECONDITIONS: Default Modules types that can be created:
    PRECONDITIONS: * AEM
    PRECONDITIONS: * Next Events
    PRECONDITIONS: * Next Events Individual
    PRECONDITIONS: * Outright
    PRECONDITIONS: * Promotions
    PRECONDITIONS: * Specials
    PRECONDITIONS: * Specials Overview
    PRECONDITIONS: * Group Widget
    PRECONDITIONS: * Group All
    PRECONDITIONS: * Group Individual
    PRECONDITIONS: * Knockouts
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is loaded
        """
        pass

    def test_002_go_to_big_competition_section___choose_competition___choose_tab_that_has_inactive_subtabs_option(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has inactive SubTabs option
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_003_click_create_module_button(self):
        """
        DESCRIPTION: Click 'Create Module' button
        EXPECTED: * 'Create a new module' pop-up is displayed
        """
        pass

    def test_004_enter_module_name_select_aem_module_type_from_drop_down_and_click_create_button(self):
        """
        DESCRIPTION: Enter Module name, select 'AEM' Module type from drop-down and click 'Create' button
        EXPECTED: * 'Save complete' success pop-up is displayed
        EXPECTED: * User stays on Tab landing page
        EXPECTED: * AEM Module is present within list of all Modules
        EXPECTED: * AEM Module is disabled by default
        """
        pass

    def test_005_repeat_steps_3_4_but_on_step_3_chose_next_events_module_type(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #3 chose 'Next Events' Module type
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_3_4_but_on_step_3_chose_outright_module_type(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #3 chose 'Outright' Module type
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_4_but_on_step_3_chose_promotions_module_type(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #3 chose 'Promotions' Module type
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_3_4_but_on_step_3_chose_specials_module_type(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #3 chose 'Specials' Module type
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_3_4_but_on_step_3_chose_specials_overview_module_type(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #3 chose 'Specials Overview' Module type
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_3_4_but_on_step_3_chose_group_widget_module_type(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #3 chose 'Group Widget' Module type
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_3_4_but_on_step_3_chose_group_all_module_type(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #3 chose 'Group All' Module type
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_3_4_but_on_step_3_chose_group_individual_module_type(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #3 chose 'Group Individual' Module type
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_3_4_but_on_step_3_chose_knockouts_module_type(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #3 chose 'Knockouts' Module type
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_3_4_but_on_step_3_chose_next_events_individual_module_type(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #3 chose 'Next Events Individual' Module type
        EXPECTED: 
        """
        pass

    def test_015_go_back_to_big_competition_section___choose_competition___choose_tab_that_has_subtabs_created___choose_subtab(self):
        """
        DESCRIPTION: Go back to Big Competition section -> choose Competition -> choose Tab that has SubTabs created -> choose SubTab
        EXPECTED: SubTab landing page is opened
        """
        pass

    def test_016_repeat_steps_3_12(self):
        """
        DESCRIPTION: Repeat steps #3-12
        EXPECTED: 
        """
        pass
