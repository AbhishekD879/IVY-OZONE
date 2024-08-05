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
class Test_C1288420_Add_new_SubTab(Common):
    """
    TR_ID: C1288420
    NAME: Add new SubTab
    DESCRIPTION: This test case verifies adding new SubTab within Tab on CMS
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: * https://coral-cms-dev0.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is loaded
        """
        pass

    def test_002_go_to_big_competition_section___choose_competition___choose_tab_that_has_active_subtabs_option(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has active SubTabs option
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_003_click_create_sub_tab_button(self):
        """
        DESCRIPTION: Click 'Create Sub Tab' button
        EXPECTED: 'Create a Sub Tab' pop-up is displayed
        """
        pass

    def test_004_enter_subtab_name_and_click_create_subtab_button(self):
        """
        DESCRIPTION: Enter SubTab Name and click 'Create SubTab' button
        EXPECTED: * New Sub Tab is created successfully
        EXPECTED: * User stays on the same page
        EXPECTED: * New Sub Tab is displayed within list of all existing Competitions on Big Competition section
        """
        pass

    def test_005_go_to_subtab_details_page(self):
        """
        DESCRIPTION: Go to SubTab details page
        EXPECTED: SubTab details page is opened
        """
        pass

    def test_006_verify_url_field(self):
        """
        DESCRIPTION: Verify 'URL' field
        EXPECTED: * Its impossible to edit 'URL' field
        EXPECTED: * 'URL' field is auto-populated with the value that displayed in text format:
        EXPECTED: '/' symbol + SubTab name
        """
        pass

    def test_007_go_back_to_tab_landing_page_and_repeat_steps_3_4_but_on_step_4_click_cancel_page(self):
        """
        DESCRIPTION: Go back to Tab landing page and repeat steps #3-4, but on step #4 click 'Cancel' page
        EXPECTED: * New Sub Tab is NOT created
        EXPECTED: * 'Create a Sub Tab' pop-up is closed
        EXPECTED: * User stays on the same page
        """
        pass
