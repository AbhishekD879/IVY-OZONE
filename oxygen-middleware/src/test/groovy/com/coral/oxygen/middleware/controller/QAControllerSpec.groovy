package com.coral.oxygen.middleware.controller


import com.coral.oxygen.middleware.featured.service.impl.InplayDataRestService
import com.egalacoral.spark.liveserver.Message
import com.egalacoral.spark.liveserver.Subscriber
import com.egalacoral.spark.liveserver.service.LiveServerSubscriptionsQAStorage
import groovy.json.JsonSlurper
import org.springframework.http.HttpStatus
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.setup.MockMvcBuilders
import spock.lang.Specification

import static org.springframework.http.MediaType.APPLICATION_JSON_VALUE
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get

class QAControllerSpec extends Specification {

  LiveServerSubscriptionsQAStorage liveServerStorageService = Mock()
  Subscriber liveServerSubscriber = Mock()
  InplayDataRestService inplayDataRestService = Mock()

  QAController controller = new QAController(liveServerStorageService, liveServerSubscriber, inplayDataRestService)

  MockMvc mockMvc = MockMvcBuilders.standaloneSetup(controller).build()

  def "Get Liveserver Message"() {
    given:
    Message message = new Message("code12345678901234", "messageId123", '{"json": "data"}', "eventHash123", "body")
    String mapId = "mapId123"
    Map<String, Message> testMap = new HashMap<>()
    testMap.put(mapId, message)
    liveServerStorageService.getMessages() >> testMap

    when:
    def response = mockMvc.perform(get("/api/qa/liveserver/messages")).andReturn().getResponse()
    Map<String, Message> content = new JsonSlurper().parseText(response.getContentAsString()) as Map<String, Message>

    then:
    response.getStatus() == HttpStatus.OK.value()
    response.getContentType() == APPLICATION_JSON_VALUE
    content.size() == 1
    content.containsKey(mapId)
    Map<String, String> messageMapContent = content.get(mapId) as Map<String, String>

    messageMapContent.get("messageCode") == "code12345678901234"
    messageMapContent.get("evenId") == "4567890123"
    messageMapContent.get("type") == "ode123"
    messageMapContent.get("lastMessageID") == "messageId123"
    messageMapContent.get("jsonData") == '{"json": "data"}'
    messageMapContent.get("eventHash") == "eventHash123"
    messageMapContent.get("body") == "body"
  }
}
