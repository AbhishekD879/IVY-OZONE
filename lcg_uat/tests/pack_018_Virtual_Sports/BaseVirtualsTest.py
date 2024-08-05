from copy import copy
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
import voltron.environments.constants as vec


class BaseVirtualsTest(Common):
    _virtual_carousel_menu_items = None

    @property
    def virtual_carousel_menu_items(self):
        cms = self.cms_config
        if not self._virtual_carousel_menu_items:
            self._virtual_carousel_menu_items = cms.get_virtual_carousel_menu_items()
        return self._virtual_carousel_menu_items

    def get_runner_bet_buttons(self, index: int = 0) -> list:
        """
        This method get list of runner buttons for outcome
        :param index: int
        :return list of runner buttons for outcome
        """
        def check_current_tab():
            current_tab = self.site.virtual_sports.tab_content.event_markets_list.market_tabs_list.current
            expected_tabs = [vec.racing.RACING_EDP_TRICAST_MARKET_TAB, vec.racing.RACING_EDP_FORECAST_MARKET_TAB]
            if current_tab not in expected_tabs:
                raise VoltronException('Virtual sport content refreshed, could not verify the page')

        check_current_tab()
        sections = self.site.virtual_sports.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections were found')
        self.__class__.outcome_name, outcome = list(sections.items())[index]
        runner_buttons = outcome.items_as_ordered_dict
        check_current_tab()
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{self.outcome_name}"')
        return list(runner_buttons.values())

    def cms_virtual_sports_class_ids(self) -> list:
        """
        :return: List of configured Virtual sports classIds
        """
        cms_class_ids = [tracks.get('classId') for item in self.virtual_carousel_menu_items for tracks in item.get('tracks', None)]
        return cms_class_ids

    def cms_virtual_sport_tab_name_by_class_ids(self, class_ids: list) -> list:
        """
        :param class_ids: active events ids list from SS response
        :return: title from CMS
        """
        tracks = [item for id in class_ids for item in self.virtual_carousel_menu_items
                  for tracks in item.get('tracks', None) if tracks.get('classId', None) == id]
        titles = [i['title'] for i in tracks]
        self._logger.debug(f'*** Found tabs: {titles}')
        return titles

    def get_cms_unique_virtual_sport_tab_name_by_class_ids_by_cms_order(self, class_ids: list) -> list:
        """
        Get unique displayed tab_names including cms order
        :param class_ids: active events ids list from SS response
        :return: title from CMS
        """
        displayed_tab_names = []
        for item in self.virtual_carousel_menu_items:
            for child in item.get('tracks'):
                if child.get('classId') in class_ids and item.get('title') not in displayed_tab_names:
                    displayed_tab_names.append(item.get('title'))
        self._logger.debug(f'*** Found tabs: {displayed_tab_names}')
        return displayed_tab_names

    def get_parent_virtual_sport_with_more_than_one_child(self, child_ids: list):
        """
        Find and get parent virtual sport that have at least two active children
        :param child_ids: child ids
        :return: Dict with parent sport name/id
        """
        result = {}
        child_ids = list(set(copy(child_ids)))  # to make sure all ids are unique and save income list in previous state
        for item in self.virtual_carousel_menu_items:
            item_child_ids = [child.get('classId') for child in item.get('tracks')]
            available_children = [item_child_id for item_child_id in item_child_ids if item_child_id in child_ids]
            if len(available_children) >= 2:
                parent_name = item.get('title')
                parent_id = item.get('id')
                self._logger.debug(f'*** Found parent: {parent_name}')

                result.update({parent_name: parent_id})
        return result

    def get_virtual_sport_ids(self):
        sports = self.cms_config.get_virtual_carousel_menu_items()
        ids = [item.get('id') for item in sports]
        return ids

    def get_child_virtual_sport_ids_for_parent(self, parent_sport_name):
        sports = self.cms_config.get_virtual_carousel_menu_items()
        parent_sport = next((item for item in sports if item.get('title') == parent_sport_name), None)
        if not parent_sport:
            raise CmsClientException(f'Cannot find "{parent_sport_name}"')
        children_ids = [child.get('id') for child in parent_sport.get('tracks')]
        return children_ids
