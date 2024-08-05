from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.contents.base_contents.racing_base_components.meeting_selector import MeetingListSection
from voltron.pages.shared.contents.base_contents.racing_base_components.meeting_selector import MeetingsList
from voltron.pages.shared.contents.edp.racing_event_details import PostInfo
from voltron.pages.shared.contents.edp.racing_event_details import RacingEDPTabContent
from voltron.pages.shared.components.racing_post_verdict_overlay import RacePostVerdictOverlayDesktop
from voltron.pages.shared.contents.edp.racing_event_details import RacingEventDetails
from voltron.utils.waiters import wait_for_result


class PostInfoDesktop(PostInfo, Accordion):
    pass


class RacingEDPTabContentDesktop(RacingEDPTabContent):
    _post_info_accordion = 'xpath=.//*[@data-crlat="racingPostContainer"]//*[@data-crlat="accordion"]'
    _watch_free_logo = 'xpath=.//*[@data-crlat="wFLogo"]'

    def has_post_info(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._post_info_accordion,
                                                   timeout=0) is not None,
            name=f'Post info status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_watch_free_logo(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._watch_free_logo,
                                                   timeout=0) is not None,
            name=f'"Watch Free" logo to appear"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def post_info(self):
        return PostInfoDesktop(selector=self._post_info_accordion, context=self._we)


class MeetingListSectionDesktop(MeetingListSection):
    # _name = 'xpath=.//*[@data-crlat="dropdown.menuTitle" or @data-crlat="meetingName"]'

    # @property
    # def name(self):
    #     return self._get_webelement_text(selector=self._name, context=self._we, timeout=1)
    pass

class MeetingsListDesktop(MeetingsList):
    # _item = 'xpath=.//*[@data-crlat="dropdown.menuItem" or @data-crlat="meetingItem"][*]'
    _list_item_type = MeetingListSectionDesktop


class RacingEventDetailsDesktop(RacingEventDetails):
    _tab_content_type = RacingEDPTabContentDesktop
    _meetings_list_type = MeetingsListDesktop
    _meeting_selector = 'xpath=.//*[@data-crlat="dropdown"] | .//*[@data-crlat="meetingSelector"]'
    _meetings_list = 'xpath= .//*[@data-crlat="dropdownMenu"] | .//*[@data-crlat="racingMeetingsContainer" or @class="desktop-list"]'
    _racing_post_verdict = 'xpath=.//*[@data-crlat="racingPostContainer"]//accordion'

    @property
    def racing_post_verdict(self):
        racing_post_verdict = self._find_element_by_selector(selector=self._racing_post_verdict, context=self._we,
                                                             timeout=2)
        return RacePostVerdictOverlayDesktop(web_element=racing_post_verdict) if racing_post_verdict else None

    @property
    def meetings_list(self):
        return MeetingsListDesktop(selector=self._meetings_list, context=self._we)
