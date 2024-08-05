package com.coral.oxygen.middleware.featured.service;

import static com.coral.oxygen.middleware.common.configuration.DistributedKey.*;
import static com.coral.oxygen.middleware.common.service.GenerationKeyType.FEATURED_GENERATION;
import static java.util.stream.Collectors.partitioningBy;

import com.coral.oxygen.middleware.common.imdg.DistributedAtomicLong;
import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import com.coral.oxygen.middleware.common.service.GenerationStorageService;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.VersionedPageKey;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@ConditionalOnProperty(name = "featured.scheduled.task.enabled")
public class FeaturedModelStorageService extends ModuleAdapter {

  private static final long ATOMIC_DELTA = 1;

  private DistributedInstance distributedInstance;
  private GenerationStorageService storageService;
  private ObjectMapper objectMapper;

  @Autowired
  public FeaturedModelStorageService(
      DistributedInstance distributedInstance,
      GenerationStorageService storageService,
      ObjectMapper objectMapper) {
    this.distributedInstance = distributedInstance;
    this.storageService = storageService;
    this.objectMapper = objectMapper;
  }

  public FeaturedModel save(FeaturedModel model, long version) {
    model
        .getModules()
        .forEach(
            m -> {
              // Module unique key.
              String moduleUKey = FeaturedRawIndex.ModuleKey.fromModule(m, version).toString();
              try {
                distributedInstance.updateExpirableValue(
                    FEATURED_MODULE_MAP, moduleUKey, objectMapper.writeValueAsString(m));
              } catch (JsonProcessingException e) {
                log.info(
                    "exception while saving Featured module {} / {} :: {} ",
                    moduleUKey,
                    m,
                    e.getMessage());
              }
              log.info("Featured module stored {} / {} ", moduleUKey, m);
            });

    Map<Boolean, List<AbstractFeaturedModule>> mapByExpanded =
        model.getModules().stream()
            .collect(partitioningBy(AbstractFeaturedModule::getShowExpanded));

    mapByExpanded.get(false).parallelStream()
        .forEach(
            module -> {
              log.info("Remove data from module {} featured module ", module);
              module.setData(new ArrayList<>());
            });

    // Page unique key
    VersionedPageKey pageIndex = VersionedPageKey.fromPage(model, version);
    try {
      distributedInstance.updateExpirableValue(
          FEATURED_PAGE_MODEL_MAP, pageIndex.toString(), objectMapper.writeValueAsString(model));
    } catch (JsonProcessingException e) {
      log.error("error :" + e.getMessage());
    }
    log.info("Featured model with {} ID stored", pageIndex);
    if (model.getPageId().equals("0")) log.info("featuredModel saved:::::::::::::::::" + pageIndex);
    return model;
  }

  public void saveGenerationIndex(Set<VersionedPageKey> thisIndex) {
    storageService.putLatest(FEATURED_GENERATION, ModuleAdapter.FEATURED_GSON.toJson(thisIndex));
  }

  public Optional<String> getLatestFeatureModelJson() {
    DistributedAtomicLong atomicLong = distributedInstance.getAtomicLong(ATOMIC_FEATURED_DATA);
    // what page should we get?
    return Optional.ofNullable(getFeaturedPageModel(atomicLong.get()));
  }

  public FeaturedModel getFeaturedModel(String pageId, Long version) {
    String pageKey = VersionedPageKey.fromPage(pageId, version).toString();
    FeaturedModel featuredModel = null;

    try {
      String featuredModelStr = distributedInstance.getValue(FEATURED_PAGE_MODEL_MAP, pageKey);
      if (featuredModelStr != null)
        featuredModel = objectMapper.readValue(featuredModelStr, FeaturedModel.class);
    } catch (JsonProcessingException e) {
      log.error("Exception while converting {}, {} ::", pageId, version, e);
    }
    return featuredModel;
  }

  private String getFeaturedPageModel(long version) {
    return distributedInstance.getValue(FEATURED_PAGE_MODEL_MAP, String.valueOf(version));
  }

  public Long getNextVersion() {
    DistributedAtomicLong atomicLong = distributedInstance.getAtomicLong(ATOMIC_FEATURED_DATA);
    return atomicLong.addAndGet(ATOMIC_DELTA);
  }

  private Long getThisVersion() {
    return distributedInstance.getAtomicLong(ATOMIC_FEATURED_DATA).get();
  }

  public List<AbstractFeaturedModule> getModulesById(Long key, List<String> ids) {
    List<String> compositeKeys =
        ids.stream()
            .map(item -> FeaturedRawIndex.ModuleKey.fromModule(item, key).toString())
            .collect(Collectors.toCollection(ArrayList::new));

    return distributedInstance.getValues(FEATURED_MODULE_MAP, compositeKeys).stream()
        .filter(Objects::nonNull)
        .map(
            (String value) -> {
              try {
                return objectMapper.readValue(value, AbstractFeaturedModule.class);
              } catch (JsonProcessingException e) {
                log.error("error  ::" + e.getMessage());
              }
              return null;
            })
        .collect(Collectors.toCollection(ArrayList::new));
  }

  public String getLastModulesById(List<String> ids) {
    return ModuleAdapter.FEATURED_GSON.toJson(getModulesById(getThisVersion(), ids));
  }

  public Long getPreviousVersion(Long version) {
    return version - ATOMIC_DELTA;
  }

  public List<String> getAndSaveFeaturedSports(List<String> sports) {
    String delimiter = ",";
    return Optional.ofNullable(
            distributedInstance.updateExpirableValue(
                FEATURED_SPORT_PAGES, String.join(delimiter, sports)))
        .map(s -> Arrays.asList(s.split(delimiter)))
        .orElse(Collections.emptyList());
  }

  public Long getLastRunTime() {
    String lastRunStr = distributedInstance.getValue(LAST_RUN_TIME);
    log.info(
        "last excecution time stored:: {}",
        Objects.isNull(lastRunStr) ? null : Instant.ofEpochMilli(Long.valueOf(lastRunStr)));
    return Objects.isNull(lastRunStr) ? null : Long.valueOf(lastRunStr);
  }

  public void saveLastRunTime(long lastRunTime) {
    distributedInstance.updateExpirableValue(LAST_RUN_TIME, String.valueOf(lastRunTime));
  }
}
