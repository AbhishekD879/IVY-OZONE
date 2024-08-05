import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p1
@pytest.mark.prod
@pytest.mark.navigation
@pytest.mark.mobile_only
@pytest.mark.uat
@pytest.mark.high
@pytest.mark.all_sports
@vtest
class Test_C44870178_C44870184_Verify_navigations_of_A_Z_menu(Common):
    """
    TR_ID: C44870178
    AUTOTEST: C49050588
    NAME: Verify navigations of A-Z menu
    DESCRIPTION: This test case verifies functionality of 'A-Z' page which can be opened via footer menu and via pressing the button 'All Sports' on the Sport menu ribbon
    PRECONDITIONS: 1. Sports are configured in CMS : Sports Pages > Sports Categories
    PRECONDITIONS: 2. A-Z sports is configured in CMS for some sports (Sports Pages > Sport Categories > <Sport> 'Show in AZ' check box is checked)
    PRECONDITIONS: 3. Application is Loaded
    Note: CMS verification cannot be done on Prod
    """
    keep_browser_open = True

    def test_001_tap_on_all_sports_icon_on_sports_menu_ribbon__menu_icon_on_footer_menu_bar(self):
        """
        DESCRIPTION: Tap on 'All Sports' icon on Sports menu ribbon / 'Menu' icon on Footer Menu bar
        EXPECTED: 'All Sports' page is opened
        EXPECTED: Top Sports are listed in the first section followed by A-Z Sports
        """
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        all_items.get(vec.SB.ALL_SPORTS).click()
        self.site.wait_content_state(state_name='AllSports')

        top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        self.assertTrue(top_sports, msg='No sports found in "Top Sports" section')

        az_sports_name = self.site.all_sports.a_z_sports_section.name
        expected_name = vec.SB.AZ_SPORTS.upper()
        self.assertEqual(az_sports_name, expected_name, msg=f'"{expected_name}" section is not displayed')

    def test_002_while_on_all_sports_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on 'All sports' page tap on Back button
        EXPECTED: User should navigate back to the home page
        """
        self.site.back_button.click()
        self.site.wait_content_state(state_name='HomePage')

    def test_003_tap_on_any_menu_item__sport_from_top_section_or_a_z_sports_on_all_sports_page(self):
        """
        DESCRIPTION: Tap on any menu item / sport from top section or A-Z Sports on All Sports page
        EXPECTED: User should navigate to the corresponding Sports Landing Page.
        """
        self.site.home.menu_carousel.items_as_ordered_dict.get(vec.SB.ALL_SPORTS).click()
        self.site.wait_content_state(state_name='AllSports')

    def test_004_verify_a_z_sports(self):
        """
        DESCRIPTION: Verify A-Z Sports
        EXPECTED: Title is 'A-Z Sports'
        EXPECTED: Sports are displayed in a list view
        EXPECTED: There are Sport name and icon
        EXPECTED: Only Sports with the CMS setting 'Show in A-Z' are shown in this section
        """
        self.__class__.az_sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
        self.assertTrue(self.az_sports, msg=f'No sports found in "{vec.SB.AZ_SPORTS}" section')

        for sport_name, sport in self.az_sports.items():
            self.assertTrue(sport.item_icon.is_displayed(),
                            msg=f'Sport icon for "{sport.item_name}" is not displayed')

    def test_005_verify_sports_ordering_under_a_z_sports(self):
        """
        DESCRIPTION: Verify sports ordering under A-Z Sports
        EXPECTED: All sports are shown in alphabetical A-Z order
        """
        all_sports_names = list(self.az_sports.keys())
        self.assertListEqual(all_sports_names, sorted(all_sports_names),
                             msg=f'Sports are not sorted in alphabetical A-Z order:'
                                 f' Actual: {all_sports_names} Expected: {sorted(all_sports_names)}')
