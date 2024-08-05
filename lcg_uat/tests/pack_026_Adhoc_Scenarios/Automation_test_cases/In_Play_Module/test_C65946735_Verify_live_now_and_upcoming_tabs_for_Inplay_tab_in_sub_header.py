import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.timeout(3800)
@vtest
class Test_C65946735_Verify_live_now_and_upcoming_tabs_for_Inplay_tab_in_sub_header(Common):
    """
    TR_ID: C65946735
    NAME: Verify live now and upcoming tabs for 
    Inplay tab in sub-header.
    DESCRIPTION: This testcase verifies live now and upcoming tabs for Inplay tab in sub-header.
    PRECONDITIONS: 1. Verify with Login/logout user.
    PRECONDITIONS: 2. Navigate to CMS-> menus-> header submenus active/inactive.
    """
    keep_browser_open = True
    inplay_config = {
        "title": "In-Play" if tests.settings.brand != "bma" else "In-Play".upper(),
        "categoryId": 0,
        "isTopSport": True,
        "targetUri": "in-play",
        "ssCategoryCode": "0",
        "oddsCardHeaderType": None,
        "inApp": True,
        "showInHome": True,
        "showInPlay": True,
        "showScoreboard": False,
        "showInAZ": True,
        "tire": "UNTIED"
    }
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get or create events with at least one non runner
        """
        sport_categories = self.cms_config.get_sport_categories()

        # Get Football From All Sport Categories
        self.__class__.inplay = next(
            (sport_category for sport_category in sport_categories if
             sport_category['imageTitle'].strip().upper() == "In-Play".upper()), None)

        # Check If Football is Available in AllSport Categories
        if not self.inplay:
            self.__class__.inplay = self.cms_config.create_sport_category(**self.inplay)

        self.__class__.inplay['imageTitle'] = self.inplay['imageTitle'].upper()

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: User should be able to launch the application successfully.
        """
        self.site.wait_content_state_changed()

    def test_002_verify_inplay_tab_in_sub_header(self):
        """
        DESCRIPTION: Verify Inplay tab in sub-header.
        EXPECTED: User should be able to see the Inplay tab in sub-header.
        """
        all_sport_ribbon_items = self.site.header.sport_menu.items_names
        self.assertIn(self.inplay.get("imageTitle").strip(), all_sport_ribbon_items)

    def test_003_click_on_inplay_tab_sub_header(self):
        """
        DESCRIPTION: Click on Inplay tab sub-header.
        EXPECTED: User should be able to navigate to Inplay page successfully.
        """
        self.site.header.sport_menu.items_as_ordered_dict.get(self.inplay.get("imageTitle").strip()).click()
        self.site.wait_content_state(state_name="inplay")

    def test_004_verify_the_inplay_page(self):
        """
        DESCRIPTION: Verify the Inplay page.
        EXPECTED: User should be able to see any one of the sport should
        EXPECTED: be selected by default successfully.
        """
        is_sport_selected = any(
            ["active" in inplay_sport._we.get_attribute("class") for inplay_sport_name, inplay_sport in
             self.site.inplay.inplay_sport_menu.items_as_ordered_dict.items()])
        self.assertTrue(is_sport_selected, msg="No sport is Selected By Default After navigating to inplay")

    def test_005_verify_live_now_and_upcoming_tabs(self):
        """
        DESCRIPTION: Verify live now and upcoming tabs.
        EXPECTED: User should be able to see the live now and upcoming tab.
        """
        inplay_tabs = self.site.inplay.tab_content.grouping_buttons.items_names
        self.assertIn("LIVE NOW", inplay_tabs)
        self.assertIn("UPCOMING", inplay_tabs)

    def test_006_verify_switching_between_live_now_and_upcoming_tabs(self):
        """
        DESCRIPTION: Verify switching between live now and upcoming tabs.
        EXPECTED: User should be able to switch between live now and
        EXPECTED: upcoming tabs by clicking on it.
        """
        self.assertTrue(
            self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.get("LIVE NOW").is_selected())
        self.assertFalse(
            self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.get("UPCOMING").is_selected())
        self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.get("UPCOMING").click()
        self.assertFalse(
            self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.get("LIVE NOW").is_selected())
        self.assertTrue(
            self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.get("UPCOMING").is_selected())
