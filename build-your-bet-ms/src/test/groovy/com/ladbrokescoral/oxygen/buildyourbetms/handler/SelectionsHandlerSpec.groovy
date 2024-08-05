package com.ladbrokescoral.oxygen.buildyourbetms.handler

import com.ladbrokescoral.oxygen.buildyourbetms.handler.impl.SelectionsHandler
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.SelectionsResponse
import org.springframework.web.reactive.function.server.ServerRequest
import reactor.core.publisher.Mono
import spock.lang.Specification

class SelectionsHandlerTest extends Specification {

  BanachClient<Mono<SelectionsResponse>> webClient = Mock()

  def handler = new SelectionsHandler(webClient)
  def request = Mock(ServerRequest)

  def setup() {

    def headers = Mock(ServerRequest.Headers)
    headers.header("X-Correlation-Id") >> Mock(List)

    request.headers() >> headers
  }

  def "When request contains malformed obEventId id - NumberFormatException is thrown" () {
    given:
    request.queryParam("obEventId") >> Optional.ofNullable("string")
    when:
    handler.handle(request)
    then:
    thrown(NumberFormatException)
  }

  def "When request doesnt contain obEventId id - IllegalStateException is thrown" () {
    given:
    request.queryParam("obEventId") >> Optional.empty()
    when:
    handler.handle(request)
    then:
    thrown(IllegalStateException)
  }

  def "When request contains malformed comma separated marketIds - NumberFormatException is thrown" () {
    given:
    request.queryParam("obEventId") >> Optional.ofNullable("12313")
    request.queryParam("marketIds") >> Optional.ofNullable("1,2,string")
    when:
    handler.handle(request)
    then:
    thrown(NumberFormatException)
  }

  def "When request doesn't contain marketIds - IllegalStateException is thrown" () {
    given:
    request.queryParam("obEventId") >> Optional.ofNullable("12313")
    request.queryParam("marketIds") >> Optional.empty()
    when:
    handler.handle(request)
    then:
    thrown(IllegalStateException)
  }
}
