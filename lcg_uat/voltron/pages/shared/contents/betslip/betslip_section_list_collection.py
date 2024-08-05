from collections import OrderedDict

from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from voltron.pages.shared.components.primitives.collection import Collection
from voltron.utils.exceptions.voltron_exception import VoltronException


class BetSlipSectionsListCollection(Collection):

    def _make_dict(self):
        items_we = self._find_elements_by_selector(selector=self._item)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        self.ordered_collection = OrderedDict()

        try:
            self.__generate_ordered_collection(items_we)
        except (VoltronException, StaleElementReferenceException) as e:
            self._logger.debug(f'*** Overriding {e} in collections class {self.__class__.__name__} method {self.__name__}')
            self.ordered_collection.clear()
            self.__generate_ordered_collection(items_we)

        return self.ordered_collection

    def __generate_ordered_collection(self, items_we):
        for i in range(1, len(items_we) + 1):
            item_component = self._list_item_type(selector=f'{self._item}[{i}]', context=self._we)
            component_name = item_component.name
            if component_name not in self.ordered_collection.keys():
                self.ordered_collection.update({component_name: item_component})
            else:
                for stake_name, stake in item_component.items():
                    self.ordered_collection[component_name].update({stake_name: stake})

            if component_name == 'ACCA':
                self.ordered_collection.update({vec.betslip.MULTIPLES: self._list_item_type(selector=f'{self._item}[{i}]', context=self._we)})
