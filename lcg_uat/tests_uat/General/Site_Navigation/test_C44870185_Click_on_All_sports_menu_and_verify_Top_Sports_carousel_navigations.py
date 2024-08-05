import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.navigation
@pytest.mark.p1
@pytest.mark.mobile_only
@pytest.mark.uat
@pytest.mark.high
@pytest.mark.all_sports
@vtest
class Test_C44870185_Click_on_All_sports_menu_and_verify_Top_Sports_carousel_navigations(Common):
    """
    TR_ID: C44870185
    AUTOTEST: C49050593
    NAME: Click on 'All sports' menu and verify 'Top Sports' carousel navigations
    """
    keep_browser_open = True
    top_sport_list = [vec.Inplay.BY_IN_PLAY, vec.Football.FOOTBALL_TITLE, vec.sb.HORSERACING]

    def test_001_tap_on_all_sports_icon_on_quick_carousel(self):
        """
        DESCRIPTION: Tap on 'All Sports' icon on Quick Carousel
        EXPECTED: 'All Sports' page opens with 'Top Sports' followed by 'A-Z Sports' Sections.
        """
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        all_items.get(vec.SB.ALL_SPORTS).click()
        self.site.wait_content_state(state_name='AllSports')

        self.__class__.top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        self.assertTrue(self.top_sports, msg='No sports found in "Top Sports" section')

        az_sports_name = self.site.all_sports.a_z_sports_section.name
        self.assertEqual(az_sports_name, vec.SB.AZ_SPORTS.upper(),
                         msg=f'Actual sport name:"{az_sports_name}" is not same as Expected sport name: "{vec.SB.AZ_SPORTS.upper()}"')

    def test_002_verify_top_sports_carousel(self):
        """
        DESCRIPTION: Verify Top Sports carousel
        EXPECTED: Top sports (eg : Football, Tennis, Horses) are listed in this section along with 'In-Play'. User should be able to tap on any of the menu items and corresponding sports page should load.
        """
        for event_name in self.top_sport_list:
            self.assertIn(event_name, self.top_sports.keys(),
                          msg=f'"{event_name}" not found in Top sport list')

        # Corresponding sport is loaded- Covered in step 3 and 4

    def test_003_tap_on_in_play(self):
        """
        DESCRIPTION: Tap on In-Play
        EXPECTED: User should land on In-Play page
        """
        in_play = self.top_sports.get(vec.Inplay.BY_IN_PLAY)
        in_play.click()
        self.site.wait_content_state(state_name="In-Play")
        self.site.back_button.click()

    def test_004_tap_on_any_other_sport__race_from_the_list(self):
        """
        DESCRIPTION: Tap on any other sport / Race from the list
        EXPECTED: User should land on respective sport/race landing page
        """
        top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        self.assertTrue(top_sports, msg=f'No sports found in "{top_sports}"')
        top_sports[self.top_sport_list[1]].click()
        self.site.wait_content_state(state_name=self.top_sport_list[1].upper())

    def test_005_while_on_all_sports_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on 'All Sports' page tap on 'Back' button
        EXPECTED: User should navigate back to the previous page
        """
        self.site.back_button.click()
        self.site.wait_content_state(state_name='ALL SPORTS')
