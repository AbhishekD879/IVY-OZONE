package com.coral.oxygen.middleware.featured.service;

import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.SPORTS_FEATURED_PAGE_ADDED;
import static java.text.MessageFormat.format;
import static java.util.stream.Collectors.toList;

import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkService;
import com.coral.oxygen.middleware.common.service.ChangeDetector;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.common.service.featured.FeaturedModelChangeDetector;
import com.coral.oxygen.middleware.common.service.featured.FeaturedModuleChangeDetector;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.common.service.notification.topic.TopicType;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.VersionedPageKey;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@ConditionalOnProperty(name = "featured.scheduled.task.enabled")
public class FeaturedDataProcessor extends ModuleAdapter {
  private FeaturedModelStorageService storageService;
  private FeaturedModuleChangeDetector featuredModuleChangeDetector;
  private FeaturedModelChangeDetector sportsPageChangeDetector;
  private MessagePublisher messagePublisher;
  private FeaturedLiveServerSubscriber featuredLiveServerSubscriber;
  private Set<VersionedPageKey> lastIndex;

  private DeliveryNetworkService context;
  protected static final String PATH_TEMPLATE = "api/{0}/fsc";

  @Value("${cms.brand}")
  String brand;

  @Autowired
  public FeaturedDataProcessor(
      FeaturedModelStorageService storageService,
      FeaturedModuleChangeDetector featuredModuleChangeDetector,
      FeaturedModelChangeDetector sportsPageChangeDetector,
      MessagePublisher messagePublisher,
      FeaturedLiveServerSubscriber featuredLiveServerSubscriber,
      DeliveryNetworkService context) {
    this.storageService = storageService;
    this.featuredModuleChangeDetector = featuredModuleChangeDetector;
    this.sportsPageChangeDetector = sportsPageChangeDetector;
    this.messagePublisher = messagePublisher;
    this.featuredLiveServerSubscriber = featuredLiveServerSubscriber;
    this.lastIndex = null;
    this.context = context;
  }

  public void process(FeaturedModelsData data) {
    saveModelsAndCompare(data.getFeaturedModels());
    saveSportsAndCompare(data.getSportPages());
  }

  private void saveSportsAndCompare(List<String> sports) {
    List<String> prevSports = storageService.getAndSaveFeaturedSports(sports);
    sports.stream()
        .filter(p -> !prevSports.contains(p))
        .forEach(
            sport ->
                messagePublisher.publish(
                    SPORTS_FEATURED_PAGE_ADDED, VersionedPageKey.fromPage(sport).toString()));
  }

  private void saveModelsAndCompare(List<FeaturedModel> pages) {
    if (pages.isEmpty()) {
      log.warn("No pages to process! Check CMS configuration.");
    } else {
      final Long nextVersion = storageService.getNextVersion();
      log.info("Next version :: {}", nextVersion);
      Set<VersionedPageKey> thisIndex = processPages(pages, nextVersion);
      this.comparePageIndexes(nextVersion, thisIndex, pages.get(0).isUseFSCCached());
    }
  }

  private Set<VersionedPageKey> processPages(List<FeaturedModel> pages, Long nextVersion) {
    Set<VersionedPageKey> thisIndex = new HashSet<>();
    pages.forEach(page -> thisIndex.add(processPage(page, nextVersion)));
    storageService.saveGenerationIndex(thisIndex);
    return thisIndex;
  }

  void comparePageIndexes(Long nextVersion, Set<VersionedPageKey> thisIndex, boolean useFSCCached) {
    if (lastIndex == null) {
      this.lastIndex = thisIndex;
      return;
    }
    for (VersionedPageKey last : lastIndex) {
      if (thisIndex.stream()
          .noneMatch(
              index ->
                  last.getPageId().equals(index.getPageId())
                      && last.getType().equals(index.getType()))) {
        messagePublisher.publish(
            TopicType.SPORTS_FEATURED_PAGE_DELETED,
            new VersionedPageKey(last.getType(), last.getPageId(), nextVersion).toString());
        publishFSCToCF(
            FeaturedModel.builder().pageId(last.getPageId()).useFSCCached(useFSCCached).build());
      }
    }
    this.lastIndex = thisIndex;
  }

