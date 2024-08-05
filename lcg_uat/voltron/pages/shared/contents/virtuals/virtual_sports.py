from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.edp.racing_event_details import RacingEventDetails
from voltron.pages.shared.contents.virtuals.racing_tab_content import VirtualRacingTabContent
from voltron.pages.shared.contents.virtuals.sport_tab_content import VirtualSportTabContent
from voltron.pages.shared.contents.virtuals.sports_carousel import VirtualSportsCarousel
from voltron.utils.waiters import wait_for_result


class VirtualSports(RacingEventDetails):
    _url_pattern = r'^https?:\/\/.+\/virtual-sports|(\/)?' \
                   '(virtual-horse-racing|virtual-greyhounds|virtual-football|virtual-grand-national|' \
                   'virtual-motorsports|virtual-darts|virtual-boxing|virtual-cycling|virtual-speedway|virtual-tennis)'
    _sport_carousel = 'xpath=.//*[@data-crlat="virtualMenuCarousel"]'
    _sport_carousel_type = VirtualSportsCarousel
    _tab_content_type = VirtualRacingTabContent
    _tab_content_type_racing = VirtualRacingTabContent
    _tab_content_type_sport = VirtualSportTabContent
    _sport_event_header = 'xpath=.//*[@data-crlat="virtualSportsHeader"]'  # visible for ladbrokes only
    _no_sport_event_message = 'xpath=.//*[@data-crlat="errorMessageText"]'
    _switchers = 'xpath=.//*[@data-crlat="switchers"]'

    def has_switchers(self, expected_result=True, timeout=0.5):
        """
        Used only to determine if Racing: W or EW/Forecast/Tricast tabs + outcomes (same as racing edp)
                               or Sport: No market tabs but market accordions (same as sport edp)
                                        virtual page is shown
        Checked same way as it's done on BMA side:
        src/app/vsbr/components/virtualSportClasses/virtual-sport-classes.component.html:44
                                        *ngIf="hasWinOrEachWay" [ngSwitch]="filter"
        :param expected_result:
        :param timeout:
        :return:
        """
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._switchers, timeout=0) is not None,
                               name=f'Switchers shown status to be "{expected_result}"',
                               timeout=timeout)

    @property
    def sport_carousel(self):
        return self._sport_carousel_type(selector=self._sport_carousel, context=self._we)

    @property
    def tab_content(self):
        tab_content_type = self._tab_content_type_racing if self.has_switchers() else self._tab_content_type_sport
        return tab_content_type(selector=self._tab_content, context=self._we)

    @property
    def sport_event_header(self):
        return ComponentBase(selector=self._sport_event_header, context=self._we)

    @property
    def no_sport_event_message(self):
        return self._get_webelement_text(selector=self._no_sport_event_message, context=self._we)
