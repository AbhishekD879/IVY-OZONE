package com.oxygen.publisher.service.impl

import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry
import com.oxygen.publisher.sportsfeatured.relation.FeaturedApi
import com.oxygen.publisher.sportsfeatured.service.FeaturedServiceImpl
import com.oxygen.publisher.test.util.TestCall
import spock.lang.Specification

class FeaturedServiceImplFailuresSpec extends Specification {
  FeaturedServiceImpl featuredService

  def featuredApi = Mock(FeaturedApi)
  def featuredServiceRegistry = Mock(SportsServiceRegistry)


  def setup() {
    featuredServiceRegistry.getFeaturedApi() >> featuredApi

    featuredService = Spy()
    featuredService.setServiceRegistry(featuredServiceRegistry)
  }

  def "Get Last Generation_Client Call Failed_Exception Logged"() {
    Throwable throwable = new RuntimeException()
    featuredApi.getVersion() >> new TestCall<>("http://test.test", throwable)

    when:
    featuredService.getLastGeneration{r -> }

    then:
    thrown(NullPointerException)
  }
}
