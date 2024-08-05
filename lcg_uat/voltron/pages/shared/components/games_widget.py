
from voltron.pages.shared.components.base import ComponentBase


class MiniGameWidget(ComponentBase):

    def _load_complete(self, timeout=None):
        """
        Waits for component to load. Most commonly component is considered to be loaded if splash disappears and url is
        changed (if applicable) or spinner to disappear
        :param timeout:
        :return:
        """
        return self._spinner_wait()

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)
