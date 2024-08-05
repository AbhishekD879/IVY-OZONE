import pytest
import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import BaseHighlightsCarouselTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create highlight carousel on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@vtest
class Test_C59516839_Highlight_Carousel__Verify_that_more_than_two_Highlight_Carousels_are_configured_on_CMS_and_displayed_on_Homepage(BaseHighlightsCarouselTest):
    """
    TR_ID: C59516839
    NAME: Highlight Carousel - Verify that more than two Highlight Carousels are configured on CMS and displayed on Homepage
    DESCRIPTION: Test case verifies that more than two Highlight Carousels are configured on CMS and displayed on Homepage
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel: 1) 1st Highlights Carousel should be configured by TypeID; 2) 2nd Highlight Carousel is configured by EventIDs.
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    highlights_carousels_titles = ['Autotest Highlight Carousel with Event', 'Autotest Highlight Carousel with Type ID',
                                   'Autotest Highlight Carousel with Football Type ID',
                                   'Autotest Highlight Carousel with Football Event']

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
        PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel: 1) 1st Highlights Carousel should be configured by TypeID; 2) 2nd Highlight Carousel is configured by EventIDs.
        PRECONDITIONS: - You should be on a home page in application
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.football_config.category_id
            event = self.get_active_events_for_category(category_id=category_id)[0]
            self.__class__.event_id_1 = event['event']['id']
            self.__class__.event_name = event['event']['name']

            self.__class__.type_id = \
                self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]['event'][
                    'typeId']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = event.team1 + ' v ' + event.team2
            self.__class__.event_id_1 = event.event_id

            self.__class__.type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id

        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[0], events=[self.event_id_1])

        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[1], events=None,
                                                   typeId=self.type_id)

        self.__class__.highlights_carousel_name_event = self.convert_highlights_carousel_title(
            self.highlights_carousels_titles[0])
        self.__class__.highlights_carousel_name_type_id = self.convert_highlights_carousel_title(
            self.highlights_carousels_titles[1])

    def test_001_verify_highlights_carousels_displaying_on_homepage(self):
        """
        DESCRIPTION: Verify Highlights Carousels displaying on Homepage
        EXPECTED: 2 Highlights Carousels are displayed
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name_event)

        UI_highlight_carousels = self.site.home.tab_content.highlight_carousels.keys()

        self.__class__.created_highlight_carousels = [self.highlights_carousel_name_event,
                                                      self.highlights_carousel_name_type_id]

        self.assertListEqual(sorted(UI_highlight_carousels), sorted(self.created_highlight_carousels),
                             msg=f'Created highlight carousels are not appearing in UI, expected L "{UI_highlight_carousels}" and actual: "{self.created_highlight_carousels}"')

    def test_002_in_cms__sport_pages__homepage__highlights_carousel_configure_one_more_highlights_carousel_by_typeid(
            self):
        """
        DESCRIPTION: In CMS > Sport Pages > Homepage > Highlights Carousel configure one more Highlights Carousel by TypeID
        EXPECTED: New created Highlights Carousel is saved in CMS without any error messages
        """
        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[2], events=None,
                                                   typeId=self.type_id)

        self.__class__.highlights_carousel_with_new_type_id = self.convert_highlights_carousel_title(
            self.highlights_carousels_titles[2])

        self.created_highlight_carousels.append(self.highlights_carousel_with_new_type_id)
        self.custom_site_setup()

    def test_003_verify_highlights_carousel_displaying_on_homepage(self):
        """
        DESCRIPTION: Verify Highlights Carousel displaying on Homepage
        EXPECTED: 3 Highlights Carousels are displayed
        """
        self.navigate_to_page(name='home')
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_with_new_type_id)
        UI_highlight_carousels = self.site.home.tab_content.highlight_carousels.keys()
        self.assertListEqual(sorted(UI_highlight_carousels), sorted(self.created_highlight_carousels),
                             msg=f'Created highlight carousels are not appearing in UI, expected L "{UI_highlight_carousels}" and actual: "{self.created_highlight_carousels}"')

    def test_004_in_cms__sport_pages__homepage__highlights_carousel_configure_one_more_highlights_carousel_by_eventid(
            self):
        """
        DESCRIPTION: In CMS > Sport Pages > Homepage > Highlights Carousel configure one more Highlights Carousel by EventID
        EXPECTED: New created Highlights Carousel is saved in CMS without any error messages
        """
        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[3], events=[self.event_id_1])

        self.__class__.highlights_carousel_with_new_football_event = self.convert_highlights_carousel_title(
            self.highlights_carousels_titles[3])

        self.created_highlight_carousels.append(self.highlights_carousel_with_new_football_event)
        self.custom_site_setup()

    def test_005_verify_highlights_carousel_displaying_on_homepage(self):
        """
        DESCRIPTION: Verify Highlights Carousel displaying on Homepage
        EXPECTED: 4 Highlights Carousels are displayed
        """
        self.navigate_to_page(name='home')
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_with_new_football_event)
        UI_highlight_carousels = self.site.home.tab_content.highlight_carousels.keys()
        self.assertListEqual(sorted(UI_highlight_carousels), sorted(self.created_highlight_carousels),
                             msg=f'Created highlight carousels are not appearing in UI, expected L "{UI_highlight_carousels}" and actual: "{self.created_highlight_carousels}"')
