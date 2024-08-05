import pytest

from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    BaseHighlightsCarouselTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.featured
@pytest.mark.liveserv_updates
@pytest.mark.highlights_carousel
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.consequent
@vtest
class Test_C2987426_Highlights_Carousel_displaying_next_cards_after_undisplayingresulting_some_events(BaseHighlightsCarouselTest):
    """
    TR_ID: C2987426
    VOL_ID: C9698699
    NAME: Highlights Carousel - displaying next cards after undisplayingresulting some events
    DESCRIPTION: This test case verifies that Highlights Carousel with provided limitation of displayed events shows next events after some of the already displayed events have been undisplayed/resulted and there are more to show
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    """
    limit = 2

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: active Highlights Carousel with active events in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: "No. of Events" should be set in Highlights Carousel and it should be less then the amount of events provided in Highlights Carousel
        DESCRIPTION: Home page in application is opened
        """
        cms = self.cms_config
        events = []
        self.__class__.events_ids = []
        self.__class__.events_names = []
        self.__class__.selection_ids = []
        for index in range(5):
            event = self.ob_config.add_autotest_premier_league_football_event()
            events.append(event)
            self.events_ids.append(event.event_id)
            self.events_names.append(f'{event.team1} v {event.team2}')
            self.selection_ids.append(list(event.selection_ids.values()))
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.market_id = self.ob_config.market_ids[self.events_ids[1]][market_short_name]

        self.__class__.highlights_carousel = cms.create_highlights_carousel(
            title=self.highlights_carousels_titles[0], events=self.events_ids, limit=self.limit)

        self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])

    def test_001_undisplay_and_result_displayed_events_and_verify_cards_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool undisplay and result some events that are already displayed in Highlights Carousel
        DESCRIPTION: - In application refresh the page and verify cards displaying in Highlights Carousel
        EXPECTED: - Cards of events that were undisplayed/resulted are not shown and next active events according to order are displayed instead of them
        EXPECTED: - Limitation is kept and amount of cards doesn't exceed it
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name}')

        highlight_carousel_events = list(highlight_carousel.items_as_ordered_dict.keys())
        self.assertEqual(len(highlight_carousel_events), self.limit,
                         msg=f'Only {self.limit} events should be displayed')
        index_1 = self.events_names.index(highlight_carousel_events[0])
        index_2 = self.events_names.index(highlight_carousel_events[1])

        self.ob_config.change_event_state(event_id=self.events_ids[index_1], active=True, displayed=False)
        self.result_event(selection_ids=self.selection_ids[index_2], market_id=self.market_id, event_id=self.events_ids[index_2])

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name}')

        highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertEqual(len(highlight_carousel_events), self.limit,
                         msg=f'Only {self.limit} events should be displayed')
        self.assertNotIn(self.events_names[index_1], highlight_carousel_events,
                         msg=f'Event {self.events_names[index_1]} should disappear')
        self.assertNotIn(self.events_names[index_2], highlight_carousel_events,
                         msg=f'Event {self.events_names[index_2]} should disappear')
