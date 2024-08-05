from voltron.pages.ladbrokes.contents.edp.racing_event_details import EventMarketsListLadbrokes, \
    RacingEventDetailsLadbrokes, RacingEDPTabContentLadbrokes
from voltron.pages.shared.contents.edp.greyhound_event_details import GreyHoundEDPTabContent, GreyHoundSubHeader, \
    GreyHoundEventDetails


class GreyhoundEventMarketsListLadbrokes(EventMarketsListLadbrokes):
    _forecast_tricast = 'xpath=.//*[@data-crlat="raceCard.forTri"]'


class GreyHoundEDPTabContentLadbrokes(GreyHoundEDPTabContent, RacingEDPTabContentLadbrokes):
    _event_markets_list_type = GreyhoundEventMarketsListLadbrokes
    _status = 'xpath=.//*[@class="race-details-container-l"]/div[2]/span'  # TODO: VOL-4170


class LadbrokesGreyHoundSubHeader(GreyHoundSubHeader):
    _meeting_selector = 'xpath=.//*[@data-crlat="meetingSelector"]'


class GreyHoundEventDetailsLadbrokes(GreyHoundEventDetails, RacingEventDetailsLadbrokes):
    _tab_content_type = GreyHoundEDPTabContentLadbrokes
    _url_pattern = r'^http[s]?:\/\/.+\/(greyhound-racing)\/[\w-]+\/[\w-]+\/[\w-]+\/[0-9]+\/[\w-]+'
    _sub_header_type = LadbrokesGreyHoundSubHeader

    @property
    def event_name(self):
        return self.event_title


class GreyHoundEventDetailsLadbrokesDesktop(GreyHoundEventDetailsLadbrokes):
    _tab_content_type = GreyHoundEDPTabContent
