package com.ladbrokescoral.oxygen.buildyourbetms.handler

import com.ladbrokescoral.oxygen.buildyourbetms.handler.impl.EventsHandler
import com.ladbrokescoral.oxygen.buildyourbetms.util.Message
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient
import org.springframework.web.reactive.function.server.ServerRequest
import spock.lang.Specification

class EventsHandlerTest extends Specification {
  def webClient = Mock(BanachClient)

  def "When leaguesId contains malformed id - NumberFormatException is thrown"() {
    given:
    def handler = new EventsHandler(webClient)
    def request = Mock(ServerRequest)
    request.queryParam("dateFrom") >> Optional.of("2018-05-23T17:14:00.000Z")
    request.queryParam("dateTo") >> Optional.of("2018-05-23T17:14:00.000Z")
    request.queryParam("leagueIds") >> Optional.ofNullable("abc,557")
    when:
    def resp = handler.handle(request)
    then:
    NumberFormatException ex = thrown()
  }

  def "ISO8601 is converted to timestamp"() {
    given:
    def iso8601date = "2018-05-23T17:14:00.000Z"
    when:
    def timestampMillis = EventsHandler.fromIsoDateToTimeStamp(iso8601date)
    then:
    timestampMillis == 1527095640000
    Message test = new Message()
    test.setMessage("test")
    test.toString()
    test.getMessage()
  }
}
