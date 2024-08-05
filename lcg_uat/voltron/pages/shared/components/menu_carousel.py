from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


class MenuCarouselItem(ComponentBase):
    _title_text = 'xpath=.//*[@data-crlat="menuItem.title"]'
    _link = 'xpath=.//*[@data-crlat="menu.item"]'
    _icon = 'xpath=.//*[@data-crlat="submenuListIcon"]/*'
    _counter = 'xpath=.//*[@data-crlat="eventCount"]'
    _context_timeout = 5

    def __init__(self, *args, **kwargs):
        super(MenuCarouselItem, self).__init__(*args, **kwargs)
        self.scroll_to_top()

    @property
    def title(self):
        return LinkBase(selector=self._title_text, timeout=0, context=self._we)

    @property
    def link(self):
        return LinkBase(selector=self._link, timeout=0, context=self._we)

    @property
    def title_text(self):
        return self._wait_for_not_empty_web_element_text(selector=self._title_text, timeout=0.5)

    @property
    def name(self):
        return self.title_text.rstrip()

    @property
    def icon(self):
        return self._find_element_by_selector(selector=self._icon, context=self._we)

    @property
    def counter(self) -> int:
        text = wait_for_result(lambda: self._get_webelement_text(selector=self._counter),
                               name='Counter to show up',
                               timeout=1, bypass_exceptions=())
        return int(text) if text else 0


class MenuCarousel(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="carouselMenu.item"]'
    _list_item_type = MenuCarouselItem
    _context_timeout = 5

    def __init__(self, *args, **kwargs):
        super(MenuCarousel, self).__init__(*args, **kwargs)
        self.scroll_to_top()

    def click_item(self, item_name: str, timeout: (int, float) = 0):
        items = self.items_as_ordered_dict
        if item_name in items:
            items[item_name].scroll_to()
            click(items[item_name].link._we)
        else:
            raise VoltronException('Item "%s" not found, it has to be one of ["%s"]'
                                   % (item_name, '", "'.join(items.keys())))
