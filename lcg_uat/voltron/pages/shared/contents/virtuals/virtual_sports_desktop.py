from voltron.pages.shared.components.breadcrumbs import Breadcrumbs
from voltron.pages.shared.contents.virtuals.virtual_sports import VirtualSports


class VirtualSportsDesktop(VirtualSports):
    _breadcrumbs_type = Breadcrumbs
    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs, context=self._we)
