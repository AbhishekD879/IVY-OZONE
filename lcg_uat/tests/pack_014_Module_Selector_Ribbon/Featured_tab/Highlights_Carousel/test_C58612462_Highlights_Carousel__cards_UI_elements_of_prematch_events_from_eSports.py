import pytest
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry_if_exception_type, wait_fixed, stop_after_attempt, retry
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name, BaseHighlightsCarouselTest
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #can't create events
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@vtest
class Test_C58612462_Highlights_Carousel__cards_UI_elements_of_prematch_events_from_eSports(BaseHighlightsCarouselTest,
                                                                                            ComponentBase):
    """
    TR_ID: C58612462
    NAME: Highlights Carousel - cards UI elements of prematch events from eSports
    DESCRIPTION: This test case verifies UI cards elements displaying of prematch events from eSports
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) CMS > Sport Pages > Homepage:
    PRECONDITIONS: - 'Highlights Carousel' module should be enabled
    PRECONDITIONS: - Highlights Carousel should be created, containing prematch events from eSports
    PRECONDITIONS: 2) CMS > Sport Pages > Sport Categories >eSports:
    PRECONDITIONS: - 'Highlights Carousel' module should be enabled
    PRECONDITIONS: - Highlights Carousel should be created, containing prematch events from eSports
    PRECONDITIONS: 3) eSports prematch events should have active Primary market from |Match Result (2 way)| market template with selections
    PRECONDITIONS: 4) Event name of eSports prematch events should be in the following formats:
    PRECONDITIONS: **|Player A| - |Player B|**
    PRECONDITIONS: **|Player A|<space here>|vs|<space here>|Player B|**
    PRECONDITIONS: To verify data within Highlights carousel open DevTools > Network > WS > Featured WS:
    PRECONDITIONS: ![](index.php?/attachments/get/104612703)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to eSports landing page > Matches tab
    """
    keep_browser_open = True
    highlights_carousels_titles = [generate_highlights_carousel_name()]

    @retry(stop=stop_after_attempt(4), wait=wait_fixed(wait=10),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def get_highlight_carousel(self, page):
        if page == "home":
            self.wait_for_highlights_carousels(name=self.highlights_carousel_name)
            highlight_carousels = self.site.home.tab_content.highlight_carousels
            self.__class__.highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        else:
            highlight_carousels = self.site.sports_page.tab_content.highlight_carousels
            self.__class__.highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(self.highlight_carousel, msg=f'There is no "{self.highlights_carousel_name}" carousel')
        self.assertTrue(self.highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name}')

    def verify_event_card_in_highlights_carousel(self) -> None:
        """
        This method verify if specific event odds card is displayed within Highlights Carousel
        """
        created_teams = []
        created_teams.extend([self.pre_match_event_name,
                              self.pre_match_stream_event_name])
        for hightlight_caro in self.highlight_carousel.items:
            hightlight_caro.bet_button.is_displayed()
            self.scroll_to_we(hightlight_caro.bet_button)
            hightlight_caro.see_all.is_displayed()
            hightlight_caro.team_names.is_displayed()
            if hightlight_caro.team_names.text.replace("\n", " v ") in self.pre_match_stream_event_name:
                hightlight_caro.watch_live_button.is_displayed()
            self.scroll_to_we(hightlight_caro.bet_button)
            self.assertTrue(hightlight_caro.bet_button.text)
            self.assertIn(hightlight_caro.team_names.text.replace("\n", " v "), created_teams)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Events for esports and verify ESPORTS configuration in CMS
        """
        category_id = self.ob_config.esports_config.category_id
        sport_categories = self.cms_config.get_sport_categories()
        for sport in sport_categories:
            if 'esports' in sport['targetUri']:
                self.assertEqual(sport['categoryId'], category_id,
                                 msg=f'Actual category id "{sport["categoryId"]}" is not as '
                                     f'Expected "{category_id}".')
                self.assertEqual(sport['ssCategoryCode'], 'ESPORTS',
                                 msg=f'Actual category code "{sport["ssCategoryCode"]}" is not as '
                                     f'Expected "{"ESPORTS"}".')
                self.sport_in_cms = True
                break

        if not self.sport_in_cms:
            raise CmsClientException('ESPORTS sport category is not configured in the CMS')
        self.ob_config.add_autotest_esports_event()
        start_time = self.get_date_time_formatted_string(hours=-3)
        event_pre_match = self.ob_config.add_autotest_esports_event(start_time=start_time)
        pre_match_event_id = event_pre_match.event_id
        self.__class__.pre_match_event_name = f'{event_pre_match.team1} v {event_pre_match.team2}'

        event_pre_match_stream = self.ob_config.add_autotest_esports_event(start_time=start_time,
                                                                           img_stream=True)
        pre_match_stream_event_id = event_pre_match_stream.event_id
        self.__class__.pre_match_stream_event_name = f'{event_pre_match_stream.team1} v {event_pre_match_stream.team2}'

        self.cms_config.create_highlights_carousel(
            title=self.highlights_carousels_titles[0],
            events=[pre_match_event_id, pre_match_stream_event_id], inplay=True, sport_id=category_id, page_id=str(category_id))
        self.cms_config.create_highlights_carousel(
            title=self.highlights_carousels_titles[0],
            events=[pre_match_event_id, pre_match_stream_event_id], inplay=True)
        self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(
            self.highlights_carousels_titles[0])

        self.navigate_to_page('sport/esports')
        self.site.wait_content_state_changed()

    def test_001_verify_cards_elements_in_highlights_carousel(self):
        """
        DESCRIPTION: Verify cards elements in Highlights Carousel
        EXPECTED: **Prematch event without stream mapped:**
        EXPECTED: - Event's start date and time at the top left corner
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price/odds buttons under the teams/players names with correct prices and header 1 2
        EXPECTED: ![](index.php?/attachments/get/104612701)
        EXPECTED: **Prematch event with stream mapped:**
        EXPECTED: - "Watch" label at the top left corner
        EXPECTED: - Event's start date and time at the top left corner next to "Watch" label
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price/odds buttons under the teams/players names with correct prices and header 1 2
        EXPECTED: ![](index.php?/attachments/get/104612702)
        """
        self.get_highlight_carousel(page="esports")
        self.verify_event_card_in_highlights_carousel()

    def test_002__navigate_to_home_page__featured_tab_verify_cards_elements_in_highlights_carousel_for_esports(self):
        """
        DESCRIPTION: * Navigate to Home page > 'Featured' tab
        DESCRIPTION: * Verify cards elements in Highlights Carousel for eSports
        EXPECTED: **Prematch event without stream mapped:**
        EXPECTED: - Event's start date and time at the top left corner
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price/odds buttons under the teams/players names with correct prices and header 1 2
        EXPECTED: ![](index.php?/attachments/get/104612701)
        EXPECTED: **Prematch event with stream mapped:**
        EXPECTED: - "Watch" label at the top left corner
        EXPECTED: - Event's start date and time at the top left corner next to "Watch" label
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price/odds buttons under the teams/players names with correct prices and header 1 2
        EXPECTED: ![](index.php?/attachments/get/104612702)
        """
        self.navigate_to_page('Home')
        self.get_highlight_carousel(page="home")
        self.verify_event_card_in_highlights_carousel()
