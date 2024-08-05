from voltron.pages.shared.components.base import ComponentBase


class MiniGameCoral(ComponentBase):
    _verify_spinner = True

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)
