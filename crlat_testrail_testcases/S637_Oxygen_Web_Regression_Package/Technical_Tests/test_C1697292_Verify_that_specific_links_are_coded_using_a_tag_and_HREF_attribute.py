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
class Test_C1697292_Verify_that_specific_links_are_coded_using_a_tag_and_HREF_attribute(Common):
    """
    TR_ID: C1697292
    NAME: Verify that specific links are coded using <a> tag and HREF attribute
    DESCRIPTION: This test case verifies that all links associated with areas listed are coded using <a> tag and href attribute
    DESCRIPTION: *Header menus*
    DESCRIPTION: *Left menu*
    PRECONDITIONS: Open Dev Tools ->Elements -> Select an element in the page to inspect it
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Oxygen application is loaded
        """
        pass

    def test_002_navigate_to_each_of_the_header_menus(self):
        """
        DESCRIPTION: Navigate to each of the *Header menus*
        EXPECTED: 
        """
        pass

    def test_003_click_on_each_header_menus_link_to_verify_that_a_tags_and_href_attribute_are_being_used(self):
        """
        DESCRIPTION: Click on each *Header menus* link to verify that <a> tags and HREF attribute are being used.
        EXPECTED: '<a>' tags and 'HREF' attribute are being used.
        """
        pass

    def test_004_click_on_each_sports_pages_sub_menu_to_verify_that_a_tags_and_href_attribute_are_being_used_for_example__in_play__matches__competitions__coupons__outrights__specials__player_bets(self):
        """
        DESCRIPTION: Click on each Sports page's sub menu to verify that <a> tags and HREF attribute are being used. For example:
        DESCRIPTION: - In-play
        DESCRIPTION: - Matches
        DESCRIPTION: - Competitions
        DESCRIPTION: - Coupons
        DESCRIPTION: - Outrights
        DESCRIPTION: - Specials
        DESCRIPTION: - Player bets
        EXPECTED: '<a>' tags and 'HREF' attribute are being used.
        """
        pass

    def test_005_click_on_the_left_menus_link_to_verify_that_a_tags_and_href_attribute_are_being_used(self):
        """
        DESCRIPTION: Click on the *Left menus* link to verify that <a> tags and HREF attribute are being used.
        EXPECTED: '<a>' tags and 'HREF' attribute are being used.
        """
        pass
