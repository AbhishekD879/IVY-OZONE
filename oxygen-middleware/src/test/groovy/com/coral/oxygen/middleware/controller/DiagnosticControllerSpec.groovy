package com.coral.oxygen.middleware.controller


import com.coral.oxygen.middleware.common.service.ErrorsStorageService
import groovy.json.JsonSlurper
import org.springframework.core.env.AbstractEnvironment
import org.springframework.core.env.EnumerablePropertySource
import org.springframework.core.env.MutablePropertySources
import org.springframework.core.env.PropertySource
import org.springframework.http.HttpStatus
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.setup.MockMvcBuilders
import spock.lang.Specification

import static org.springframework.http.MediaType.APPLICATION_JSON
import static org.springframework.http.MediaType.APPLICATION_JSON_VALUE
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get

class DiagnosticControllerSpec extends Specification {

  AbstractEnvironment environment = Mock()
  ErrorsStorageService errorsStorageService = Mock()

  DiagnosticController controller = new DiagnosticController(environment, errorsStorageService)

  MockMvc mockMvc = MockMvcBuilders.standaloneSetup(controller).build()

  def "Get config as Map"() {
    given:
    PropertySource<Map<String, String>> propertySource = new EnumerablePropertySource<Map<String, String>>("testProps") {
          @Override
          String[] getPropertyNames() {
            return ["prop1", "prop2"]
          }

          @Override
          Object getProperty(String propertyName) {
            if (getSource().containsKey(propertyName)) {
              return getSource().get(propertyName)
            } else {
              return null
            }
          }

          @Override
          Map<String, String> getSource() {
            Map<String, String> sourcesMap = new HashMap<>()
            sourcesMap.put("prop1", "propValue1")
            sourcesMap.put("prop2", "propValue2")
            return sourcesMap
          }
        }
    MutablePropertySources propertySources = new MutablePropertySources()
    propertySources.addFirst(propertySource)
    environment.getPropertySources() >> propertySources

    when:
    def response = mockMvc.perform(get("/api/diagnostic")
        .contentType(APPLICATION_JSON))
        .andReturn().response
    Map<String, Object> content = new JsonSlurper().parseText(response.contentAsString) as Map<String, Object>

    then:
    response.status == HttpStatus.OK.value()
    response.contentType == APPLICATION_JSON_VALUE
    content.get("prop1") == "propValue1"
    content.get("prop2") == "propValue2"
  }

  def "Get distributed error Map"() {
    given:

    def testMap = new HashMap()
    testMap.put("key", "value")
    errorsStorageService.getErrors() >> testMap

    when:
    def response = mockMvc.perform(get("/api/diagnostic/errors")).andReturn().getResponse()
    def responseContent = response.contentAsString
    Map<String, Object> content = new JsonSlurper().parseText(responseContent) as Map<String, Object>

    then:
    response.getStatus() == HttpStatus.OK.value()
    response.contentType == APPLICATION_JSON_VALUE
    content.get("key") == "value"
  }
}
