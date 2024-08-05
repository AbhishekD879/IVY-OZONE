package com.coral.oxygen.middleware.featured.controller

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get

import com.coral.oxygen.middleware.featured.service.FeaturedDataService
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.setup.MockMvcBuilders
import spock.lang.Specification

class FeaturedDataControllerSpec extends Specification {

  FeaturedDataService service = Mock()

  FeaturedDataController controller = new FeaturedDataController(service)

  MockMvc mockMvc = MockMvcBuilders.standaloneSetup(controller).build()

  def "Featured endpoints"() {
    given:
    service.getStructureById(_) >> 'structure'
    service.getVersion() >> 'version'
    service.getModuleById(_) >> 'moduleById'
    service.getModuleByIdAndVersion(_, _) >> 'moduleByIdAndVersion'
    service.getTopics(_, _) >> 'topics'

    expect:
    def response = mockMvc.perform(getMethod).andReturn().getResponse()
    result == response.getContentAsString()

    where:
    getMethod                                            | result
    get('/api/featured/structure/{id}', '1')             | 'structure'
    get('/api/featured/generation')                      | 'version'
    get('/api/featured/module/{id}', '1')                | 'moduleById'
    get('/api/featured/module/{id}/version', '1')        | 'moduleByIdAndVersion'
    get('/api/featured/topics/{id}/{version}', '1', '1') | 'topics'
  }
}
