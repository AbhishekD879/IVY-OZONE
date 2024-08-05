package com.coral.oxygen.middleware.featured.service

import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkService
import com.coral.oxygen.middleware.common.service.featured.FeaturedModuleChangeDetector
import com.coral.oxygen.middleware.common.service.featured.FeaturedModelChangeDetector
import com.coral.oxygen.middleware.common.service.notification.MessagePublisher
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule
import spock.lang.Specification

import java.util.stream.Collectors

import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.*

class FeaturedDateProcessorSpec extends Specification {
  FeaturedModelStorageService storageService
  FeaturedModuleChangeDetector moduleChangeDetector
  FeaturedModelChangeDetector structureChangeDetector
  MessagePublisher messagePublisher
  FeaturedLiveServerSubscriber featuredLiveServerSubscriber
  FeaturedDataProcessor dataProcessor
  DeliveryNetworkService context;

  def setup() {
    storageService = Mock(FeaturedModelStorageService)
    moduleChangeDetector = Mock(FeaturedModuleChangeDetector)
    structureChangeDetector = Mock(FeaturedModelChangeDetector)
    messagePublisher = Mock(MessagePublisher)
    context=Mock(DeliveryNetworkService)
    featuredLiveServerSubscriber = Mock(FeaturedLiveServerSubscriber)
    dataProcessor = new FeaturedDataProcessor(storageService, moduleChangeDetector,
        structureChangeDetector, messagePublisher, featuredLiveServerSubscriber,context)
  }

  private static FeaturedModel prepareModel() {
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)

    EventsModule sampleModule = new EventsModule()
    sampleModule.setId("_id")
    sampleModule.setCashoutAvail(true)
    sampleModule.setData(Arrays.asList(event))

