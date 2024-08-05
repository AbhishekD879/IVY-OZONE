from faker import Faker
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


def generate_highlights_carousel_name():
    faker = Faker()
    return f'Autotest Highlight Carousel {faker.color_name()}'


class BaseHighlightsCarouselTest(BaseFeaturedTest):
    keep_browser_open = True
    highlights_carousels = []
    active_highlights_carousels = []
    highlights_carousels_titles = [generate_highlights_carousel_name()]

    @classmethod
    def custom_setUp(cls, **kwargs):
        cls._logger.info("==============> custom_setUp method executed in BaseHighlightsCarouselTest class")
        # cms = cls.get_cms_config()
        # highlights_carousels = cms.get_all_highlights_carousels()
        # from crlat_cms_client.utils.exceptions import CMSException
        # for highlights_carousel in highlights_carousels:
        #     if not highlights_carousel['disabled']:
        #         try:
        #             cms.change_highlights_carousel_state(highlight_carousel=highlights_carousel, active=False)
        #             cls.active_highlights_carousels.append(highlights_carousel)
        #         except (CMSException, InvalidResponseException) as e:
        #             title = highlights_carousel['title']
        #             cls._logger.warning(msg=f'Failed to deactivate existing carousel "{title}" in CMS. '
        #                                     f'Probably there is something wrong with it.\n'
        #                                     f'Error is:\n{e}')

    @classmethod
    def custom_tearDown(cls):
        cls._logger.info(msg="==============> custom_tearDown method executed in BaseHighlightsCarouselTest class")
        # cms = cls.get_cms_config()
        # for highlights_carousel in cls.active_highlights_carousels:
        #     cms.change_highlights_carousel_state(highlight_carousel=highlights_carousel, active=True)

    def convert_highlights_carousel_title(self, title):
        return title if not self.brand == 'ladbrokes' else title.upper()
