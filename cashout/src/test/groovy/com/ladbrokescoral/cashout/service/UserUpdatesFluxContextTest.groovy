package com.ladbrokescoral.cashout.service

import com.ladbrokescoral.cashout.model.response.UpdateDto
import reactor.core.publisher.FluxSink
import spock.lang.Specification

class UserUpdatesFluxContextTest extends Specification {
  private UserFluxBetUpdatesContext ctx
  private UpdateDto betUpdate = Mock(UpdateDto)
  private FluxSink sink = Mock(FluxSink)

  void setup() {
    ctx = new UserFluxBetUpdatesContext()
  }

  def "Sink can be registered"() {
    when:
    ctx.register("123", sink)
    ctx.sendBetUpdate("123", this.betUpdate)
    then:
    1 * sink.next(betUpdate)
  }

  def "Updates are sent to multiple sinks"() {
    given:
    def sink2 = Mock(FluxSink)
    when:
    ctx.register("123", sink)
    ctx.register("123", sink2)
    ctx.sendBetUpdate("123", betUpdate)
    then:
    1 * sink.next(betUpdate)
    1 * sink2.next(betUpdate)
  }

  def "No exception is thrown when sink is not registered"() {
    when:
    ctx.sendBetUpdate("123", betUpdate)
    then:
    notThrown()
  }

  def "When sink is cancelled, update is sent"() {
    given:
    sink.isCancelled() >> true
    when:
    ctx.register("123", sink)
    ctx.sendBetUpdate("123", betUpdate)
    then:
    0 * sink.next(_)
  }
}
