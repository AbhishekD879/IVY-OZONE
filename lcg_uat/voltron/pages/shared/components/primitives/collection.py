from collections import OrderedDict

from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException


class Collection(ComponentBase):

    def _make_dict(self):
        items_we = self._find_elements_by_selector(selector=self._item)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        self.ordered_collection = OrderedDict()
        try:
            for i in range(1, len(items_we) + 1):
                item_component = self._list_item_type(selector='%s[%s]' % (self._item, i), context=self._we)
                component_name = item_component.name
                if component_name in self.ordered_collection.keys():
                    component_name = component_name + ' - ' + item_component.event_name
                    # todo: also might need to add market name here.
                self.ordered_collection.update({component_name: item_component})
        except (VoltronException, StaleElementReferenceException) as e:
            self._logger.debug(f'*** Overriding {e} in collections class {self.__class__.__name__} method {self.__name__}')
            self.ordered_collection.clear()
            for i in range(1, len(items_we) + 1):
                item_component = self._list_item_type(selector='%s[%s]' % (self._item, i), context=self._we)
                component_name = item_component.name
                if component_name in self.ordered_collection.keys():
                    component_name = component_name + ' - ' + item_component.event_name
                    # todo: also might need to add market name here.
                self.ordered_collection.update({component_name: item_component})
        return self.ordered_collection

    def __init__(self, selector='', context=None, web_element=None, timeout=15, pattern_values=None, *args, **kwargs):
        if web_element:
            raise VoltronException('Collection can\'t be initialised by web_element')
        super(Collection, self).__init__(selector=selector, context=context, web_element=web_element, timeout=timeout, pattern_values=pattern_values, *args, **kwargs)
        try:
            self._make_dict()
        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Overriding {e} in collections class {self.__class__.__name__} method {self.__name__}')
            self._we = self._find_myself()
            self._make_dict()

    def __getitem__(self, key):
        try:
            item = self.ordered_collection[key]
            item._we.is_displayed()
            return item
        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Overriding {e} in collections class {self.__class__.__name__} method {self.__name__}')
            self._we = self._find_myself()
            self._make_dict()
            return self.ordered_collection[key]

    def __iter__(self):
        """is called when an iterator is required for a collection. returns a new iterator object"""
        try:
            return iter(self.ordered_collection)
        except StaleElementReferenceException as e:
            self._logger.debug('*** Overriding %s in collections method %s' % (e, self.__name__))
            self._we = self._find_myself()
            self._make_dict()
            return iter(self.ordered_collection)

    def __contains__(self, key):
        """key in od -> membership test operator. return true if key is in ordered dict, false otherwise"""
        try:
            return key in self.ordered_collection
        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Overriding {e} in collections class {self.__class__.__name__} method {self.__name__}')
            self._we = self._find_myself()
            self._make_dict()
            return key in self.ordered_collection

    def __len__(self):
        """len(od) -> length of collection"""
        return len(self.ordered_collection)

    def __getattr__(self, name):
        try:
            return getattr(Collection, name)
        except KeyError as e:
            raise AttributeError(e)

    def __str__(self):
        """ x.__str__() <==> str(x) -> gets string representation of ordered dictionary"""
        return str(self.ordered_collection)

    def keys(self):
        """od.keys() -> list of keys in ordered dictionary"""
        return list(self.ordered_collection)

    def values(self):
        """od.values() -> list of values in ordered dictionary"""
        return [self.ordered_collection[key] for key in self.ordered_collection]

    def items(self):
        """od.items() -> list of (key, value) pairs in ordered dictionary"""
        try:
            return [(key, self.ordered_collection[key]) for key in self.ordered_collection if self.ordered_collection[key]._we.is_displayed()]
        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Overriding {e} in collections class {self.__class__.__name__} method {self.__name__}')
            self._we = self._find_myself()
            self._make_dict()
            return [(key, self.ordered_collection[key]) for key in self.ordered_collection if self.ordered_collection[key]._we.is_displayed()]

    def iteritems(self):
        """od.iteritems -> an iterator over the (key, value) pairs in ordered dictionary"""
        try:
            for k in self:
                yield (k, self.ordered_collection[k])
        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Overriding {e} in collections class {self.__class__.__name__} method {self.__name__}')
            self._we = self._find_myself()
            self._make_dict()
            for k in self:
                yield (k, self.ordered_collection[k])

    def pop(self, *args):
        """od.pop(k[,d]) -> v, remove specified key and return the corresponding
        value.  If key is not found, d is returned if given, otherwise KeyError
        is raised."""
        return self.ordered_collection.pop(*args)

    def clear(self):
        """od.clear() -> None.  Remove all items from ordered dictionary"""
        return self.ordered_collection.clear()

    def get(self, *args):
        """od.get(k[,d]) -> D[k] if k in D, else d. d defaults to None."""
        return self.ordered_collection.get(*args)

    def copy(self):
        """od.copy() -> a shallow copy of ordered dictionary"""
        return self.ordered_collection.copy()

    def update(self, *args):
        """Like dict.update() but add counts instead of replacing them."""
        return self.ordered_collection.update(*args)

    @property
    def items_as_ordered_dict(self):
        raise VoltronException('items_as_ordered_dict should not be called on Collection.'
                               'Collection is OrderedDict() itself')
