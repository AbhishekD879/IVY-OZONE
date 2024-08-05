import pytest
import tests

from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import BaseHighlightsCarouselTest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import generate_highlights_carousel_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.featured
@pytest.mark.highlights_carousel
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.consequent
@vtest
class Test_C2987416_Highlights_Carousel_displaying_based_on_active_option_for_particular_highlights_carousel(BaseHighlightsCarouselTest):
    """
    TR_ID: C2987416
    VOL_ID: C9698533
    NAME: Highlights Carousel displaying based on active option for particular highlights carousel
    DESCRIPTION: This test case verifies Highlights Carousel displaying based on "Active" option for particular Highlights Carousel
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    highlights_carousels_titles = [generate_highlights_carousel_name(), generate_highlights_carousel_name()]

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: Home page in application is opened
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.football_config.category_id
            events = self.get_active_events_for_category(category_id=category_id,
                                                         number_of_events=2)

            event_id_1 = events[0]['event']['id']
            event_id_2 = events[1]['event']['id']

            self._logger.info(f'*** First event with id "{event_id_1}"')
            self._logger.info(f'*** Second event with id "{event_id_2}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            event_2 = self.ob_config.add_autotest_premier_league_football_event()
            event_id_1 = event.event_id
            event_id_2 = event_2.event_id

        cms = self.cms_config
        self.__class__.highlights_carousel = cms.create_highlights_carousel(title=self.highlights_carousels_titles[0],
                                                                            events=[event_id_1])

        self.__class__.highlights_carousel_2 = cms.create_highlights_carousel(title=self.highlights_carousels_titles[1],
                                                                              events=[event_id_2])
        self.__class__.highlights_carousel_name_1 = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])
        self.__class__.highlights_carousel_name_2 = self.convert_highlights_carousel_title(self.highlights_carousels_titles[1])

    def test_001_verify_highlights_carousels_displaying(self):
        """
        DESCRIPTION: Verify Highlights Carousels displaying
        EXPECTED: 2 Highlights Carousels are displayed
        """
        self.site.wait_content_state('Home')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_1)
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_2)

        highlight_carousels = self.site.home.tab_content.highlight_carousels

        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_1)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_1}')

        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_2)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_2}')

    def test_002_deactivate_one_of_the_highlights_carousels(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage > Highlights Carousel deactivate one of the displayed Highlights Carousels
        DESCRIPTION: - In Application refresh the page and verify Highlights Carousel displaying
        EXPECTED: Only 1 active Highlights Carousel is displayed and deactivated Highlights Carousel is not displayed
        """
        self.cms_config.change_highlights_carousel_state(self.highlights_carousel, active=False)
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_1, expected_result=False)

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertNotIn(self.highlights_carousel_name_1, highlight_carousels.keys(),
                         msg=f'Highlights Carousel named "{self.highlights_carousel_name_1}" should disappear')
        self.assertIn(self.highlights_carousel_name_2, highlight_carousels.keys(),
                      msg=f'Highlights Carousel named "{self.highlights_carousel_name_2}" was not found in {highlight_carousels.keys()}')
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_2)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named "{self.highlights_carousel_name_1}"')

    def test_003_deactivate_another_highlights_carousel(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage > Highlights Carousel deactivate another Highlights Carousels that is still displayed
        DESCRIPTION: - In Application refresh the page and verify Highlights Carousel displaying
        EXPECTED: None Highlights Carousels are displayed
        """
        self.cms_config.change_highlights_carousel_state(self.highlights_carousel_2, active=False)
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_2, expected_result=False)

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertNotIn(self.highlights_carousel_name_1, highlight_carousels.keys(),
                         msg=f'Highlights Carousel named {self.highlights_carousel_name_1} should disappear')
        self.assertNotIn(self.highlights_carousel_name_2, highlight_carousels.keys(),
                         msg=f'Highlights Carousel named {self.highlights_carousel_name_2} should disappear')
