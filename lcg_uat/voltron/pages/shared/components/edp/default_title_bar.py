from voltron.pages.shared import get_device_properties
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.helpers import normalize_name


class DefaultTitleBar(ComponentBase):
    _event_name = 'xpath=.//*[@data-crlat="eventEntity.name" or @data-crlat="topBarTitle"]'
    _event_time = 'xpath=.//*[@data-crlat="eventEntity.filteredTime"]'
    _live_now_label = 'xpath=.//*[@data-crlat="liveLabel"]'

    @property
    def event_name_we(self):
        return TextBase(selector=self._event_name, context=self._we)

    @property
    def event_name(self):
        text = normalize_name(self._get_webelement_text(selector=self._event_name, timeout=3))
        device_type = get_device_properties()['type']
        if device_type == 'desktop':
            text = text.replace(' v ', ' V ')
        return text

    @property
    def event_name_without_scores(self):
        return self.event_name

    @property
    def home_team_name(self):
        event_name = self.event_name.split(' v ') if ' v ' in self.event_name else self.event_name.split(' vs ')
        return event_name[0]

    @property
    def away_team_name(self):
        event_name = self.event_name.split(' v ') if ' v ' in self.event_name else self.event_name.split(' vs ')
        return event_name[1]

    @property
    def event_time_we(self):
        return TextBase(selector=self._event_time, context=self._we)

    @property
    def event_time(self):
        return self._get_webelement_text(selector=self._event_time, timeout=0.5).replace('LIVE\n', '')

    @property
    def live_now_icon(self):
        return IconBase(selector=self._live_now_label, timeout=0.5, context=self._we)

    @property
    def is_live_now_event(self):
        return self._find_element_by_selector(selector=self._live_now_label, timeout=0) is not None

    @property
    def event_time_icon(self):
        return IconBase(selector=self._event_time, timeout=0.5, context=self._we)
