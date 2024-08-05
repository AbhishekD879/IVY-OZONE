package com.ladbrokescoral.oxygen.buildyourbetms.handler

import com.ladbrokescoral.oxygen.buildyourbetms.handler.impl.LeaguesUpcomingHandler
import com.ladbrokescoral.oxygen.buildyourbetms.util.TestUtils
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClients
import com.ladbrokescoral.oxygen.byb.banach.client.LeaguesBanachClient
import org.springframework.web.reactive.function.server.ServerRequest
import reactor.core.publisher.Mono
import spock.lang.Specification

import java.time.Clock
import java.time.Instant
import java.time.ZoneId

class LeaguesUpcomingHandlerTest extends Specification {

  private FacadeHandler handler
  private ServerRequest request = Mock()
  private LeaguesBanachClient leaguesClientMock = Mock()

  def setup() {

    mockLeaguesUpcomingHandlerWithFixedClock(1527601168L)

    def headers = Mock(ServerRequest.Headers)
    headers.header("X-Correlation-Id") >> Mock(List)

    request.headers() >> headers
  }

  private void mockLeaguesUpcomingHandlerWithFixedClock(long mockedTimestampOfNow) {
    leaguesClientMock.execute(*_) >> {
      print "Invoked: " + it
      return Mono.empty()
    }
    def fixedClock = Clock.fixed(Instant.ofEpochSecond(mockedTimestampOfNow), ZoneId.of("UTC"))
    handler = new LeaguesUpcomingHandler(leaguesClientMock, fixedClock)
  }

  def "today and upcoming are combined from different streams"() {
    given:
    def today = Mono.just(TestUtils.createLeagues(1L, 2L))
    def upcoming = Mono.just(TestUtils.createLeagues(3L, 4L))
    when:
    def result = LeaguesUpcomingHandler.combineTodayAndUpcoming(today, upcoming);
    then:
    def block = result.block();
    block.today.size() == 2
    block.today*.obTypeId.sort() == [1L, 2L]
    block.upcoming.size() == 2
    block.upcoming*.obTypeId.sort() == [3L, 4L]
  }

  def "today is present, upcoming is empty mono"() {
    given:
    def today = Mono.just(TestUtils.createLeagues(1L, 2L))
    def upcoming = Mono.empty()
    when:
    def result = LeaguesUpcomingHandler.combineTodayAndUpcoming(today, upcoming);
    then:
    def block = result.block();
    block.today.size() == 2
    block.today*.obTypeId.sort() == [1L, 2L]
    block.upcoming.size() == 0
  }

  def "test correct millis are used"() {
    when:
    request.queryParam("days") >> Optional.of("5")
    request.queryParam("tz") >> Optional.of("2")
    def result = handler.handle(request)
    then:
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1527601168000", toEpochMillis: "1527631199000"]) >> Mono.empty()
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1527631200000", toEpochMillis: "1527976799000"]) >> Mono.empty()
  }

  def "test timezone with large offset"() {
    when:
    request.queryParam("days") >> Optional.of("2")
    request.queryParam("tz") >> Optional.of("12")
    def result = handler.handle(request)
    then:
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1527601168000",
      toEpochMillis: "1527681599000"]) >> Mono.empty()
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1527681600000",
      toEpochMillis: "1527767999000"]) >> Mono.empty()
  }

  def "test timezone with large negative offset"() {
    given:
    mockLeaguesUpcomingHandlerWithFixedClock(1530514800L) // Mon, 02 Jul 2018 07:00:00 UTC
    when:
    request.queryParam("days") >> Optional.of("2")
    request.queryParam("tz") >> Optional.of("-10")
    def result = handler.handle(request)
    then:
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1530514800000",
      toEpochMillis: "1530525599000"]) >> Mono.empty()
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1530525600000",
      toEpochMillis: "1530611999000"]) >> Mono.empty()
  }

  def "if one day is passed, only today should be returned"() {
    when:
    request.queryParam("days") >> Optional.of("1")
    request.queryParam("tz") >> Optional.of("2")
    def result = handler.handle(request)
    then:
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1527601168000", toEpochMillis: "1527631199000"]) >> Mono.empty()
    0 * leaguesClientMock.execute(_, _ as Map)
  }

  def "test with negative timezone"() {
    when:
    request.queryParam("days") >> Optional.of("5")
    request.queryParam("tz") >> Optional.of("-2")
    def result = handler.handle(request)
    then:
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1527601168000", toEpochMillis: "1527645599000"]) >> Mono.empty()
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1527645600000", toEpochMillis: "1527991199000"]) >> Mono.empty()
  }

  def "test with 0 timezone"() {
    when:
    request.queryParam("days") >> Optional.of("5")
    request.queryParam("tz") >> Optional.of("0")
    def result = handler.handle(request)
    then:
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1527601168000", toEpochMillis: "1527638399000"]) >> Mono.empty()
    1 * leaguesClientMock.execute(_, [fromEpochMillis: "1527638400000", toEpochMillis: "1527983999000"]) >> Mono.empty()
  }

  def "less then one day causes exception"() {
    when:
    request.queryParam("days") >> Optional.of("0")
    request.queryParam("tz") >> Optional.of("2")
    def result = handler.handle(request)
    then:
    thrown(IllegalArgumentException)
  }
}
