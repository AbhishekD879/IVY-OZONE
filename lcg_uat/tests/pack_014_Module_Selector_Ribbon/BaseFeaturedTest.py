from time import sleep

from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_featured_structure_changed
from voltron.utils.waiters import wait_for_result


class BaseFeaturedTest(BaseSportTest):
    time_to_wait = 15

    @classmethod
    def custom_site_setup(cls, **kwargs):
        for i in range(0, cls.time_to_wait):
            cls._logger.info(f'Waiting for CMS modules to become available for Featured MS, elapsed time in seconds: {i}')
            sleep(1)

    def is_quick_links_enabled(self) -> bool:
        """
        :return: Verify that quick links is Enabled/Disabled as feature in CMS
        """
        quick_link_enable = self.cms_config.get_initial_data(cached=True).get('Sport Quick Links', {}).get('enabled')
        if not quick_link_enable:
            quick_link_enable = self.get_initial_data_system_configuration().get('Sport Quick Links', {}).get('enabled')
        if not quick_link_enable:
            quick_link_enable = self.cms_config.get_system_configuration_item('Sport Quick Links').get('enabled')
        return quick_link_enable

    def is_quick_link_disabled_for_sport_category(self, sport_id: int = None):
        """
        :param sport_id: int for example for football=16, tennis=34, ID is getting from OpenBet
        :return: bool
        """
        quick_link_module = self.cms_config.get_sport_module(sport_id=sport_id, module_type='QUICK_LINK')[0]
        return quick_link_module.get('disabled')

    def wait_for_featured_module(self, name: str, timeout: float = 60, poll_interval: float = 1,
                                 delimiter: str = '42', expected_result: bool = True, raise_exceptions=True) -> dict:
        """
        Waits for Featured module to appear/disappear from FEATURED_STRUCTURE_CHANGE and asserts the result
        :param name: module name
        :param delimiter: WS message delimiter
        :param timeout: timeout for looking for module
        :param expected_result: True or False
        :param raise_exceptions: whether do assertion or don't
        :return: module object
        """
        module_ = None
        result = wait_for_result(lambda: name in [module.get('title', module['@type']).upper() for module in
                                                  get_featured_structure_changed(delimiter=delimiter).get('modules', [])
                                                  if module['@type'] in self.featured_module_types],
                                 name=f'Featured module "{name}" appears among modules '
                                      f'\n"{[module.get("title", module["@type"]).upper() for module in get_featured_structure_changed(delimiter=delimiter).get("modules", []) if module["@type"] in self.featured_module_types]}"',
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        featured_structure = get_featured_structure_changed(delimiter=delimiter).get("modules", [])
        existing_modules = [module.get('title', module['@type']).upper() for module in featured_structure
                            if module["@type"] in self.featured_module_types]
        if expected_result:
            module_ = next(
                (module for module in featured_structure if module.get('title', module['@type']).upper() == name), None)
            self._logger.debug(f'*** Module title "{module_}"')

        if raise_exceptions:
            self.assertEqual(result, expected_result,
                             msg=f'Module "{name}" presence status "{result}" among modules '
                                 f'\n"{existing_modules}" is not the same as expected "{expected_result}"')
        return module_

    def wait_for_surface_bets(self, name: str, timeout: float = 40, poll_interval: float = 0.6,
                              delimiter: str = '42', expected_result: bool = True, raise_exceptions=True) -> dict:
        """
        Waits for Surface Bets to appear/disappear from FEATURED_STRUCTURE_CHANGE and asserts the result
        :param name: Surface Bet name
        :param delimiter: WS message delimiter
        :param timeout: timeout for looking for module
        :param expected_result: True or False
        :param raise_exceptions: whether do assertion or don't
        :return: module object
        """
        module_ = None
        result = wait_for_result(lambda: name in [submodule.get('title').upper()
                                                  for module in
                                                  get_featured_structure_changed(delimiter=delimiter).get('modules', [])
                                                  for submodule in module.get('data', [])
                                                  if module.get("@type") == "SurfaceBetModule"],
                                 name=f'Surface Bet "{name}" appears among modules '
                                      f'\n"{[submodule.get("title").upper() for module in get_featured_structure_changed(delimiter=delimiter).get("modules", []) for submodule in module.get("data", []) if module.get("@type") == "SurfaceBetModule"]}"',
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 bypass_exceptions=(IndexError, KeyError, TypeError))
        featured_structure = get_featured_structure_changed(delimiter=delimiter).get("modules", [])
        existing_modules = [submodule.get('title').upper()
                            for module in featured_structure
                            for submodule in module.get('data', [])
                            if module.get("@type") == "SurfaceBetModule"]
        self._logger.info(f'*** Existing modules {existing_modules}')
        if expected_result:
            module_ = next((submodule for module in featured_structure
                            for submodule in module.get('data', []) if submodule.get('title', '').upper() == name
                            if module.get("@type") == "SurfaceBetModule"), None)
            self._logger.info(f'*** Module title "{module_}"')

        if raise_exceptions:
            self.assertEqual(result, expected_result,
                             msg=f'Surface Bet "{name}" presense status "{result}" among modules '
                                 f'\n"{existing_modules}" is not the same as expected "{expected_result}"')
        return module_

    def wait_for_quick_link_from_response(self, name: str, timeout: float = 40, poll_interval: float = 0.6,
                                          delimiter: str = '42', expected_result: bool = True,
                                          raise_exceptions=True) -> dict:
        """
        Waits for Quick Link to appear/disappear from FEATURED_STRUCTURE_CHANGE and asserts the result
        :param name: Quick Link name
        :param timeout: timeout for looking for module
        :param delimiter: WS message delimiter
        :param expected_result: True or False
        :param raise_exceptions: whether do assertion or don't
        :return: module object
        """
        module_ = None
        result = wait_for_result(lambda: name in [submodule.get('title')
                                                  for module in
                                                  get_featured_structure_changed(delimiter=delimiter).get('modules', [])
                                                  for submodule in module.get('data', [])
                                                  if module.get("@type") == "QuickLinkModule"],
                                 name=f'Quick Link module "{name}" appears among modules '
                                      f'\n"{[submodule.get("title") for module in get_featured_structure_changed(delimiter=delimiter).get("modules", []) for submodule in module.get("data", []) if module.get("@type") == "QuickLinkModule"]}"',
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 bypass_exceptions=(IndexError, KeyError, TypeError))
        featured_structure = get_featured_structure_changed(delimiter=delimiter).get("modules", [])
        existing_modules = [submodule.get('title')
                            for module in featured_structure
                            for submodule in module.get('data', [])
                            if module.get("@type") == "QuickLinkModule"]
        self._logger.info(f'*** Existing modules {existing_modules}')
        if result:
            module_ = next(
                (submodule for module in featured_structure
                 for submodule in module.get('data', []) if submodule.get('title', '') == name
                 if module.get("@type") == "QuickLinkModule"), None)
            self._logger.info(f'*** Module title "{module_}"')

        if raise_exceptions:
            self.assertEqual(result, expected_result,
                             msg=f'Quick link "{name}" presense status "{result}" among modules '
                                 f'\n"{existing_modules}" is not the same as expected "{expected_result}"')
        return module_

    def wait_for_highlights_carousels(self, name: str, delimiter: str = '42', expected_result: bool = True,
                                      timeout: float = 30, poll_interval: float = 0.6,
                                      raise_exceptions: bool = True) -> dict:
        """
        Waits for Highlights Carousel to appear/disappear from FEATURED_STRUCTURE_CHANGE and asserts the result
        :param name: Highlights carousel name
        :param delimiter: WS message delimiter
        :param timeout: timeout for looking for module
        :param expected_result: True or False
        :param raise_exceptions: whether do assertion or don't
        :return: module object
        """
        name = name.upper()  # name is expected always as UPPER case
        result = wait_for_result(lambda: self.wait_for_featured_module(name=name,
                                                                       delimiter=delimiter,
                                                                       raise_exceptions=False,
                                                                       timeout=1,
                                                                       expected_result=expected_result),
                                 timeout=timeout,
                                 bypass_exceptions=AttributeError)

        if not result:
            for _ in range(0, 2):
                self.device.refresh_page()
                self.site.wait_splash_to_hide()
                result = wait_for_result(lambda: self.wait_for_featured_module(name=name,
                                                                               delimiter=delimiter,
                                                                               timeout=1,
                                                                               poll_interval=poll_interval,
                                                                               expected_result=expected_result),
                                         timeout=timeout,
                                         bypass_exceptions=AttributeError)
                if result:
                    break
            return result

    def wait_for_quick_link(self, name: str, timeout: float = 30, poll_interval: float = 0.6,
                            delimiter: str = '42', expected_result: bool = True, raise_exceptions=False) -> dict:
        """
        Waits for Quick Link to appear/disappear from FEATURED_STRUCTURE_CHANGE and asserts the result
        :param name: Quick Link name
        :param timeout: timeout for looking for module
        :param delimiter: WS message delimiter
        :param expected_result: True or False
        :param raise_exceptions: whether do assertion or don't
        :return: module object
        """
        result = self.wait_for_quick_link_from_response(name=name, timeout=timeout, delimiter=delimiter, poll_interval=1,
                                                        raise_exceptions=raise_exceptions, expected_result=expected_result)
        if bool(result) is not expected_result:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            result = self.wait_for_quick_link_from_response(name=name, timeout=timeout, delimiter=delimiter,
                                                            poll_interval=1, expected_result=expected_result)

        return result

    def verify_quick_link_displayed(self, name: str = None, expected_result: bool = True, page_name='home', timeout: int = 15) -> None:
        """
        :param name: str
        :param expected_result: True/False
        :param page_name: name of page to display
        :param timeout: timeout
        :return:
        """
        page = getattr(self.site, page_name, None)
        has_links = page.tab_content.has_quick_links()

        def check_links():
            if has_links:
                quick_links_section = page.tab_content.quick_links

                result = wait_for_result(lambda: next((True for ql_name in quick_links_section.items_as_ordered_dict.keys() if ql_name == name or (ql_name[-3:] == '...' and name[:len(ql_name) - 3] + '...' == ql_name)), False),
                                         name=f'Quick link "{name}" to presence status to "{expected_result}"',
                                         expected_result=expected_result,
                                         timeout=timeout)
                self.assertEqual(result, expected_result,
                                 msg=f'Quick link "{name}" presence status "{result}" is not the same as expected "{expected_result}"')
            else:
                return False

        if expected_result:
            self.assertTrue(has_links, msg=f'Quick links module was not found on "{page_name}"')
            check_links()
        else:
            check_links()

    def check_event_is_active(self, event_id: (str, int)) -> bool:
        """
        Checks if event with given id is active (event status code is active, market status code is active, outcomes status codes are active
        :param event_id: id of event
        :return: True or False depending if event is active or not
        """
        query = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A'))\
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.MARKET_STATUS_CODE, OPERATORS.EQUALS, 'A')))\
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A')))

        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id, query_builder=query, raise_exceptions=False)
        return True if resp else False

    @retry(stop=stop_after_attempt(3),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), wait=wait_fixed(wait=2),
           reraise=True)
    def get_module(self, module_content_name, module_name):
        """
        Get module from module on home page
        :param module_content_name: module name
        :param module_name: created module name
        :return: module
        """
        module_content = self.site.home.get_module_content(module_name=module_content_name)
        module_content.scroll_to()
        module = module_content.accordions_list.items_as_ordered_dict.get(module_name)
        return module
