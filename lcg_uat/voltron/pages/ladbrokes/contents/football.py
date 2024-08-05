from voltron.pages.ladbrokes.components.fanzone_banner import FanZoneBanner
from voltron.pages.ladbrokes.contents.base_contents.sport_base import LadbrokesSportPageBase
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.football import SportPageDesktop
from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content_desktop import \
    CompetitionsTabContentDesktop
from voltron.utils.waiters import wait_for_result


class LadbrokesMobileFootball(LadbrokesSportPageBase):
    _url_pattern = r'^https?:\/\/.+\/football(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'
    _league_icon = 'xpath=.//*[@data-crlat="link.searchLeagues"]'
    _fanzone_banner = 'xpath=.//*[contains(@class, "fanzone-banner")]'
    _syc_popup = 'xpath=.//*[@class="modal-dialog"]'

    @property
    def league_icon(self):
        return ComponentBase(selector=self._league_icon)

    def fanzone_banner(self, timeout=10):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._fanzone_banner, context=self._we,
                                                                        timeout=5) is not None,
                                 timeout=timeout,
                                 name='Waiting for fanzone banner to display')
        if result:
            return FanZoneBanner(selector=self._fanzone_banner, context=self._we, timeout=5)
        else:
            return result

    def has_syc_popup(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._syc_popup, timeout=2) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'SYC popup shown status to be "{expected_result}"'
        )


class LadbrokesDesktopFootball(SportPageDesktop):
    _url_pattern = r'^https?:\/\/.+\/football(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'
    _competitions_tab = CompetitionsTabContentDesktop
    _fanzone_banner = 'xpath=.//*[contains(@class, "fanzone-banner")]'
    _syc_popup = 'xpath=.//*[@class="modal-dialog"]'

    def fanzone_banner(self, timeout=10):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._fanzone_banner, context=self._we,
                                                                        timeout=5) is not None,
                                 timeout=timeout,
                                 name='Waiting for fanzone banner to display')
        if result:
            return FanZoneBanner(selector=self._fanzone_banner, context=self._we, timeout=5)
        else:
            return result

    def has_syc_popup(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._syc_popup, timeout=2) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'SYC popup shown status to be "{expected_result}"'
        )
