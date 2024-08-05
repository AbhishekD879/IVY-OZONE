package com.coral.oxygen.middleware.featured.service

import com.coral.oxygen.middleware.common.configuration.DistributedKey
import com.coral.oxygen.middleware.common.imdg.DistributedAtomicLong
import com.coral.oxygen.middleware.common.imdg.DistributedInstance
import com.coral.oxygen.middleware.common.imdg.DistributedMap
import com.coral.oxygen.middleware.common.service.GenerationKeyType
import com.coral.oxygen.middleware.common.service.GenerationStorageService
import com.coral.oxygen.middleware.common.service.ModuleAdapter
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel
import com.fasterxml.jackson.databind.ObjectMapper
import spock.lang.Ignore
import spock.lang.Specification

@Ignore
class FeaturedModelStorageServiceSpec extends Specification {
  FeaturedModelStorageService service
  FeaturedModel model

  GenerationStorageService storageService
  DistributedMap featureModelMap
  DistributedMap featureModuleMap
  DistributedAtomicLong generation

  def setup() {
    storageService = Mock(GenerationStorageService)
    generation = Mock(DistributedAtomicLong)
    featureModelMap = Mock(DistributedMap)
    featureModuleMap = Mock(DistributedMap)

    DistributedInstance instance = Mock(DistributedInstance)
    instance.getAtomicLong(DistributedKey.ATOMIC_FEATURED_DATA) >> generation
    instance.getMap(DistributedKey.FEATURED_PAGE_MODEL_MAP) >> featureModelMap
    instance.getMap(DistributedKey.FEATURED_MODULE_MAP) >> featureModuleMap
    service = new FeaturedModelStorageService(instance, storageService, new ObjectMapper())

    model = new FeaturedModel()
    model.setDirectiveName("testdirectove")
    ArrayList<EventsModule> modules = new ArrayList<>()
    modules.add(createModule(false))
    modules.add(createModule(true))
    modules.add(createModule(false))
    model.setPageId("0")
    model.setModules(modules)
  }


  private static EventsModule createModule(boolean showExapanded) {
    EventsModule e = new EventsModule()
    e.setShowExpanded(showExapanded)
    return e
  }

  def "Saving model is putting 0 as latest to storage"() {
    when:
    service.save(model, 1)

    then:
    1 * storageService.putLatest(GenerationKeyType.FEATURED_GENERATION, "0")
  }

  def "Latest feature model is not present if feature module map is empty"() {
    featureModelMap.entrySet() >> new LinkedHashMap<>().entrySet()

    when:
    Optional<String> optional = service.getLatestFeatureModelJson()

    then:
    !optional.isPresent()
  }

  def "Latest feature model is getting from feature module map"() {
    def map = new HashMap<>()
    map.put("0", "json0")
    map.put("1", "json1")
    featureModelMap.entrySet() >> (map.entrySet())
    generation.get() >> 1L

    when:
    Optional<String> optional = service.getLatestFeatureModelJson()

    then:
    optional.isPresent()
    optional.get() == "json1"
  }

  private populateFeatureModelMap = {
    ->
    Map<String, String> map = new HashMap<>()
    map.put("0", ModuleAdapter.FEATURED_GSON.toJson(model.getModules().get(0)))
    map.put("1", ModuleAdapter.FEATURED_GSON.toJson(model.getModules().get(1)))
    featureModelMap.entrySet() >> map.entrySet()
    featureModelMap.get("1") >> map.get("1")
  }

  private populateFeatureModuleMap = {
    ->
    Map<String, String> map = new HashMap<>()
    map.put("1::0", ModuleAdapter.FEATURED_GSON.toJson(new EventsModule()))
    map.put("1::1", ModuleAdapter.FEATURED_GSON.toJson(new EventsModule()))
    featureModuleMap.entrySet() >> map.entrySet()
    featureModuleMap.get("1::1") >> map.get("1::1")
    featureModuleMap.get("1::0") >> map.get("1::0")
  }

  def "Featured model is null if map is not yet populated"() {
    when:
    FeaturedModel optional = service.getFeaturedModelById(1L)

    then:
    optional == null
  }

  def "Featured model is not null if map already populated"() {
    populateFeatureModelMap()

    when:
    FeaturedModel optional = service.getFeaturedModelById(1L)

    then:
    optional != null
  }

  def "Featured model JSON is null if map is not yet populated"() {
    when:
    String optional = service.getFeaturedModelByIdJson(1L)

    then:
    optional == null
  }

  def "Featured model JSON is not null if map is already populated"() {
    populateFeatureModelMap()

    when:
    String optional = service.getFeaturedModelByIdJson(1L)

    then:
    optional != null
  }

  def "Module is empty optional if map is not populated"() {
    when:
    List<AbstractFeaturedModule> optional = service.getModulesById(1L, new ArrayList<>())

    then:
    optional.isEmpty()
  }

  def "Module is not empty if map is already populated"() {
    populateFeatureModuleMap()

    when:
    List<AbstractFeaturedModule> optional = service.getModulesById(1L, Arrays.asList("1"))

    then:
    !optional.isEmpty()
  }

  def "Module is empty array if map is already populated"() {
    when:
    String optional = service.getLastModulesById(Arrays.asList("1"))
    then:
    "[]" == optional
  }

  def "Module json is not empty if map is already populated"() {
    populateFeatureModuleMap()

    when:
    String optional = service.getLastModulesById(Arrays.asList("1"))
    then:
    "[" + ModuleAdapter.FEATURED_GSON.toJson(new EventsModule()).replaceAll("[\\n\\t\\s]", "") + "]" ==
        optional.replaceAll("[\\s\\n\\t]", "")
  }
}
