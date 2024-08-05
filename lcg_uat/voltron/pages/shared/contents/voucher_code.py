from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.info_panel import InfoPanel
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.contents.base_content import BaseContent


class SportsForm(ComponentBase):
    _voucher_code = 'xpath=.//*[@data-crlat="inputVoucherCode"]'
    _claim_now_button = 'xpath=.//*[@data-crlat="buttonSubmit"]'
    _view_all_offers_button = 'xpath=.//*[@data-crlat="buttonOpenPromotions"]'

    @property
    def voucher_input(self):
        return InputBase(selector=self._voucher_code, context=self._we)

    @property
    def claim_now_button(self):
        return ButtonBase(selector=self._claim_now_button, context=self._we)

    @property
    def view_offers_button(self):
        return ButtonBase(selector=self._view_all_offers_button, context=self._we)


class VoucherCode(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/voucher-code'
    _sports_form = 'xpath=.//*[@data-crlat="voucherForm"]'
    _message = 'xpath=.//*[@data-crlat="voucherMessage"]'
    _info_panel = 'xpath=.//*[@data-crlat="infPan.msg" and not(contains(@class, "ng-hide"))]'

    @property
    def sports_form(self):
        return SportsForm(web_element=self._find_element_by_selector(selector=self._sports_form))

    @property
    def info_panels(self):
        return InfoPanel(selector=self._info_panel, context=self._we, timeout=5)

    @property
    def info_panels_text(self):
        return self.info_panels.texts
