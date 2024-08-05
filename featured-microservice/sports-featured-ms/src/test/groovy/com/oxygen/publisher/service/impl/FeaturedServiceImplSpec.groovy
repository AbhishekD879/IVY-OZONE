package com.oxygen.publisher.service.impl

import com.oxygen.publisher.model.OutputModule
import com.oxygen.publisher.relation.dto.VersionResponse
import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel
import com.oxygen.publisher.sportsfeatured.relation.FeaturedApi
import com.oxygen.publisher.sportsfeatured.service.FeaturedServiceImpl
import com.oxygen.publisher.test.util.TestCall
import spock.lang.Ignore
import spock.lang.Specification

class FeaturedServiceImplSpec extends Specification {
  static final String MODEL_VERSION = "12"
  static final String TEST_URL = "http://test.test"

  FeaturedServiceImpl featuredService

  def featuredApi = Mock(FeaturedApi)
  def featuredServiceRegistry = Mock(SportsServiceRegistry)


  def setup() {
    featuredApi.getVersion() >> new TestCall<>(TEST_URL, new VersionResponse(MODEL_VERSION))
    featuredServiceRegistry.getFeaturedApi() >> featuredApi

    featuredService = Spy()
    featuredService.setServiceRegistry(featuredServiceRegistry)
  }


  @Ignore
  def "Get Last Generation_Correct Response Received"() {
    expect:
    featuredService.getLastGeneration({ c ->
      assert c.equals(MODEL_VERSION)
    })
  }

  def "Get Modules Structure_Version Passed_Correct Response Received"() {
    FeaturedModel featuredModel = new FeaturedModel("0");
    String modelVersion = "135";
    featuredApi.getModelStructure(modelVersion) >> new TestCall<>(TEST_URL, featuredModel)

    when:
    featuredService.getFeaturedPagesStructure(modelVersion, { r ->
      assert r == featuredModel
    })

    then:
    noExceptionThrown()
  }

  def "Get Module_Version Passed_Correct Response Received"() {
    String moduleId = "UUID"
    String modelVersion = "135"
    OutputModule module = new OutputModule()
    featuredApi.getModule(moduleId, modelVersion) >> new TestCall<>(TEST_URL, module)

    when:
    featuredService.getModule(moduleId, modelVersion, { r ->
      assert r == module
    })

    then:
    noExceptionThrown()
  }

  def "Get Topics_Version Passed_Correct Response Received"() {
    String moduleId = "UUID"
    String modelVersion = "135"
    List<String> topics = Arrays.asList("topic_1", "topic_2")
    featuredApi.getTopics(moduleId, modelVersion) >> new TestCall<>(TEST_URL, topics)

    when:
    featuredService.getTopics(moduleId, modelVersion, { r ->
      assert r == topics
    })

    then:
    noExceptionThrown()
  }
}
