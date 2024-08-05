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
class Test_C44870411_Quick_links_at_the_bottom_of_the_pages(Common):
    """
    TR_ID: C44870411
    NAME: Quick links at the bottom of the pages
    DESCRIPTION: Quick links at the bottom of the pages and message above should be displayed on the bottom of each desktop page
    PRECONDITIONS: User loads the Ladbrokes desktop web page and log in
    """
    keep_browser_open = True

    def test_001_verify_that_on_the_bottom_of_each_desktop_page_there_is_a_section_that_contains__a_messagenot_found_what_you_are_looking_for_hit_a_quick_link__links_to_other_sports_landing_pagesverify_that_all_the_links_navigate_user_in_the_right_page(self):
        """
        DESCRIPTION: Verify that on the bottom of each desktop page there is a section that contains
        DESCRIPTION: - a message
        DESCRIPTION: NOT FOUND WHAT YOU ARE LOOKING FOR? HIT A QUICK LINK
        DESCRIPTION: - links to other Sports Landing pages
        DESCRIPTION: Verify that all the links navigate user in the right page
        EXPECTED: Quick links at the bottom of the pages and message above should be displayed on the bottom of each desktop page
        EXPECTED: The navigation works fine
        """
        pass
