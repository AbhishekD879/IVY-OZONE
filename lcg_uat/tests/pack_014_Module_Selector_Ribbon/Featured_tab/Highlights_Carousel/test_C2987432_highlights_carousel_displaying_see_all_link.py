import pytest

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import BaseHighlightsCarouselTest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import generate_highlights_carousel_name
from voltron.utils.helpers import normalize_name


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
class Test_C2987432_Highlights_Carousel_displaying_See_All_link(BaseHighlightsCarouselTest):
    """
    TR_ID: C2987432
    VOL_ID: C9698536
    NAME: Highlights Carousel - displaying See All link
    DESCRIPTION: This test case verifies displaying of "See All" link on Highlights Carousel
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

            self.__class__.event_name = normalize_name(events[0]['event']['name'])
            self.__class__.event_2_name = normalize_name(events[1]['event']['name'])

            self._logger.info(f'*** First event with id "{event_id_1}" and name "{self.event_name}"')
            self._logger.info(f'*** Second event with id "{event_id_2}" and name "{self.event_2_name}"')
            self.__class__.type_id = events[0]['event']['typeId']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            event_2 = self.ob_config.add_autotest_premier_league_football_event()
            event_id_1 = event.event_id
            event_id_2 = event_2.event_id
            self.__class__.event_name = event.team1 + ' v ' + event.team2
            self.__class__.event_2_name = event_2.team1 + ' v ' + event_2.team2

            self.__class__.type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id

        cms = self.cms_config

        self.__class__.highlights_carousel = cms.create_highlights_carousel(title=self.highlights_carousels_titles[0],
                                                                            events=[event_id_1, event_id_2])

        self.__class__.type_highlights_carousel = cms.create_highlights_carousel(
            title=self.highlights_carousels_titles[1], events=None, typeId=self.type_id)

        self.__class__.highlights_carousel_name_1 = self.convert_highlights_carousel_title(self.highlights_carousels_titles[0])
        self.__class__.highlights_carousel_name_2 = self.convert_highlights_carousel_title(self.highlights_carousels_titles[1])

    def test_001_verify_see_all_link_displaying_on_highlights_carousel(self):
        """
        DESCRIPTION: Verify "See All" link displaying on Highlights Carousel
        EXPECTED: - Highlights Carousel configured by TypeID has "See All" link displayed at the top right corner
        EXPECTED: - Highlights Carousel configured by EventIDs doesn't have "See All" link displayed
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_1)

        highlight_carousels = self.site.home.tab_content.highlight_carousels

        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_1)
        self.assertTrue(highlight_carousel, msg=f'There is no "{self.highlights_carousel_name_1}" carousel')
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_1}')
        self.assertFalse(highlight_carousel.has_see_all_link(expected_result=False),
                         msg='"See all" link should be not displayed for highlights carousel configured by EventIDs')

        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_2)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_2}')
        self.assertTrue(highlight_carousel.has_see_all_link(),
                        msg='"See all" link should be displayed for highlights carousel configured by TypeID')
