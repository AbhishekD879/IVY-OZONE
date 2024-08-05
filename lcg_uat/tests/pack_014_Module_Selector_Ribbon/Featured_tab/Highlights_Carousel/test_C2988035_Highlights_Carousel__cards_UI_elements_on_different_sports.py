import pytest
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, retry_if_exception_type, wait_fixed, stop_after_attempt
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name, BaseHighlightsCarouselTest
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@vtest
class Test_C2988035_Highlights_Carousel__cards_UI_elements_on_different_sports(BaseHighlightsCarouselTest,
                                                                               ComponentBase):
    """
    TR_ID: C2988035
    NAME: Highlights Carousel - cards UI elements on different sports
    DESCRIPTION: This test case verifies UI cards elements displaying for different sports
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have 3 active Highlights Carousels with active events from appropriate sport: 1) 1st Highlights Carousel for Football configured in CMS > Sport Pages > Sport Categories > Football; 2) 2nd Highlights Carousel for Badminton configured in CMS > Sport Pages > Sport Categories > Golf; 3) 3rd Highlights Carousel for Volleyball configured in CMS > Sport Pages > Sport Categories > Boxing
    PRECONDITIONS: - "Display In-Play" option should be enabled in Highlights Carousels
    PRECONDITIONS: - For each sport above you should have: 1) prematch event without stream mapped; 2) prematch event with stream mapped; 3) live event without stream mapped; 4) live event with stream mapped
    PRECONDITIONS: - All events should have active market from |Match Betting| market template with selections
    PRECONDITIONS: - You should be on a landing page of the sports with configured Highlights Carousels: 1) For Football on "Matches" tab; 2) For Golf on "Events" tab; 3) For Boxing on "Fights" tab
    """
    keep_browser_open = True
    prices = {'odds_home': '1/12', 'odds_draw': '1/13', 'odds_away': '1/14'}
    highlights_carousels_titles = [generate_highlights_carousel_name(), generate_highlights_carousel_name(),
                                   generate_highlights_carousel_name()]

    @retry(stop=stop_after_attempt(4), wait=wait_fixed(wait=10),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def get_highlight_carousel(self):
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.__class__.highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(self.highlight_carousel, msg=f'There is no "{self.highlights_carousel_name}" carousel')
        self.assertTrue(self.highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name}')

    def verify_event_card_in_highlights_carousel(self, sport) -> None:
        """
        This method verify if specific event odds card is displayed within Highlights Carousel
        :param sport: verification based on sport
        """
        created_teams = []
        created_teams.extend([self.live_event_name, self.live_stream_event_name, self.pre_match_event_name,
                              self.pre_match_stream_event_name])
        for hightlight_caro in self.highlight_carousel.items:
            hightlight_caro.bet_button.is_displayed()
            self.scroll_to_we(hightlight_caro.bet_button)
            hightlight_caro.see_all.is_displayed()
            hightlight_caro.team_names.is_displayed()
            if hightlight_caro.team_names.text.replace("\n", " v ") in self.live_event_name:
                hightlight_caro.live_button.is_displayed()
            if hightlight_caro.team_names.text.replace("\n", " v ") in self.live_stream_event_name:
                hightlight_caro.watch_live_button.is_displayed()
            self.scroll_to_we(hightlight_caro.bet_button)
            odds_head = hightlight_caro.bet_button.text
            if sport == "football":
                self.assertIn("HOME", odds_head)
                self.assertIn("DRAW", odds_head)
                self.assertIn("AWAY", odds_head)
            self.assertIn(hightlight_caro.team_names.text.replace("\n", " v "), created_teams)

    def create_four_different_events(self, sport):
        if sport == "football":
            start_time = self.get_date_time_formatted_string(hours=-3)
            event_pre_match = self.ob_config.add_football_event_to_autotest_league2(start_time=start_time)
            pre_match_event_id = event_pre_match.event_id
            self.__class__.pre_match_event_name = f'{event_pre_match.team1} v {event_pre_match.team2}'
            event_pre_match_stream = self.ob_config.add_football_event_to_autotest_league2(start_time=start_time,
                                                                                           img_stream=True)
            pre_match_stream_event_id = event_pre_match_stream.event_id
            self.__class__.pre_match_stream_event_name = f'{event_pre_match_stream.team1} v {event_pre_match_stream.team2}'
            event_live_stream = self.ob_config.add_football_event_to_autotest_league2(cashout=True, is_live=True,
                                                                                      img_stream=True)
            live_stream_event_id = event_live_stream.event_id
            self.__class__.live_stream_event_name = f'{event_live_stream.team1} v {event_live_stream.team2}'
            event_live = self.ob_config.add_football_event_to_autotest_league2(cashout=True, is_live=True)
            live_event_id = event_live.event_id
            self.__class__.live_event_name = f'{event_live.team1} v {event_live.team2}'
            self.cms_config.create_highlights_carousel(
                title=self.highlights_carousels_titles[0],
                events=[pre_match_event_id, pre_match_stream_event_id, live_stream_event_id,
                        live_event_id], inplay=True)
            self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(
                self.highlights_carousels_titles[0])

        if sport == "golf":
            start_time = self.get_date_time_formatted_string(hours=-3)
            event_pre_match = self.ob_config.add_golf_event_to_golf_all_golf(start_time=start_time)
            pre_match_event_id = event_pre_match.event_id
            self.__class__.pre_match_event_name = f'{event_pre_match.team1} v {event_pre_match.team2}'
            event_pre_match_stream = self.ob_config.add_golf_event_to_golf_all_golf(start_time=start_time,
                                                                                    img_stream=True)
            pre_match_stream_event_id = event_pre_match_stream.event_id
            self.__class__.pre_match_stream_event_name = f'{event_pre_match_stream.team1} v {event_pre_match_stream.team2}'
            event_live_stream = self.ob_config.add_golf_event_to_golf_all_golf(cashout=True, is_live=True,
                                                                               img_stream=True)
            live_stream_event_id = event_live_stream.event_id
            self.__class__.live_stream_event_name = f'{event_live_stream.team1} v {event_live_stream.team2}'
            event_live = self.ob_config.add_golf_event_to_golf_all_golf(cashout=True, is_live=True)
            live_event_id = event_live.event_id
            self.__class__.live_event_name = f'{event_live.team1} v {event_live.team2}'
            self.cms_config.create_highlights_carousel(
                title=self.highlights_carousels_titles[1],
                events=[pre_match_event_id, pre_match_stream_event_id, live_stream_event_id,
                        live_event_id], inplay=True)
            self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(
                self.highlights_carousels_titles[1])

        if sport == "boxing":
            start_time = self.get_date_time_formatted_string(hours=-3)
            event_pre_match = self.ob_config.add_autotest_boxing_event(start_time=start_time)
            pre_match_event_id = event_pre_match.event_id
            self.__class__.pre_match_event_name = f'{event_pre_match.team1} v {event_pre_match.team2}'
            event_pre_match_stream = self.ob_config.add_autotest_boxing_event(start_time=start_time,
                                                                              img_stream=True)
            pre_match_stream_event_id = event_pre_match_stream.event_id
            self.__class__.pre_match_stream_event_name = f'{event_pre_match_stream.team1} v {event_pre_match_stream.team2}'
            event_live_stream = self.ob_config.add_autotest_boxing_event(cashout=True, is_live=True,
                                                                         img_stream=True)
            live_stream_event_id = event_live_stream.event_id
            self.__class__.live_stream_event_name = f'{event_live_stream.team1} v {event_live_stream.team2}'
            event_live = self.ob_config.add_autotest_boxing_event(cashout=True, is_live=True)
            live_event_id = event_live.event_id
            self.__class__.live_event_name = f'{event_live.team1} v {event_live.team2}'
            self.cms_config.create_highlights_carousel(
                title=self.highlights_carousels_titles[2],
                events=[pre_match_event_id, pre_match_stream_event_id, live_stream_event_id,
                        live_event_id], inplay=True)
            self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(
                self.highlights_carousels_titles[2])

        self.site.wait_content_state('HOMEPAGE')
        self.device.driver.delete_all_cookies()

    def test_001_verify_cards_elements_in_highlights_carousels_on_landing_pages_for_football_golf_and_boxing(self):
        """
        DESCRIPTION: Verify cards elements in Highlights Carousels on landing pages for Football, Golf and Boxing
        EXPECTED: Prematch event without stream mapped:
        EXPECTED: - Event's start date and time at the top left corner (if event starts today there is "Today" instead of date and time)
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles: Home/Draw/Away (For Football only) and 1X2 or 12 for other sports
        EXPECTED: Prematch event with stream mapped:
        EXPECTED: - "Watch" label at the top left corner
        EXPECTED: - Event's start date and time at the top left corner (if event starts today there is "Today" instead of date and time)
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under start date
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles: Home/Draw/Away (For Football only) and 1X2 or 12 for other sports
        EXPECTED: Live event without stream mapped:
        EXPECTED: - "Live" label at the top left corner
        EXPECTED: - Event's time in live/set/round
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under "Live" label
        EXPECTED: - Correct scores against teams/players (For Badminton 2 columns G and P with scores)
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles: Home/Draw/Away (For Football only) and 1X2 or 12 for other sports
        EXPECTED: Live event with stream mapped:
        EXPECTED: - "Watch Live" label at the top left corner
        EXPECTED: - Event's time in live/set/round
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under "Watch Live" label
        EXPECTED: - Correct scores against teams/players (For Badminton 2 columns G and P with scores
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles: Home/Draw/Away (For Football only) and 1X2 or 12 for other sports
        """
        self.create_four_different_events(sport="football")
        self.get_highlight_carousel()
        self.verify_event_card_in_highlights_carousel(sport="football")
        self.create_four_different_events(sport="golf")
        self.get_highlight_carousel()
        self.verify_event_card_in_highlights_carousel(sport="golf")
        self.create_four_different_events(sport="boxing")
        self.get_highlight_carousel()
        self.verify_event_card_in_highlights_carousel(sport="boxing")
