package com.ladbrokescoral.cashout.service

import com.ladbrokescoral.cashout.model.safbaf.Entity
import com.ladbrokescoral.cashout.model.safbaf.Event
import com.ladbrokescoral.cashout.model.safbaf.Market
import com.ladbrokescoral.cashout.model.safbaf.Selection
import com.ladbrokescoral.cashout.model.safbaf.betslip.Betslip
import org.apache.commons.io.IOUtils
import spock.lang.Specification

import java.nio.charset.Charset

class TopicContentConverterTest extends Specification {
  TopicContentConverter converter = new TopicContentConverter()
  String path = "com/ladbrokescoral/cashout/service/"

  def "convert msg to event"() {
    given:
    String fileContent = IOUtils.toString(this.getClass().classLoader.getResource(path + "event.json"), Charset.forName("UTF-8"))
    when:
    Optional<Entity> entity = converter.convertSafUpdateToPojo(fileContent)
    then:
    entity.isPresent()
    entity.get() instanceof Event
  }

  def "convert msg to market"() {
    given:
    String fileContent = IOUtils.toString(this.getClass().classLoader.getResource(path + "market.json"), Charset.forName("UTF-8"))
    when:
    Optional<Entity> entity = converter.convertSafUpdateToPojo(fileContent)
    then:
    entity.isPresent()
    entity.get() instanceof Market
  }

  def "convert msg to selection"() {
    given:
    String fileContent = IOUtils.toString(this.getClass().classLoader.getResource(path + "selection.json"), Charset.forName("UTF-8"))
    when:
    Optional<Entity> entity = converter.convertSafUpdateToPojo(fileContent)
    then:
    entity.isPresent()
    entity.get() instanceof Selection
  }

  def "convert msg to selection2"() {
    given:
    String fileContent = IOUtils.toString(this.getClass().classLoader.getResource(path + "selection2.json"), Charset.forName("UTF-8"))
    when:
    Optional<Entity> entity = converter.convertSafUpdateToPojo(fileContent)
    then:
    entity.isPresent()
    entity.get() instanceof Selection
  }

  def "convert betslip message"() {
    given:
    String fileContent = IOUtils.toString(this.getClass().classLoader.getResource(path + "betslip.json"), Charset.forName("UTF-8"))
    when:
    Optional<Entity> entity = converter.convertBetslipUpdateToPojo(fileContent)
    then:
    entity.isPresent()
    entity.get() instanceof Betslip
  }
}
