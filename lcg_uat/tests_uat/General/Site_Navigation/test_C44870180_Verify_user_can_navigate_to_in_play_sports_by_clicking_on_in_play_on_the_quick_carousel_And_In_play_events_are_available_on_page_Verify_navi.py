import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p2
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870180_Verify_user_can_navigate_to_in_play_sports_by_clicking_on_in_play_on_the_quick_carousel_And_In_play_events_are_available_on_page_Verify_navigation_to_Multiple_sports_pages_from_Quick_Carousel_say_Cricket_GH_Rugby_Union_(Common):
    """
    TR_ID: C44870180
    NAME: "Verify user can navigate to in-play sports by clicking on in-play on the quick carousel And In -play events are available on page  Verify navigation to Multiple sports pages from Quick Carousel say Cricket, GH , Rugby Union "
    DESCRIPTION: "Verify user can navigate to in-play sports by clicking on in-play on the quick carousel
    DESCRIPTION: And In -play events are available on page
    DESCRIPTION: Verify navigation to Multiple sports pages from Quick Carousel say Cricket, GH , Rugby Union
    """
    keep_browser_open = True

    def test_001_on_the_home_page_tap_on_in_play_from_footer_menu(self):
        """
        DESCRIPTION: On the Home page, tap on 'In-Play' from footer menu
        EXPECTED: In-Play page is loaded and In-Play events of the first sport in the header menu are displayed.
        """
        footer = self.site.navigation_menu.items_as_ordered_dict
        if self.brand == 'ladbrokes':
            footer[vec.bma.IN_PLAY].click()
        else:
            footer[vec.siteserve.IN_PLAY_TAB].click()
        self.site.wait_content_state(state_name='In-Play')
        first_sport = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.values())[1]
        self.assertTrue(first_sport.is_selected(), msg='First sport is not selected')
        events = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.values()
        for event in events:
            self.assertTrue(event.is_displayed(), msg='Events are not displayed ')

    def test_002_click_on_any_other_sport_from_the_header_menu(self):
        """
        DESCRIPTION: Click on any other sport from the header menu.
        EXPECTED: All the In-Play events of the sport are displayed. User is able to switch between sports and should be able to view all In-Play events for the
        corresponding sport.
        """
        '''This step is covered in step 003'''

    def test_003_verify_the_content_for_each_sport(self):
        """
        DESCRIPTION: Verify the content for each sport
        EXPECTED: All the In-Play events for each sport are grouped according to competitions and user is able to
         expand/ collapse by clicking on the accordion.
        """
        sports_categories = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(sports_categories, msg='Sports categories are not loaded')
        for sport_name, sport in list(sports_categories.items())[1:]:
            sport.click()
            accordions = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
            if len(accordions) != 0:
                self.assertTrue(accordions, msg='Accordions are not present')
            else:
                self._logger.info('***No events are available')  # TODO:remove it when find all inplay events.
            for section_name, section in list(accordions.items()):
                section.collapse()
                self.assertFalse(section.is_expanded(), msg=f'{section_name} is not collapsed in {sport_name}')
                section.expand()
                self.assertTrue(section.is_expanded(), msg=f'{section_name} is not expanded in {sport_name}')
