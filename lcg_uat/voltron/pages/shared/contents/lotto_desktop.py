from voltron.pages.shared.contents.football import SportPageDesktop
from voltron.pages.shared.contents.lotto import Lotto


class LottoDesktop(Lotto, SportPageDesktop):
    @property
    def tab_content(self):
        return self._tab_content_type(selector=self._tab_content)
