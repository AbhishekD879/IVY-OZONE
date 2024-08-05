from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.offer_section import OffersSection, OfferSlide, OfferLink
from voltron.pages.shared.components.primitives.slide_dots import SlideDots
from voltron.pages.shared.components.right_column_widgets.right_column_item_widget import RightColumnItem
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.utils.waiters import wait_for_result


class SlideLink(OfferLink):

    def get_link(self):
        # done because on offers widget there is no attribute 'href'
        # currently image's "alt" is the same as destination url
        return self.image.get_attribute('alt')


class OffersWidgetSectionItemSlide(OfferSlide):
    _link_type = SlideLink


class OffersWidgetSectionItem(Accordion, OffersSection):
    _list_item_type = OffersWidgetSectionItemSlide

    _slide_dots = 'xpath=.//*[@data-crlat="slideDots"]'
    _slide_dots_type = SlideDots

    @property
    def slide_dots(self):
        return self._slide_dots_type(selector=self._slide_dots, context=self._we)

    def has_slide_dots(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._slide_dots, timeout=0) is not None,
            name=f'Slide dots status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class OffersWidgetSection(AccordionsList, RightColumnItem):
    _item = 'tag=accordion'  # ToDo: _item = 'xpath=.//*[@data-crlat="offerAccordion"]'
    _list_item_type = OffersWidgetSectionItem
