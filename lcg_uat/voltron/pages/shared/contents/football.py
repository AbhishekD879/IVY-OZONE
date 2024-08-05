from voltron.pages.shared.components.live_stream_widget import LiveStreamWidgetEventCardBody
from voltron.pages.shared.components.right_column_widgets.in_play_widget import WidgetAccordionList
from voltron.pages.shared.contents.base_contents.sport_base import SportPageBase
from voltron.pages.shared.components.breadcrumbs import Breadcrumbs


class SportPage(SportPageBase):
    """
    This wrapper is needed in case we don't really know the sport page name we are on.
    And also so we do not import SportPageBase in bma_site directly (in this case we have cross-import error)
    """
    _verify_spinner = True


class SportPageDesktop(SportPageBase):
    """
    This wrapper is needed in case we don't really know the sport page name we are on.
    And also so we do not import SportPageBase in bma_site directly (in this case we have cross-import error)
    """
    _breadcrumbs_type = Breadcrumbs
    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'
    _in_play_widget = 'xpath=.//*[@data-uat="widgetColumn"]'
    _live_stream_widget = 'xpath=.//*[@data-crlat="lsWidget"]'

    @property
    def in_play_widget(self):
        return WidgetAccordionList(selector=self._in_play_widget, context=self._we)

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs, context=self._we)

    @property
    def live_stream_widget(self):
        return LiveStreamWidgetEventCardBody(selector=self._live_stream_widget, context=self._we)


class Football(SportPageBase):
    _url_pattern = r'^https?:\/\/.+\/football(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'
    _league_icon = 'xpath=.//*[@data-crlat="link.searchLeagues"]'

    @property
    def league_icon(self):
        return self._find_element_by_selector(selector=self._league_icon)


class FootballDesktop(SportPageDesktop):
    _url_pattern = r'^https?:\/\/.+\/football(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'
