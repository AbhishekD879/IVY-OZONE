import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732046_Verify_the_displaying_of_the_warning_message_during_deleting_of_a_linked_Quick_Link_page(Common):
    """
    TR_ID: C57732046
    NAME: Verify the displaying of the warning message during deleting of a linked Quick Link page
    DESCRIPTION: This test case verifies the displaying of the warning message during deleting of a linked Quick Link page.
    PRECONDITIONS: 1. The CMS User has created a Quick Link page.
    PRECONDITIONS: 2. The CMS User has created a Quiz and:
    PRECONDITIONS: - set the 'Display From Date' to the past date.
    PRECONDITIONS: - selected a previously created Quick Link page in the 'Quick Links Set' row.
    PRECONDITIONS: - checked the 'Displayed' checkbox.
    """
    keep_browser_open = True

    def test_001_open_cms(self):
        """
        DESCRIPTION: Open CMS.
        EXPECTED: The CMS is opened.
        """
        pass

    def test_002_click_on_the_question_engine_section(self):
        """
        DESCRIPTION: Click on the 'Question engine' section.
        EXPECTED: The 'Question engine' section is expanded.
        """
        pass

    def test_003_click_on_the_quick_links_subsection(self):
        """
        DESCRIPTION: Click on the 'Quick links' subsection.
        EXPECTED: The list of Quick link pages is displayed.
        """
        pass

    def test_004_click_on_the_delete_icon_in_the_row_where_the_previously_created_quick_link_page_is_displayed(self):
        """
        DESCRIPTION: Click on the Delete icon in the row, where the previously created Quick link page is displayed.
        EXPECTED: The 'Remove Quick Links Page' pop-up is opened.
        """
        pass

    def test_005_click_on_the_no_button(self):
        """
        DESCRIPTION: Click on the 'No' button.
        EXPECTED: The 'Remove Quick Links Page' pop-up is closed.
        """
        pass

    def test_006_click_on_the_delete_icon_in_the_row_where_the_previously_created_quick_link_page_is_displayed(self):
        """
        DESCRIPTION: Click on the Delete icon in the row, where the previously created Quick link page is displayed.
        EXPECTED: The 'Remove Quick Links Page' pop-up is opened.
        """
        pass

    def test_007_click_on_the_yes_button(self):
        """
        DESCRIPTION: Click on the 'Yes' button.
        EXPECTED: The 'Remove Completed' pop-up is opened.
        """
        pass

    def test_008_click_on_the_ok_button(self):
        """
        DESCRIPTION: Click on the 'OK' button.
        EXPECTED: The 'Remove Completed' pop-up is closed.
        EXPECTED: The Quick link page is deleted from the list.
        """
        pass
