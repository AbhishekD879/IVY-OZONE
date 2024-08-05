from voltron.pages.shared.contents.edp.byb_event_details import BYBEventDetailsTabContent
from voltron.pages.shared.contents.edp.byb_event_details import BYBMarketsSectionsList
from voltron.pages.ladbrokes.components.byb_dashboard import LadbrokesBYBDashboardSection


class LadbrokesBYBMarketsSectionsList(BYBMarketsSectionsList):
    _item = 'xpath=.//accordion[contains(@class, "first")] | .//accordion[contains(@class, "second")]'


class LadbrokesBYBEventDetailsTabContent(BYBEventDetailsTabContent):
    _accordions_list_type = LadbrokesBYBMarketsSectionsList

    @property
    def dashboard_panel(self):
        return LadbrokesBYBDashboardSection(selector=self._yourcall_dashboard_panel, context=self._we, timeout=1)
