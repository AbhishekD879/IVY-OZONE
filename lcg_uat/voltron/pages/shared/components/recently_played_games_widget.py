from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import switch_to_iframe
from voltron.pages.shared import get_driver
from collections import OrderedDict
import re


class RecentlyPlayedGame(ComponentBase):

    _image = 'xpath=.//img'
    _title = 'xpath=.//div[contains(@class, "carousel-title")]'

    @property
    def image(self):
        return ComponentBase(selector=self._image, context=self._we, timeout=1)

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, context=self._we)

    def click(self):
        return self.image.click()

    @property
    def name(self):
        image = self.image
        src = image.get_attribute('src')
        if src:
            regexp = re.search('square/(.*).(jpg|png|jpeg)$', src)
            if not regexp:
                data_src = image.get_attribute('data-src')
                regexp = re.search('square/(.*).(jpg|png|jpeg)$', data_src)
                if not regexp:
                    raise VoltronException(f'Error parsing attributes "src": "{src}" and "data-src": "{data_src}" from recently played game widget item')
            game_name = regexp.group(1)
            if game_name:
                return game_name
            else:
                raise VoltronException(f'Error getting attribute "src" from recently played game widget item. Received "{src}" instead')
        else:
            raise VoltronException(f'Attribute "src" from recently played game widget item is absent!')


class RecentlyPlayedGamesWidget(ComponentBase):
    _iframe = 'xpath=.//div[contains(@class, "rpg-iframe-container visible")]/iframe'
    _rpg_title = 'xpath=.//div[contains(@class, "rpg-title")]'
    _see_more = 'xpath=.//div[contains(@class, "rpg-module-container")]//a[contains(@class, "show-more")]'
    _item = 'xpath=.//div[contains(@class, "carousel-item")]'
    _list_item_type = RecentlyPlayedGame

    @property
    def see_more(self):
        return LinkBase(selector=self._see_more, context=get_driver(), timeout=2)

    @property
    def rpg_title(self):
        return self._get_webelement_text(selector=self._rpg_title, timeout=5)

    @property
    def get_all_game_titles(self):
        items_we = self._find_elements_by_selector(selector=self._item, context=self._context)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        game_titles_list = []
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            game_titles_list.append(list_item.title)
        return game_titles_list

    def stick_to_iframe(self):
        switch_to_iframe(self._iframe)
        return self

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._context)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    def order_of_elements_inside_recently_played_games(self):
        sections_names = OrderedDict()
        module_type_name = {'header': 'title',
                            'div': 'rpg-carousel-thumbnails',
                            'a': 'see-all-gaming-link',
                            }
        order = 0
        all_elements = self._find_elements_by_selector(selector='xpath=.//div[contains(@class,"rpg-module-container")]/*', context=self._context)
        for element in all_elements:
            if element.tag_name in module_type_name:
                sections_names[module_type_name.get(element.tag_name)] = order
                order += 1

        return sections_names
