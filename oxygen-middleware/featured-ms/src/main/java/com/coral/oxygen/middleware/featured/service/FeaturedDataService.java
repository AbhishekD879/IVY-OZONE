package com.coral.oxygen.middleware.featured.service;

import static com.coral.oxygen.middleware.common.configuration.DistributedKey.*;

import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import com.coral.oxygen.middleware.common.service.GenerationKeyType;
import com.coral.oxygen.middleware.common.service.GenerationStorageService;
import com.coral.oxygen.middleware.featured.dto.FeaturedVersionResponse;
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.VersionedPageKey;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.text.MessageFormat;
import java.util.*;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

@Service
@ConditionalOnProperty(name = "featured.scheduled.task.enabled")
public class FeaturedDataService {

  private static final String MODULE_KEY_PATTERN = "{0}::{1}"; // cmsModuleId::generation

  private GenerationStorageService generationStorageService;
  private DistributedInstance distributedInstance;
  private Gson gson;

  @Autowired
  public FeaturedDataService(
      GenerationStorageService generationStorageService,
      DistributedInstance distributedInstance,
      Gson gson) {
    this.generationStorageService = generationStorageService;
    this.distributedInstance = distributedInstance;
    this.gson = gson;
  }

  public String getStructureById(String id) {
    return distributedInstance.getValue(FEATURED_PAGE_MODEL_MAP, id);
  }

  public String getVersion() {
    String latestVersion =
        generationStorageService.getLatest(GenerationKeyType.FEATURED_GENERATION);
    final FeaturedVersionResponse response =
        new FeaturedVersionResponse(
            gson.fromJson(latestVersion, new TypeToken<Set<VersionedPageKey>>() {}.getType()));
    return success(response);
  }

  public String getModuleById(String id) {
    long lastVersion = distributedInstance.getAtomicLong(ATOMIC_FEATURED_DATA).get();
    return getModuleByIdAndVersion(id, String.valueOf(lastVersion));
  }

  public String getModuleByIdAndVersion(String id, String version) {
    final String key = MessageFormat.format(MODULE_KEY_PATTERN, id, version);
    return distributedInstance.getValue(FEATURED_MODULE_MAP, key);
  }

  public String getTopics(String id, String version) {

    EventsModule model = gson.fromJson(getModuleByIdAndVersion(id, version), EventsModule.class);
    // handles the case when someone tries to get information on a non existing module.
    if (model == null || model.getData() == null) {
      return "[]";
    }

    List<String> channels =
        model.getData().stream()
            .filter(Objects::nonNull)
            .map(
                s ->
                    MessageFormat.format(
                        "live_server:{0,number,#}", Integer.valueOf(s.idForChangeDetection())))
            .collect(Collectors.toCollection(ArrayList::new));

    return success(channels);
  }

  public String getSportPages() {
    return success(
        Optional.ofNullable(distributedInstance.getValue(FEATURED_SPORT_PAGES))
            .map(s -> s.split(","))
            .orElse(new String[0]));
  }

  private String success(Object o) {
    return gson.toJson(o);
  }
}
