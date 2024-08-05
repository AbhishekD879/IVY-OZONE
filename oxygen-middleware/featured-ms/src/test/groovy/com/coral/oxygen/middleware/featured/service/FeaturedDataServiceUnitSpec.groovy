package com.coral.oxygen.middleware.featured.service

import com.coral.oxygen.middleware.common.configuration.DistributedKey
import com.coral.oxygen.middleware.common.imdg.DistributedAtomicLong
import com.coral.oxygen.middleware.common.imdg.DistributedInstance
import com.coral.oxygen.middleware.common.service.GenerationStorageService
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import spock.lang.Shared
import spock.lang.Specification

class FeaturedDataServiceUnitSpec extends Specification {
  FeaturedDataService featuredDataService

  DistributedInstance distributedInstance
  GenerationStorageService generationStorageService

  @Shared
  Gson gson

  def setupSpec() {
    gson = new GsonBuilder().create()
  }

  def setup() {
    distributedInstance = Mock(DistributedInstance)
    generationStorageService = Mock(GenerationStorageService)

    featuredDataService = new FeaturedDataService(generationStorageService, distributedInstance, gson)
  }

  def "Topics is empty array if module map not containing such module"() {
    given:
    String id = "someId"
    String version = "someVersion"
    distributedInstance.getValue(_ as DistributedKey, _ as String) >> null

    when:
    String topicsString = featuredDataService.getTopics(id, version)

    then:
    topicsString == '[]'
  }

  def "Topics list constructed properly for moduleDataItems"() {
    given:
    String id = "someId"
    String version = "someVersion"

    List<EventsModuleData> moduleDataItems = Arrays.asList(
        createModuleDataItemWithId(1l),
        createModuleDataItemWithId(2l),
        createModuleDataItemWithId(20l)
        )
    EventsModule outputModule = new EventsModule()
    outputModule.setData(moduleDataItems)
    distributedInstance.getValue(_ as DistributedKey, _ as String) >> gson.toJson(outputModule)

    when:
    String topicsJsonString = featuredDataService.getTopics(id, version)
    List<String> topicsList = gson.fromJson(topicsJsonString, List)

    then:
    topicsList == Arrays.asList("live_server:1", "live_server:2", "live_server:20")
  }

  def "On getting structure featureModelMap value was got"() {
    given:
    String id = "someId"

    when:
    featuredDataService.getStructureById(id)

    then:
    1 * distributedInstance.getValue(DistributedKey.FEATURED_PAGE_MODEL_MAP, id)
  }

  def "On getting module by id featureModuleMap value is got based on generationMap value"() {
    DistributedAtomicLong versionAtomicLong = Mock()
    String id = "someId"
    long version = 1
    String featureModuleMapKey = null
    distributedInstance.getAtomicLong(DistributedKey.ATOMIC_FEATURED_DATA) >> versionAtomicLong
    versionAtomicLong.get() >> version

    when:
    featuredDataService.getModuleById(id)

    then:
    1*distributedInstance.getValue(DistributedKey.FEATURED_MODULE_MAP, id+"::"+version) >> { arguments ->
      featureModuleMapKey = arguments[1]
    }
    featureModuleMapKey.contains(id)
    featureModuleMapKey.contains(String.valueOf(version))
  }

  private static EventsModuleData createModuleDataItemWithId(Long id) {
    EventsModuleData moduleDataItem = new EventsModuleData()
    moduleDataItem.setId(id)

    return moduleDataItem
  }
}
