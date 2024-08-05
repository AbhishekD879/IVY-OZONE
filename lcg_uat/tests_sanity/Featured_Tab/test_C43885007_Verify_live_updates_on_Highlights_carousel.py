import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    BaseHighlightsCarouselTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Not allowed to create events / highlight carousels on prod
@pytest.mark.sanity
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C43885007_Verify_live_updates_on_Highlights_carousel(BaseHighlightsCarouselTest):
    """
    TR_ID: C43885007
    NAME: Verify live updates on 'Highlights' carousel
    DESCRIPTION: This test case verifies live updates on 'Highlights' carousel
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage -> 'Featured' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) 'Highlights' carousel module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: 2) You should have 2 active 'Highlights' carousels with active events in CMS > Sports Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - 1st Highlights Carousel should be configured by TypeID
    PRECONDITIONS: - 2nd Highlight Carousel is configured by EvenIDs
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 2) To verify data for created Highlights Carousel use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "HighlightCarouselModule" and choose the appropriate module.
    PRECONDITIONS: ![](index.php?/attachments/get/32857095)
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True
    increased_price = '3/1'
    decreased_price = '5/2'
    prices = {'odds_home': '1/12', 'odds_draw': '1/13', 'odds_away': '1/14'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: 1 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: Home page in application is opened
        """
        event = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices)
        self.__class__.event_id = event.event_id
        self.__class__.selection_ids = event.selection_ids
        self.__class__.selection = event.team1
        self.__class__.event_name = f'{self.selection} v {event.team2}'

        highlights_carousel = self.cms_config.create_highlights_carousel(
            title=self.highlights_carousels_titles[0], events=[self.event_id])
        self.assertTrue(highlights_carousel, msg='Highlights corousel is not created successfully')
        self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])

    def test_001___in_ti_tool_increase_the_price_for_one_of_the_selections_of_event_displayed_in_highlights_carousel__verify_live_updates_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool increase the price for one of the selections of event displayed in Highlights carousel
        DESCRIPTION: - Verify live updates in Highlights Carousel
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to red for a few seconds
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name)

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel and highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named "{self.highlights_carousel_name}"')

        highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_name}"')
        self.assertIn(self.event_name, highlight_carousel_events,
                      msg=f'Event {self.event_name} is not displayed in Carousel "{self.highlights_carousel_name}"')

        event = highlight_carousel_events[self.event_name]
        self.__class__.bet_button = event.first_player_bet_button
        self.assertTrue(self.bet_button.is_displayed(), msg='Failed to display 1st team Bet button')

        self.ob_config.change_price(selection_id=self.selection_ids[self.selection], price=self.increased_price)
        result = self.wait_for_price_update_from_featured_ms(event_id=self.event_id,
                                                             selection_id=self.selection_ids[self.selection],
                                                             price=self.increased_price)
        self.assertTrue(result,
                        msg=f'Price updates are not received for event "{self.event_name}", event id "{self.event_id}"')
        self.assertTrue(self.bet_button.is_price_changed(expected_price=self.increased_price, timeout=5),
                        msg=f'Price for Bet Button for selection {self.selection} did not change. '
                            f'Actual price: "{self.bet_button.name}", Expected price: "{self.increased_price}"')

    def test_002___in_ti_tool_decrease_the_price_for_one_of_the_selections_of_event_displayed_in_highlights_carousel__verify_live_updates_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool decrease the price for one of the selections of event displayed in Highlights carousel
        DESCRIPTION: - Verify live updates in Highlights Carousel
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to blue for a few seconds
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.selection], price=self.decreased_price)
        result = self.wait_for_price_update_from_featured_ms(event_id=self.event_id,
                                                             selection_id=self.selection_ids[self.selection],
                                                             price=self.decreased_price)
        self.assertTrue(result,
                        msg=f'Price updates are not received for event "{self.event_name}", event id "{self.event_id}"')
        self.assertTrue(self.bet_button.is_price_changed(expected_price=self.decreased_price, timeout=5),
                        msg=f'Price for Bet Button for selection {self.selection} did not change. '
                            f'Actual price: "{self.bet_button.name}", Expected price: "{self.decreased_price}"')
