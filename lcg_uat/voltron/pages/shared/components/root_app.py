from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class RootApp(ComponentBase):
    _expected_shown_style = 'display: inline;'
    _timeline_overlay_tutorial = 'xpath=.//*[@id="timeline-tutorial-overlay"]/div[contains(@class, "tlt")]'
    _loss_limit_dialog = 'xpath=.//*[@class="dlg-responsive-content"]'
    _fanzone_cb_overlay = 'xpath=.//fanzone-cb-overlay//div[@class="FCB-Popup"]'
    _bwin_hint = 'xpath=.//vn-hint//span[@class]'

    def wait_to_show(self, timeout=25):
        name = self.__class__.__name__
        if self.get_attribute('style'):
            wait_for_result(
                lambda: (self.get_attribute('style') == self._expected_shown_style) and self.is_displayed(timeout=0),
                name=f'{name} to show',
                expected_result=True,
                timeout=timeout
            )

    def has_loss_limit_dialog(self, timeout=5, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._loss_limit_dialog,
                                                   timeout=timeout) is not None,
            name=f'Loss limit dialog to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_timeline_overlay_tutorial(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._timeline_overlay_tutorial,
                                                   timeout=timeout) is not None,
            name=f'Timeline overlay Tutorial to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_fanzone_cb_overlay(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._fanzone_cb_overlay,
                                                   timeout=2) is not None,
            name=f'Timeline overlay Tutorial to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_biwin_hint(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._bwin_hint,
                                                   timeout=2) is not None,
            name=f'Timeline overlay Tutorial to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
