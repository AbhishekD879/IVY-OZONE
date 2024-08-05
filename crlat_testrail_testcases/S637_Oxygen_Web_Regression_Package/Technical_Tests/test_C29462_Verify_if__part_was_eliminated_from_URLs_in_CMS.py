import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29462_Verify_if__part_was_eliminated_from_URLs_in_CMS(Common):
    """
    TR_ID: C29462
    NAME: Verify if /# part was eliminated from URLs in CMS
    DESCRIPTION: This test case verifies if /# part was eliminated from URLs in CMS.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: BMA-9278: SEO - Use HTML5 routing for angular application.
    PRECONDITIONS: User is logged in CMS.
    """
    keep_browser_open = True

    def test_001_go_to_banners_section(self):
        """
        DESCRIPTION: Go to 'Banners' section
        EXPECTED: 
        """
        pass

    def test_002_verify_url_address_in_target_uri_column_for_each_item_in_the_list_with_internal_link(self):
        """
        DESCRIPTION: Verify URL address in 'Target URI' column for each item in the list with internal link
        EXPECTED: /# part is not displayed in URL address
        """
        pass

    def test_003_go_to_oxygen_application_and_tap_selected_bannerverify_redirection_to_specified_in_cms_link(self):
        """
        DESCRIPTION: Go to Oxygen application and tap selected Banner.
        DESCRIPTION: Verify redirection to specified in CMS link
        EXPECTED: User is successfully redirected to specified link in application
        """
        pass

    def test_004_go_to_menus_section_and_open_each_tabs(self):
        """
        DESCRIPTION: Go to 'Menus' section and open each tabs
        EXPECTED: 
        """
        pass

    def test_005_verify_url_address_in_target_uri_column_for_each_item_in_the_list_for_all_tabs_in_menus_section(self):
        """
        DESCRIPTION: Verify URL address in 'Target URI' column for each item in the list for all tabs in 'Menus' section
        EXPECTED: /# part is not displayed in URL address
        """
        pass

    def test_006_verify_redirection_to_specified_in_cms_links_for_menu_section_in_oxygen_application(self):
        """
        DESCRIPTION: Verify redirection to specified in CMS links for 'Menu' section in Oxygen application
        EXPECTED: User is successfully redireted to specified in CMS links for 'Menu' section
        """
        pass

    def test_007_repeat_steps_1_2_for_each_uri_which_can_use_internal_links(self):
        """
        DESCRIPTION: Repeat steps 1-2 for each URi which can use internal links
        EXPECTED: Sucessfully
        """
        pass
