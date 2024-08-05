import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    BaseHighlightsCarouselTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.tablet
@pytest.mark.featured
@pytest.mark.liveserv_updates
@pytest.mark.highlights_carousel
@pytest.mark.medium
@pytest.mark.consequent
@vtest
class Test_C2987421_Highlights_Carousel_displaying_cards_of_resulted_events(BaseHighlightsCarouselTest):
    """
    TR_ID: C2987421
    VOL_ID: C9698708
    NAME: Highlights Carousel - displaying cards of resulted events
    DESCRIPTION: This test case verifies displaying cards of resulted events
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - How to map video stream to event: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousels with 2 active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - "Display In-Play" option in Highlights Carousel above should be checked
    PRECONDITIONS: - You should be on a home page in application
    """
    def result_event_selections(self, selections: dict) -> None:
        """
        This method simply results event using it selection ids
        """
        for selection_name, selection_id in selections.items():
            self.ob_config.result_selection(selection_id=selection_id, market_id=self.marketID, event_id=self.eventID)
            self.ob_config.confirm_result(selection_id=selection_id, market_id=self.marketID, event_id=self.eventID)

    def verify_event_card_in_highlights_carousel(self, event_name: str, is_displayed: bool=True) -> None:
        """
        This method verify if specific event odds card is displayed within Highlights Carousel
        :param event_name: Event name
        :param is_displayed: Expected displaying state
        """
        highlight_carousel_cards = self.highlight_carousels[self.highlights_carousel_name].items_as_ordered_dict
        self.assertTrue(highlight_carousel_cards,
                        msg=f'"{self.highlights_carousel_name}" carousel contains no odds cards')
        expected_state = '' if is_displayed else 'not'
        result = wait_for_result(
            lambda: bool(self.highlight_carousels[self.highlights_carousel_name].
                         items_as_ordered_dict.get(event_name, False)),
            expected_result=is_displayed,
            name=f'"{event_name}" odds card {expected_state} to be shown within carousel',
            timeout=15
        )
        self.assertEqual(result, is_displayed, msg=f'Event odds card: "{event_name}" displaying state: '
                                                   f'{result}, expected: {is_displayed}')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test football events and add them to Highlights Carousel
        DESCRIPTION: Navigate to the Home page.
        EXPECTED: Highlights Carousel is shown with test events in it.
        """
        cms = self.cms_config
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        self.__class__.marketID = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'

        event_params_2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID_2 = event_params_2.event_id
        self.__class__.marketID_2 = self.ob_config.market_ids[event_params_2.event_id][market_short_name]
        self.__class__.selection_id_2 = event_params_2.selection_ids
        self.__class__.event_name_2 = f'{event_params_2.team1} v {event_params_2.team2}'

        self.__class__.highlights_carousel = \
            cms.create_highlights_carousel(title=self.highlights_carousels_titles[0],
                                           events=[self.eventID, self.eventID_2])

        self.site.wait_content_state(state_name='Homepage')

        self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name)
        self.__class__.highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertIn(self.highlights_carousel_name, self.highlight_carousels,
                      msg=f'"{self.highlights_carousel_name}" carousel is not shown')

        self.verify_event_card_in_highlights_carousel(event_name=self.event_name)
        self.verify_event_card_in_highlights_carousel(event_name=self.event_name_2)

    def test_001_in_ti_tool_result_one_of_the_events_displayed_in_highlights_carousel_verify_cards_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool result one of the events displayed in Highlights Carousel
        DESCRIPTION: - Verify cards displaying in Highlights Carousel
        EXPECTED: Card of the resulted event is undisplayed in live
        """
        self.result_event_selections(selections=self.selection_ids)
        self.verify_event_card_in_highlights_carousel(event_name=self.event_name, is_displayed=False)
        self.verify_event_card_in_highlights_carousel(event_name=self.event_name_2)

    def test_002_in_ti_tool_result_the_last_event_displayed_in_highlights_carousel_verify_cards_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool result the last event displayed in Highlights Carousel
        DESCRIPTION: - Verify cards displaying in Highlights Carousel
        EXPECTED: Highlights Carousel is undisplayed in live as it has no more events to display
        """
        self.result_event_selections(selections=self.selection_id_2)

        highlights_carousel_is_displayed = wait_for_result(
            lambda: self.site.home.tab_content.has_highlight_carousels(),
            expected_result=False,
            name='Highlights Carousel section to disappear',
            timeout=15
        )
        self.assertFalse(highlights_carousel_is_displayed, msg='Highlights Carousel section still shown on the screen')
