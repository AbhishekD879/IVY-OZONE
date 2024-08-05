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
class Test_C59092442_Load_sprites_to_BMA(Common):
    """
    TR_ID: C59092442
    NAME: Load sprites to BMA
    DESCRIPTION: This test case verifies that User is able to change .svg images using Image manager in CMS and those changes will be reflected in the app.
    PRECONDITIONS: - CMS is opened and User is logged in
    PRECONDITIONS: - Oxygen app is opened
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_image_manager_make_sure_that_there_is_10plus_active_svgs_uploaded_if_not___upload_them_in_different_sprites(self):
        """
        DESCRIPTION: Navigate to CMS-Image manager, make sure that there is 10+ Active SVGs uploaded. If not - upload them in different sprites.
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_sports_pages___sport_categories___edit_anysport___general_sport_configuration_and_scroll_down_a_little(self):
        """
        DESCRIPTION: Navigate to Sports Pages - Sport Categories - edit any
        DESCRIPTION: Sport - (General Sport Configuration) and scroll down a little
        EXPECTED: <SVG Icon> field is present
        """
        pass

    def test_003_focus_on_svg_icon_field_and_type_three_first_letters_of_svg_name_svgidnoteall_svgids_can_be_found_in_cms_image_manager(self):
        """
        DESCRIPTION: Focus on 'SVG Icon' field and type three first letters of SVG name (svgId)
        DESCRIPTION: **NOTE:**
        DESCRIPTION: **All svgIDs can be found in CMS-Image manager**
        EXPECTED: Scrollable dropdown with matching options appears and contains:
        EXPECTED: - Preview
        EXPECTED: - SVG Name
        EXPECTED: - Sprite Name
        """
        pass

    def test_004_choose_any_svg_from_the_list(self):
        """
        DESCRIPTION: Choose any SVG from the list
        EXPECTED: <SVG Icon> field is filled with chosen SVG name
        """
        pass

    def test_005_scroll_the_page_down_and_click_save_changesreload_the_page(self):
        """
        DESCRIPTION: Scroll the page down and click "Save changes"
        DESCRIPTION: Reload the page.
        EXPECTED: Changes are saved
        """
        pass

    def test_006_navigate_to_oxygen_homepage_and_verify_changes(self):
        """
        DESCRIPTION: Navigate to Oxygen Homepage and verify changes
        EXPECTED: New icon is present
        """
        pass

    def test_007_open_next_pages_same_behavior_formenus___banking_menus___edit_menu_ladbrokesmenus___footer_menus___edit_menuodds_boost_pagesports_pages___homepage___quick_link_module___createsports_pages___homepage___quick_link_module___editsports_pages___sport_categories___edit_any_different_sport_general_sport_configuration(self):
        """
        DESCRIPTION: Open next pages same behavior for:
        DESCRIPTION: Menus - Banking Menus - edit menu (Ladbrokes)
        DESCRIPTION: Menus - Footer Menus - edit menu
        DESCRIPTION: Odds Boost page
        DESCRIPTION: Sports Pages - Homepage - Quick Link Module - create
        DESCRIPTION: Sports Pages - Homepage - Quick Link Module - edit
        DESCRIPTION: Sports Pages - Sport Categories - edit any different Sport (General Sport Configuration)
        EXPECTED: 
        """
        pass
