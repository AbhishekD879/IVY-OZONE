import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.adhoc_suite
@vtest
class Test_C65946729_Verify_the_navigation_to_inplay_page_from_A_Z_Menu_all_sports(Common):
    """
    TR_ID: C65946729
    NAME: Verify the navigation to inplay
    page from A-Z Menu all sports.
    DESCRIPTION: This test case is to
    DESCRIPTION: validate the navigation to inplay page from A-Z Menu all sports.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_1launch_the__ladbrokescoralapplication(self):
        """
        DESCRIPTION: 1.launch the  Ladbrokes/Coral
        DESCRIPTION: application.
        EXPECTED: 1.Application should be  Launched
        EXPECTED: successfully.
        """
        sport_categories = self.cms_config.get_sport_categories()
        sport_category = next(
            (category for category in sport_categories if category.get('imageTitle').strip().title() == 'In-Play'),
            None)
        if sport_category:
            if sport_category.get('disabled') or not sport_category.get('isTopSport'):
                self.cms_config.update_sport_category(sport_category_id=sport_category.get('id'),
                                                                     isTopSport=True, disabled=False)
        else:
            self.cms_config.create_sport_category(title='In-Play',
                                                  categoryId=90,
                                                  ssCategoryCode='IN_PLAY',
                                                  tier='UNTIED', showInHome=False,
                                                  isTopSport=True,
                                                  targetUri='/in-play')

    def test_002_click_on_all_sports_a_z_menu_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Click on all sports A-Z menu from the Sports ribbon.
        EXPECTED: A-Z menu with all sports should be displayed.
        """
        self.site.open_sport(name='ALL SPORTS')

    def test_003_click_on_in_play_under_all_sports(self):
        """
        DESCRIPTION: Click on In-play under all sports.
        EXPECTED: Should be navigated to the in-play page.
        """
        sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        in_play_sport = next((sport for sport_name, sport in sports.items() if sport_name.upper() == 'IN-PLAY'), None)
        self.assertIsNotNone(in_play_sport, f'"IN-PLAY" sport is not present in Top Sports')
        in_play_sport.click()
        self.site.wait_content_state_changed()
        has_in_play_sports_ribbon = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(has_in_play_sports_ribbon, msg=f"The sport_carousel is not present in in-play tab ")
