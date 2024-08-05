from time import sleep
import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import BaseHighlightsCarouselTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create highlight carousels and event in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.mobile_only
@vtest
class Test_C2987419_Highlights_Carousel__displaying_in_play_events_cards_based_on_Display_In_Play_option(BaseHighlightsCarouselTest):
    """
    TR_ID: C2987419
    NAME: Highlights Carousel - displaying in-play events cards based on "Display In-Play" option
    DESCRIPTION: This test case verifies displaying of cards of in-play events based on "Display In-Play" option
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - "Display in-Play" option in Highlights Carousel above should be unchecked
    PRECONDITIONS: - Some of the events in Highlights Carousel above should be configured as in-play events (some already started and some not) and some prematch events
    PRECONDITIONS: - You should be on a home page in application
    PRECONDITIONS: NOTE: event is considered as in-play if: 1) It has market with enabled "Bet In Running" option; 2) It has "Bet In Play List" check box checked; 3) It has started or it has "Is Off" option set to "Yes".
    """
    keep_browser_open = True
    highlights_carousels_titles = ['Highlight Carousel with Pre-match and In-Play Event']

    def events_data(self):
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_event)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_event)
        self.__class__.event_name_UI = list(highlight_carousel.items_as_ordered_dict.keys())

    def test_000_preconditions(self):
        """"
        PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
        PRECONDITIONS: - You should have an active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel
        PRECONDITIONS: - "Display in-Play" option in Highlights Carousel above should be unchecked
        PRECONDITIONS: - Some of the events in Highlights Carousel above should be configured as in-play events (some already started and some not) and some prematch events
        PRECONDITIONS: - You should be on a home page in application
        PRECONDITIONS: NOTE: event is considered as in-play if: 1) It has market with enabled "Bet In Running" option; 2) It has "Bet In Play List" check box checked; 3) It has started or it has "Is Off" option set to "Yes".
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        event_id_1 = event.event_id
        self.__class__.event_name = event.team1 + ' v ' + event.team2
        in_play_event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        event_id_2 = in_play_event.event_id
        self.__class__.in_play_event_name = in_play_event.team1 + ' v ' + in_play_event.team2

        self.__class__.create_highlights_carousel = self.cms_config.create_highlights_carousel(
            title=self.highlights_carousels_titles[0], events=[event_id_1, event_id_2])

        self.__class__.highlights_carousel_name_event = self.convert_highlights_carousel_title(
            self.highlights_carousels_titles[0])

    def test_001_verify_cards_displayed_in_highlights_carousel(self):
        """
        DESCRIPTION: Verify cards displayed in Highlights Carousel
        EXPECTED: Highlights Carousel contains only cards of not in-play events
        """
        self.site.wait_content_state(state_name='Homepage')
        self.events_data()
        self.assertNotIn(self.in_play_event_name, self.event_name_UI,
                         msg=f'In-play event is appearing, whereas it should not appear, event list:  "{self.event_name}" ')
        self.assertIn(self.event_name, self.event_name_UI,
                      msg=f'Event is not appearing in highlight carousel section, whereas it should appear, '
                          f'event list:  "{self.event_name}" ')

    def test_002___in_cms__sport_pages_homepage__highlights_carousel_enable_display_in_play_option_for_the_highlights_carousel_from_preconditions__in_application_refresh_the_page_and_verify_cards_displayed_in_highlights_carousel(
            self):
        """
        DESCRIPTION: - In CMS > Sport Pages> Homepage > Highlights Carousel enable "Display In-Play" option for the Highlights Carousel from preconditions
        DESCRIPTION: - In application refresh the page and verify cards displayed in Highlights Carousel
        EXPECTED: Highlights Carousel contains cards of not in-play and in-play events
        """
        self.cms_config.update_highlights_carousel(self.create_highlights_carousel, inPlay=True)
        sleep(15)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=30)
        sleep(20)
        self.events_data()
        events_list = [self.event_name, self.in_play_event_name]
        self.assertEqual(sorted(events_list), sorted(self.event_name_UI),
                         msg=f'Inplay event is not appearing, whereas it should appear, expected: "{self.in_play_event_name}" and actual "{self.event_name_UI}"')
