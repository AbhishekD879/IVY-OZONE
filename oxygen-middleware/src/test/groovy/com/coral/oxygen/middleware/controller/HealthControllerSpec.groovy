package com.coral.oxygen.middleware.controller

import com.coral.oxygen.middleware.common.imdg.DistributedInstance
import com.coral.oxygen.middleware.configuration.CmsServiceHealthIndicator
import com.coral.oxygen.middleware.component.MiddlewareHealthIndicator
import com.coral.oxygen.middleware.configuration.SiteServHealthIndicator
import org.springframework.boot.actuate.health.Health
import org.springframework.boot.actuate.health.Status
import org.springframework.http.HttpStatus
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.setup.MockMvcBuilders
import spock.lang.Specification

import static org.springframework.http.MediaType.APPLICATION_JSON_UTF8
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get

class HealthControllerSpec extends Specification {

  CmsServiceHealthIndicator cmsServiceHealthIndicator = Mock()
  SiteServHealthIndicator siteServHealthIndicator = Mock()
  MiddlewareHealthIndicator middlewareHealthIndicator = Mock()
  DistributedInstance distributedInstance = Mock()

  HealthController controller = new HealthController(cmsServiceHealthIndicator, siteServHealthIndicator, distributedInstance, middlewareHealthIndicator)

  MockMvc mockMvc = MockMvcBuilders.standaloneSetup(controller).build()

  def "Check Health Statuses"() {
    given:
    cmsServiceHealthIndicator.health() >> cmsHealth
    siteServHealthIndicator.health() >> siteServerHealth
    middlewareHealthIndicator.health() >> Health.status(Status.UP).build()
    distributedInstance.getHealthIndicator() >> healthIndicator

    expect:
    def response = mockMvc.perform(get("/health").contentType(APPLICATION_JSON_UTF8)).andReturn().getResponse()
    response.getStatus() == httpStatus

    where:
    cmsHealth                                    | siteServerHealth                             | healthIndicator                                     | httpStatus
    Health.status(Status.UNKNOWN).build()        | Health.status(Status.UNKNOWN).build()        | { health -> Health.status(Status.UNKNOWN).build() } | HttpStatus.OK.value()
    Health.status(Status.UP).build()             | Health.status(Status.UP).build()             | { health -> Health.status(Status.UP).build() }      | HttpStatus.OK.value()
    Health.status(Status.OUT_OF_SERVICE).build() | Health.status(Status.OUT_OF_SERVICE).build() | { health -> Health.status(Status.UNKNOWN).build() } | HttpStatus.OK.value()
    Health.status(Status.UNKNOWN).build()        | Health.status(Status.UNKNOWN).build()        | { health -> Health.status(Status.UNKNOWN).build() } | HttpStatus.OK.value()
    Health.status(Status.UNKNOWN).build()        | Health.status(Status.UNKNOWN).build()        | { health -> Health.status(Status.OUT_OF_SERVICE).build() } | HttpStatus.SERVICE_UNAVAILABLE.value()
  }

  def "Check Self Health Statuses"() {
    given:
    cmsServiceHealthIndicator.health() >> Health.status(Status.UP).build()
    siteServHealthIndicator.health() >> Health.status(Status.UP).build()
    middlewareHealthIndicator.health() >> middlewareHealth
    distributedInstance.getHealthIndicator() >> healthIndicator

    expect:
    def response = mockMvc.perform(get("/health").contentType(APPLICATION_JSON_UTF8)).andReturn().getResponse()
    response.getStatus() == httpStatus

    where:
    middlewareHealth                                | healthIndicator                                               | httpStatus
    Health.status(Status.UNKNOWN).build()           | { health -> Health.status(Status.UNKNOWN).build() }           | HttpStatus.OK.value()
    Health.status(Status.UP).build()                | { health -> Health.status(Status.UNKNOWN).build() }           | HttpStatus.OK.value()
    Health.status(Status.UNKNOWN).build()           | { health -> Health.status(Status.UP).build() }                | HttpStatus.OK.value()
    Health.status(Status.OUT_OF_SERVICE).build()    | { health -> Health.status(Status.UP).build() }                | HttpStatus.SERVICE_UNAVAILABLE.value()
    Health.status(Status.UP).build()                | { health -> Health.status(Status.OUT_OF_SERVICE).build() }    | HttpStatus.SERVICE_UNAVAILABLE.value()
  }
}
