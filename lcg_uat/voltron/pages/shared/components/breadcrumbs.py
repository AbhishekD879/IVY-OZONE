
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase


class BreadcrumbItem(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="breadcrumb.link"]'

    @property
    def name(self):
        text = self._wait_for_not_empty_web_element_text(selector=self._name, timeout=1)
        if text.startswith('greyhound'):
            return text.strip(' ').capitalize()
        else:
            return text.strip(' ')

    @property
    def link(self):
        return LinkBase(selector=self._name, context=self._we)

    @property
    def angle_bracket(self):
        """
        For some reason JS below also returns an angle bracket for the last element (which is not really displayed
        on the page). To avoid this xpath expression of particular structure is used, the last breadcrumb is always
        a span tag, so it won't be found.
        For the same reason it's not possible to use _we as an element for JS script - the last breadcrumb will always
        return the angle_bracket.
        """
        item_custom = 'xpath=.//*[@data-crlat="breadcrumb.item"]/a[contains(text(),"%s")]/parent::li' % self.name
        return self.after_element(item_custom)

    def click(self):
        return self.link.click()


class Breadcrumbs(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="breadcrumb.item"]'
    _list_item_type = BreadcrumbItem
    _toggle_icon = 'xpath=.//*[@data-crlat="toggleIcon" or contains(@class, "toggle-icon")]'  # VOL-2304

    @property
    def toggle_icon(self):
        return ButtonBase(selector=self._toggle_icon, context=self._we)
