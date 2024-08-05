package com.coral.oxygen.middleware.common.cache

import com.coral.oxygen.middleware.common.configuration.cfcache.CloudFlareClient
import com.coral.oxygen.middleware.common.configuration.cfcache.InvalidateCacheResult
import com.fasterxml.jackson.databind.ObjectMapper
import okhttp3.*
import okhttp3.internal.Util
import spock.lang.Specification

class CloudFlareClientSpec extends Specification {

  private CloudFlareClient cloudFlareClient
  private OkHttpClient httpClient
  private Call httpCall

  void setup() {
    def config = new com.coral.oxygen.middleware.common.configuration.cfcache.CloudFlareConfig()
    config.setEndpoint("http://test")
    config.setToken("token123")
    httpClient = Mock(OkHttpClient)
    httpCall = Mock(Call)
    httpClient.newCall(_ as Request) >> httpCall

    cloudFlareClient = new CloudFlareClient(config, httpClient, new ObjectMapper())
  }

  def "Invalidate successful"() {
    given:
    httpCall.execute() >> new Response.Builder()
        .protocol(Protocol.HTTP_1_1)
        .code(200)
        .message("OK")
        .body(ResponseBody.create(null, Util.EMPTY_BYTE_ARRAY))
        .request(new Request.Builder().url("http://any").get().build())
        .build()

    when:
    def result = cloudFlareClient.invalidate("zoneid12", Collections.singleton("somePath"))

    then:
    result.isPresent()
    InvalidateCacheResult invalidateResult = result.get()
    invalidateResult.getResponseCode() == 200
    invalidateResult.getInvalidatedItems().size() == 1
    invalidateResult.getServiceType() == CloudFlareClient.SERVICE_NAME
  }

  def "cache Tags Invalidate successful"() {
    given:
    httpCall.execute() >> new Response.Builder()
        .protocol(Protocol.HTTP_1_1)
        .code(200)
        .message("OK")
        .body(ResponseBody.create(null, Util.EMPTY_BYTE_ARRAY))
        .request(new Request.Builder().url("http://any").get().build())
        .build()

    when:
    def result = cloudFlareClient.invalidateCacheTags("zoneid12", Collections.singleton("CSP-tst1-coral"))

    then:
    result.isPresent()
    InvalidateCacheResult invalidateResult = result.get()
    invalidateResult.getResponseCode() == 200
    invalidateResult.getInvalidatedItems().size() == 1
    invalidateResult.getServiceType() == CloudFlareClient.SERVICE_NAME_CACHE_TAG
  }

  def "cache Tags Invalidate Failed"() {
    given:
    httpCall.execute() >> { args -> throw new IOException() }

    when:
    def result = cloudFlareClient.invalidateCacheTags("zoneid12", Collections.singleton("CSP-tst1-coral"))

    then:
    result.isPresent()
    InvalidateCacheResult invalidateResult = result.get()
    invalidateResult.getResponseCode() == 500
    invalidateResult.getInvalidatedItems().size() == 1
  }

  def "Invalidate failed"() {
    given:
    httpCall.execute() >> { args -> throw new IOException() }

    when:
    def result = cloudFlareClient.invalidate("zoneid12", Collections.singleton("somePath"))

    then:
    result.isPresent()
    InvalidateCacheResult invalidateResult = result.get()
    invalidateResult.getResponseCode() == 500
    invalidateResult.getInvalidatedItems().size() == 1
  }
}