    FeaturedModel page = new FeaturedModel()
    page.setModules(Arrays.asList(sampleModule))
    page.setPageId("0")
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, page)

    return page
  }

  def "Processing model for the first time - method calls verifying, content changed"() {
    FeaturedModel model = prepareModel()
    model.setUseFSCCached(true);
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, model)
    storageService.save(_ as FeaturedModel, _ as long) >> model
    def modulesIds = model.getModules()
        .stream()
        .map({ elem -> elem.getId() })
        .collect(Collectors.toList())

    when:
    dataProcessor.processPage(model,  1L)

    then:
    1 * storageService.save(model, 1L) >> model
    1 * structureChangeDetector.isChanged(storageResult.get(1L), null) >> true
    1 * moduleChangeDetector.isChanged(model.getModules().stream().findFirst().get(), null) >> true
    1 * messagePublisher.publish(FEATURED_STRUCTURE_CHANGED, "sport::0::1")
    1 * storageService.getModulesById(1L, modulesIds) >> model.getModules()
    1 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED, "_id::1")
    0 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED_MINOR, _)
  }

  def "Processing model for the first time - minor content changed"() {
    FeaturedModel model = prepareModel()
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, model)
    def moduleIds = model.getModules()
        .stream()
        .map({ elem -> elem.getId() })
        .collect(Collectors.toList())


    storageService.getModulesById(1L, moduleIds) >> model.getModules()
    moduleChangeDetector.isChanged(model.getModules().stream().findFirst().get(), null) >> false
    moduleChangeDetector.isChangedIncludingMinor(model.getModules().stream().findFirst().get(), null) >> true
    storageService.save(model, 1L) >> model

    when:
    dataProcessor.processPage(model,  1L)

    then:
    0 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED, "_id::1")
    1 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED_MINOR, "_id::1")
  }

  def "On model processing saving model is occuring. On exception all other skipped"() {
    FeaturedModel model = new FeaturedModel()
    model.setPageId("0")

    storageService.save(model, 1L) >> model

    when:
    try {
      dataProcessor.processPage(model,  1L)
    } catch (Exception e){
      // exception caught
    }

    then:
    1 * storageService.save(_, 1L)
    1 * featuredLiveServerSubscriber.subscribe([])
    0 * storageService.getModulesById(_, _)
  }

  def "Process model - modules are same"() {
    FeaturedModel model = new FeaturedModel()
    model.setPageId("0")
    EventsModule sampleModule = new EventsModule()
    sampleModule.setId("_id")
    sampleModule.setCashoutAvail(true)
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)
    sampleModule.setData(Arrays.asList(event))
    model.setModules(Arrays.asList(sampleModule))

    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, model)
    def moduleIds = model.getModules().stream()
        .map({ elem -> elem.getId() })
        .collect(Collectors.toList())
    storageService.save(_ as FeaturedModel, 1L) >> model
    storageService.getPreviousVersion(_ as Long) >>
    {arg -> return Optional.ofNullable(arg[0]).map({v -> v-1}).orElse(null)}

    when:
    dataProcessor.processPage(model,  1L)

    then:
    1*featuredLiveServerSubscriber.subscribe(_)
    1*storageService.save(_, 1L) >> model
    1*storageService.getFeaturedModel("0", 0) >> storageResult.get(1L)
    1*structureChangeDetector.isChanged(storageResult.get(1L), storageResult.get(1L)) >> false
    1*moduleChangeDetector.isChangedIncludingMinor(storageResult.get(1L).getModules().get(0),
        storageResult.get(1L).getModules().get(0)) >> false
    0*messagePublisher.publish(FEATURED_STRUCTURE_CHANGED, "1L")

    1*storageService.getModulesById(1L, moduleIds) >> model.getModules()
    1*storageService.getModulesById(0L, Arrays.asList(sampleModule.getId())) >> model.getModules()
    0*messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED, "_id::1")
    0*messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED_MINOR, "_id::1")
  }


  def "Processing model for the first time - method calls verifying, content changed and segmentchanged"() {
    FeaturedModel model = prepareModelIsSegmentChange()
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, model)
    storageService.save(_ as FeaturedModel, _ as long) >> model
    storageService.getFeaturedModel("0", 1l) >> model
    storageService.getPreviousVersion(1l) >> 1l
    def modulesIds = model.getModules()
        .stream()
        .map({ elem -> elem.getId() })
        .collect(Collectors.toList())

    when:
    dataProcessor.processPage(model,  1L)

    then:
    1 * storageService.save(model, 1L) >> model
    0 * structureChangeDetector.isChanged(storageResult.get(1L), null) >> true
    1 * structureChangeDetector.isSegmentedModulesChanged(storageResult.get(1L), storageResult.get(1L)) >> false
    1 * moduleChangeDetector.isChanged(model.getModules().stream().findFirst().get(), model.getModules().stream().findFirst().get()) >> true
    0 * messagePublisher.publish(FEATURED_STRUCTURE_CHANGED, "sport::0::1")
    2 * storageService.getModulesById(1L, modulesIds) >> model.getModules()
    1 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED, "_id::1")
    0 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED_MINOR, _)
  }

  def "Processing model for the first time - method calls verifying,eventsModuledata nonnull"() {
    FeaturedModel model = prepareModelIsSegmentChange()
    Map<Long, EventsModuleData> actualEventsModuleData = new HashMap<>()
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)
    actualEventsModuleData.put(event.getId(), event)
    model.setEventsModuleData(actualEventsModuleData)
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, model)
    storageService.save(_ as FeaturedModel, _ as long) >> model
    storageService.getFeaturedModel("0", 1l) >> model
    storageService.getPreviousVersion(1l) >> 1l
    def modulesIds = model.getModules()
        .stream()
        .map({ elem -> elem.getId() })
        .collect(Collectors.toList())

    when:
    dataProcessor.processPage(model,  1L)

    then:
    1 * storageService.save(model, 1L) >> model
    0 * structureChangeDetector.isChanged(storageResult.get(1L), null) >> true
    1 * structureChangeDetector.isSegmentedModulesChanged(storageResult.get(1L), storageResult.get(1L)) >> false
    1 * moduleChangeDetector.isChanged(model.getModules().stream().findFirst().get(), model.getModules().stream().findFirst().get()) >> true
    0 * messagePublisher.publish(FEATURED_STRUCTURE_CHANGED, "sport::0::1")
    2 * storageService.getModulesById(1L, modulesIds) >> model.getModules()
    1 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED, "_id::1")
    0 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED_MINOR, _)
  }

  def "Processing model for the first time - method calls verifying,eventsModuledata nonnull changed"() {
    FeaturedModel model = prepareModelIsSegmentChange()
    Map<Long, EventsModuleData> actualEventsModuleData = new HashMap<>()
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)
    event.addModuleId("_id")
    actualEventsModuleData.put(event.getId(), event)
    model.setEventsModuleData(actualEventsModuleData)

    FeaturedModel prevModel = prepareModelIsSegmentChange()
    Map<Long, EventsModuleData> prevEventsModuleData = new HashMap<>()
    EventsModuleData event2 = new EventsModuleData()
    event2.setName("changedevent")
    event2.setId(2L)
    prevEventsModuleData.put(event2.getId(), event2)
    prevModel.setEventsModuleData(prevEventsModuleData)
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, model)
    storageService.save(_ as FeaturedModel, _ as long) >> model
    storageService.getFeaturedModel("0", 1l) >> prevModel
    storageService.getPreviousVersion(1l) >> 1l
    def modulesIds = model.getModules()
        .stream()
        .map({ elem -> elem.getId() })
        .collect(Collectors.toList())

    when:
    dataProcessor.processPage(model,  1L)

    then:
    1 * storageService.save(model, 1L) >> model
    0 * messagePublisher.publish(FEATURED_STRUCTURE_CHANGED, "sport::0::1")
    2 * storageService.getModulesById(1L, modulesIds) >> model.getModules()
    1 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED, "_id::1")
    0 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED_MINOR, _)
  }
  def "Processing model for the first time - method calls verifying,eventsModuledata null"() {
    FeaturedModel model = prepareModelIsSegmentChange()
    model.setEventsModuleData(null)
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, model)
    storageService.save(_ as FeaturedModel, _ as long) >> model
    storageService.getFeaturedModel("0", 1l) >> model
    storageService.getPreviousVersion(1l) >> 1l
    def modulesIds = model.getModules()
        .stream()
        .map({ elem -> elem.getId() })
        .collect(Collectors.toList())

    when:
    dataProcessor.processPage(model,  1L)

    then:
    1 * storageService.save(model, 1L) >> model
    0 * structureChangeDetector.isChanged(storageResult.get(1L), null) >> true
    1 * structureChangeDetector.isSegmentedModulesChanged(storageResult.get(1L), storageResult.get(1L)) >> false
    1 * moduleChangeDetector.isChanged(model.getModules().stream().findFirst().get(), model.getModules().stream().findFirst().get()) >> true
    0 * messagePublisher.publish(FEATURED_STRUCTURE_CHANGED, "sport::0::1")
    2 * storageService.getModulesById(1L, modulesIds) >> model.getModules()
    1 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED, "_id::1")
    0 * messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED_MINOR, _)
  }

  def "Process model - modules are same segmented"() {
    FeaturedModel model = new FeaturedModel()
    model.setPageId("0")
    EventsModule sampleModule = new EventsModule()
    sampleModule.setId("_id")
    sampleModule.setCashoutAvail(true)
    sampleModule.setSegmented(true)
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)
    sampleModule.setData(Arrays.asList(event))
    model.setModules(Arrays.asList(sampleModule))

    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, model)
    def moduleIds = model.getModules().stream()
        .map({ elem -> elem.getId() })
        .collect(Collectors.toList())
    storageService.save(_ as FeaturedModel, 1L) >> model
    storageService.getPreviousVersion(_ as Long) >>
    {arg -> return Optional.ofNullable(arg[0]).map({v -> v-1}).orElse(null)}

    when:
    dataProcessor.processPage(model,  1L)

    then:
    1*featuredLiveServerSubscriber.subscribe(_)
    1*storageService.save(_, 1L) >> model
    1*storageService.getFeaturedModel("0", 0) >> storageResult.get(1L)
    0*messagePublisher.publish(FEATURED_STRUCTURE_CHANGED, "1L")

    1*storageService.getModulesById(1L, moduleIds) >> model.getModules()
    1*storageService.getModulesById(0L, Arrays.asList(sampleModule.getId())) >> model.getModules()
    0*messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED, "_id::1")
    0*messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED_MINOR, "_id::1")
  }


  private static FeaturedModel prepareModelIsSegmentChange() {
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)

    EventsModule sampleModule = new EventsModule()
    sampleModule.setId("_id")
    sampleModule.setCashoutAvail(true)
    sampleModule.setData(Arrays.asList(event))
    FeaturedModel page = new FeaturedModel()
    page.setModules(Arrays.asList(sampleModule))
    page.setPageId("0")
    page.setFeatureStructureChanged(false)
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, page)

    return page
  }
}
