package com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance

import com.fasterxml.jackson.databind.ObjectMapper
import com.ladbrokescoral.oxygen.cms.configuration.ApiProperties

import org.apache.http.HttpEntity
import org.apache.http.StatusLine
import org.apache.http.client.methods.CloseableHttpResponse
import org.apache.http.client.methods.HttpUriRequest
import org.apache.http.impl.client.CloseableHttpClient

import spock.lang.Specification

class BppMaintenanceServiceSpec extends Specification {

  final String BRAND = "brand"
  final String BRAND_URL = "http://localhost"
  CloseableHttpClient httpClient
  BppMaintenanceService service

  void setup() {
    httpClient = Mock(CloseableHttpClient)
    def config = new ApiProperties.ApiConfiguration()
    config.setUrl(BRAND_URL)

    ApiProperties properties = new ApiProperties();
    properties.setBppMaintenance([(BRAND): config])
    service = new BppMaintenanceService(httpClient, properties, new ObjectMapper())
  }

  def "SendNotification"() {
    given:
    def statusLine = Mock(StatusLine)
    statusLine.getStatusCode() >> 200
    def respMock = Mock(CloseableHttpResponse)
    respMock.getStatusLine() >> statusLine
    respMock.getEntity() >> Mock(HttpEntity)

    when:
    def response = service.sendNotification(BRAND, new BppMaintenanceRequest(true, 10))

    then:
    1 * httpClient.execute(_ as HttpUriRequest) >> respMock
    response.getUrl() == BRAND_URL
    response.getCode() == 200
  }

  def "SendNotification retry on exception"() {
    given:
    def statusLine = Mock(StatusLine)
    statusLine.getStatusCode() >> 200
    def respMock = Mock(CloseableHttpResponse)
    respMock.getStatusLine() >> statusLine
    respMock.getEntity() >> Mock(HttpEntity)

    when:
    def response = service.sendNotification(BRAND, new BppMaintenanceRequest(true, 10))

    then:
    2 * httpClient.execute(_ as HttpUriRequest) >> {throw new IOException()} >> respMock
    response.getUrl() == BRAND_URL
    response.getCode() == 200
  }

  def "GetSupportedBrands"() {
    when:
    def actualBrands = service.getSupportedBrands()

    then:
    actualBrands.size() == 1
    actualBrands[0] == BRAND
  }

  def "Close"() {
    when:
    service.close()

    then:
    1 * httpClient.close()
  }
}
