from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase


class FixtureHeader(ComponentBase):
    _date = 'xpath=.//*[@data-crlat="dateTitle"]'
    _item = 'xpath=.//*[@data-crlat="headTitles"]'
    _list_item_type = TextBase

    @property
    def date(self):
        return TextBase(selector=self._date, context=self._we)

    @property
    def header1(self):
        header_name, header = list(self.items_as_ordered_dict.items())[0]
        return header_name

    @property
    def header2(self):
        headers = self.items_as_ordered_dict
        if len(headers) == 3:
            header_name, header = list(headers.items())[1]
            return header_name
        else:
            return None

    @property
    def header3(self):
        headers = self.items_as_ordered_dict
        if len(headers) == 3:
            header_name, header = list(self.items_as_ordered_dict.items())[2]
        else:
            header_name, header = list(self.items_as_ordered_dict.items())[1]
        return header_name
