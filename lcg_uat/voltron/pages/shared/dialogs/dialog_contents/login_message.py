from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.text_labels import LinkBase


class LoginMessageDialog(Dialog):
    _dialog_content = 'xpath=.//*[@class="modal-body"]'
    _link = 'xpath=.//a[text()="Reactivation page"]'   # Can not add custom attributes since it comes from IMS

    @property
    def text(self):
        return self._get_webelement_text(selector=self._dialog_content, context=self._we)

    @property
    def link(self):
        return LinkBase(selector=self._link, context=self._we)