  protected VersionedPageKey processPage(FeaturedModel page, Long thisVersion) {
    Instant start = Instant.now();
    Long previousVersion = storageService.getPreviousVersion(thisVersion);
    VersionedPageKey thisPageKey = VersionedPageKey.fromPage(page, thisVersion);

    featuredLiveServerSubscriber.subscribe(super.toLiveserveEventsData(page.getModules()));

    FeaturedModel previousModelValue =
        storageService.getFeaturedModel(page.getPageId(), previousVersion);
    log.info(
        " previousModelValue for version={} is Null {}",
        previousVersion,
        previousModelValue == null);

    // Serialization to storage
    FeaturedModel actualModel = storageService.save(page, thisVersion);
    log.info(" isFeatureStructureChanged {}", actualModel.isFeatureStructureChanged());
    // Notifications
    if (actualModel.isFeatureStructureChanged()
        || isModelChangeDetected(actualModel, previousModelValue)
        || isUseFscCacheChanged(actualModel, previousModelValue)) {
      messagePublisher.publish(TopicType.FEATURED_STRUCTURE_CHANGED, thisPageKey.toString());
      log.info(
          " FEATURED_STRUCTURE_CHANGED Featured publish notification for version={}", thisPageKey);
      publishFSCToCF(actualModel);
      if (actualModel.isSegmented()) {
        Instant end = Instant.now();
        log.info("time: elapsed time taken {} segmented", Duration.between(end, start).toMillis());
        return VersionedPageKey.fromPage(page, thisVersion);
      }
    }
    Map<Long, EventsModuleData> actualEventsModuleData =
        actualModel.getEventsModuleData() != null
            ? actualModel.getEventsModuleData()
            : new HashMap<>();
    Map<Long, EventsModuleData> previousEventsModuleData =
        previousModelValue != null ? previousModelValue.getEventsModuleData() : new HashMap<>();
    Set<String> moduleIds =
        actualEventsModuleData.entrySet().stream()
            .filter(
                entry ->
                    ChangeDetector.changeDetected(
                        entry.getValue(), previousEventsModuleData.get(entry.getKey())))
            .map(entry -> entry.getValue().getModuleIds())
            .flatMap(Collection::stream)
            .collect(Collectors.toSet());

    List<AbstractFeaturedModule> actualModules =
        storageService.getModulesById(
            thisVersion,
            actualModel.getModules().stream().map(AbstractFeaturedModule::getId).collect(toList()));
    List<AbstractFeaturedModule> previousModules =
        previousModelValue != null
            ? storageService.getModulesById(
                storageService.getPreviousVersion(thisVersion),
                previousModelValue.getModules().stream()
                    .map(AbstractFeaturedModule::getId)
                    .collect(toList()))
            : new ArrayList<>();

    actualModules.forEach(
        module -> {
          AbstractFeaturedModule prevModule =
              previousModules.stream()
                  .filter(item -> item.getId().contentEquals(module.getId()))
                  .findFirst()
                  .orElse(null);
          if (moduleIds.contains(module.getId())
              || featuredModuleChangeDetector.isChanged(module, prevModule)) {
            String thisModuleKey =
                FeaturedRawIndex.ModuleKey.fromModule(module.getId(), thisVersion).toString();
            messagePublisher.publish(TopicType.FEATURED_MODULE_CONTENT_CHANGED, thisModuleKey);
            log.info(" FEATURED_MODULE_CONTENT_CHANGED > {} for module {} ", thisModuleKey, module);
            publishFSCToCF(actualModel);
          } else if (featuredModuleChangeDetector.isChangedIncludingMinor(module, prevModule)) {
            String thisModuleKey =
                FeaturedRawIndex.ModuleKey.fromModule(module.getId(), thisVersion).toString();
            messagePublisher.publish(
                TopicType.FEATURED_MODULE_CONTENT_CHANGED_MINOR, thisModuleKey);
            log.info(
                " FEATURED_MODULE_CONTENT_CHANGED_MINOR {} for module {} ", thisModuleKey, module);
            publishFSCToCF(actualModel);
          }
        });
    Instant end = Instant.now();
    log.info(
        "time: elapsed time taken {} segmented with page id {}",
        Duration.between(end, start).toMillis(),
        page.getPageId());

    return VersionedPageKey.fromPage(page, thisVersion);
  }

  private boolean isUseFscCacheChanged(
      FeaturedModel actualModel, FeaturedModel previousModelValue) {
    return previousModelValue != null
        && !previousModelValue.isUseFSCCached()
        && actualModel.isUseFSCCached();
  }

  private boolean isModelChangeDetected(
      FeaturedModel actualModel, FeaturedModel previousModelValue) {
    return sportsPageChangeDetector.isSegmentedModulesChanged(actualModel, previousModelValue)
        || sportsPageChangeDetector.isFanzoneSegmentedModulesChanged(
            actualModel, previousModelValue)
        || sportsPageChangeDetector.isChanged(actualModel, previousModelValue);
  }

  private void publishFSCToCF(FeaturedModel actualModel) {
    if (actualModel.isUseFSCCached()) {
      AbstractFeaturedModel cfData = prepareUniversalVeiwForHomePage(actualModel);
      context.upload(brand, format(PATH_TEMPLATE, brand), actualModel.getPageId(), cfData);
    }
  }

  private AbstractFeaturedModel prepareUniversalVeiwForHomePage(FeaturedModel actualModel) {
    if (!"0".equals(actualModel.getPageId())) return new CloudFlareFeatureModel(actualModel);

    if (actualModel.getSegmentWiseModules() == null
        || actualModel.getSegmentWiseModules().get("Universal") == null) return actualModel;
    SegmentView segmentView = actualModel.getSegmentWiseModules().get("Universal");
    List<AbstractFeaturedModule<?>> nonSegmentedModules = new ArrayList<>();
    SegmentedFeaturedModelHelper.fillNonSegmentedModules(actualModel, nonSegmentedModules);
    SegmentedFeaturedModel segmentedFeaturedModel =
        SegmentedFeaturedModelHelper.createSegmentedFeaturedModel(actualModel);
    SegmentedFeaturedModelHelper.populateSegmentedFeaturedModel(
        actualModel, segmentedFeaturedModel, segmentView);
    segmentedFeaturedModel.addModules(nonSegmentedModules);
    return segmentedFeaturedModel;
  }

  public void saveLastRunTime(long lastRunTime) {
    storageService.saveLastRunTime(lastRunTime);
  }
}
