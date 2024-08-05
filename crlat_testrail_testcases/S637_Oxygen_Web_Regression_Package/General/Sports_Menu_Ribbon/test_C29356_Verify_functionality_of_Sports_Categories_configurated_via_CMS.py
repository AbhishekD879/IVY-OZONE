import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C29356_Verify_functionality_of_Sports_Categories_configurated_via_CMS(Common):
    """
    TR_ID: C29356
    NAME: Verify functionality of Sports Categories configurated via CMS
    DESCRIPTION: This test case verifies functionality of 'Show in Sports Ribbon', 'Show in In-Play Ribbon' and 'Show in A-Z'  for Sports Categories Section configurated in CMS
    DESCRIPTION: **JIRA Ticket : BMA-5201**
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_sports_pages_item(self):
        """
        DESCRIPTION: Go to 'Sports Pages' item
        EXPECTED: 
        """
        pass

    def test_003_select_sports_categories_section(self):
        """
        DESCRIPTION: Select Sports Categories section
        EXPECTED: Sports Categories section is opened
        """
        pass

    def test_004_for_column_show_in_sports_ribbon_tick_a_checkbox_for_sport(self):
        """
        DESCRIPTION: For column 'Show in Sports Ribbon' tick a checkbox for <Sport>
        EXPECTED: The checkbox is ticked
        """
        pass

    def test_005_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: The Homepage is opened
        """
        pass

    def test_006_go_to_sports_menu_ribbon(self):
        """
        DESCRIPTION: Go to Sports Menu Ribbon
        EXPECTED: Verify presence of <Sport> enabled via 'Show in Sports Ribbon' column checkbox in CMS
        """
        pass

    def test_007_repeat_steps_2_3_and_tick_show_in_in_play_checkbox_for_selected_sport_category(self):
        """
        DESCRIPTION: Repeat steps 2-3 and tick 'Show in In-Play' checkbox for selected <Sport> Category
        EXPECTED: 
        """
        pass

    def test_008____go_to_in_play_page_opened_via_in_play_icon_on_sports_menu_ribbon_of_invictus_application___go_to_in_play_page_opened_via_in_play_icon_on_footer_menu___go_to_in_play_page_opened_via_in_play_tab_on_module_selector_ribbon___go_to_sport___in_play_tab(self):
        """
        DESCRIPTION: *   Go to In-Play page opened via 'In-Play' icon on Sports Menu Ribbon of Invictus application
        DESCRIPTION: *   Go to In-Play page opened via 'In-Play' icon on Footer Menu
        DESCRIPTION: *   Go to In-Play page opened via 'In-Play' tab on Module Selector Ribbon
        DESCRIPTION: *   Go to <Sport> -> 'In-Play' tab
        EXPECTED: Verify presence of <Sport> enabled via 'Show in Play' column checkbox in CMS
        """
        pass

    def test_009_go_to_cms_and_disable_sport_for_in_play_page(self):
        """
        DESCRIPTION: Go to CMS and disable <Sport> for In-Play page
        EXPECTED: Verify presence of Live events :
        EXPECTED: *   Live events are not displayed on In-Play page opened via 'In-Play' icon  from Sports Menu Ribbon and from Footer Menu; and via In-Play tab on Module Selector Ribbon
        EXPECTED: *   **NOTE ! Live events are displayed on <Sport> In-Play tab**
        """
        pass

    def test_010_repeat_steps_2_4_for_show_in_a_z_column(self):
        """
        DESCRIPTION: Repeat steps 2-4 for 'Show in A-Z' column
        EXPECTED: 
        """
        pass

    def test_011_select_a_z_icon_of_invictus_application(self):
        """
        DESCRIPTION: Select 'A-Z' icon of Invictus application
        EXPECTED: Verify presence of <Sport> enabled via 'Show in A-Z' column checkbox in CMS
        """
        pass

    def test_012____go_to_cms___tick_a_checkbox_for_sport_for_two_out_of_three_columns_show_in_sports_ribbon_show_in_play_ribbon_and_show_in_a_z___go_to_invictus_application(self):
        """
        DESCRIPTION: *   Go to CMS -> tick a checkbox for <Sport> for two out of three columns 'Show in Sports Ribbon', 'Show In-Play Ribbon' and 'Show in A-Z'
        DESCRIPTION: *   Go to Invictus application
        EXPECTED: <Sport> is displayed within two sections configurated in CMS
        """
        pass

    def test_013____go_to_cms___tick_a_checkbox_for_sport_for_three_columns_show_in_sports_ribbon_show_in_play_ribbon_and_show_in_a_z___go_to_invictus_application(self):
        """
        DESCRIPTION: *   Go to CMS -> tick a checkbox for <Sport> for three columns 'Show in Sports Ribbon', 'Show In-Play Ribbon' and 'Show in A-Z'
        DESCRIPTION: *   Go to Invictus application
        EXPECTED: <Sport> is displayed within three sections configurated in CMS
        """
        pass

    def test_014____go_to_cms___untick_a_checkbox_for_sport_for_three_columns_show_in_sports_ribbon_show_in_play_ribbon_and_show_in_a_z___go_to_invictus_application(self):
        """
        DESCRIPTION: *   Go to CMS -> untick a checkbox for <Sport> for three columns 'Show in Sports Ribbon', 'Show In-Play Ribbon' and 'Show in A-Z'
        DESCRIPTION: *   Go to Invictus application
        EXPECTED: <Sport> is not displayed on Sports Ribbon, 'A-Z' and 'In-Play' sections.
        """
        pass

    def test_015____find_sport_with_no_live_events___disable_the_sport_via_cms_for_in_play_section_of_the_app___go_to_wwwinvictuscoralcoukin_playsport_via_direct_link(self):
        """
        DESCRIPTION: *   Find <Sport> with no live events
        DESCRIPTION: *   Disable the <Sport> via CMS for In-Play section of the App
        DESCRIPTION: *   Go to www.invictus.coral.co.uk/#/in-play/<Sport>/ via direct link
        EXPECTED: User is redirected to In Play > All Sports page (www.invictus.coral.co.uk/#/in-play/allsports)
        """
        pass
