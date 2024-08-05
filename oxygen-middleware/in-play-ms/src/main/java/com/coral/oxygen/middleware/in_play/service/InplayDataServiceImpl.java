package com.coral.oxygen.middleware.in_play.service;

import static com.coral.oxygen.middleware.common.configuration.DistributedKey.*;

import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import com.coral.oxygen.middleware.common.service.GenerationKeyType;
import com.coral.oxygen.middleware.common.service.GenerationStorageService;
import com.coral.oxygen.middleware.in_play.service.model.InPlayCache;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon;
import com.google.gson.Gson;
import com.newrelic.api.agent.NewRelic;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.Collections;
import java.util.List;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class InplayDataServiceImpl implements InplayDataService {

  private Gson gson;
  @Getter private DistributedInstance distributedInstance;
  @Getter private GenerationStorageService generationStorageService;

  @Autowired
  public InplayDataServiceImpl(
      Gson gson,
      DistributedInstance distributedInstance,
      GenerationStorageService generationStorageService) {
    this.gson = gson;
    this.distributedInstance = distributedInstance;
    this.generationStorageService = generationStorageService;
  }

  @Override
  public InPlayData getInPlayModel(String version) {
    return fromJson(
        getDistributedInstance().getValue(INPLAY_STRUCTURE_MAP, version), InPlayData.class);
  }

  @Override
  public SportsRibbon getSportsRibbon(String version) {
    return fromJson(
        getDistributedInstance().getValue(INPLAY_SPORTS_RIBBON_MAP, version), SportsRibbon.class);
  }

  @Override
  public InPlayCache getInPlayCache(String version) {
    return fromJson(
        getDistributedInstance().getValue(INPLAY_CACHED_STRUCTURE_MAP, version), InPlayCache.class);
  }

  @Override
  public String getGeneration() {
    String currentGeneration =
        generationStorageService.getLatest(GenerationKeyType.INPLAY_GENERATION);
    if (currentGeneration == null) {
      log.warn("Couldn't determine current generation");
    }
    return currentGeneration;
  }

  public SportSegment getSportSegment(String storageKey) {
    try {
      storageKey = URLDecoder.decode(storageKey, "UTF-8");
    } catch (UnsupportedEncodingException e) {
      log.error("Can't find UTF-8 encoding."); // UTF-8 is always supported
    }
    return fromJson(
        getDistributedInstance().getValue(INPLAY_SPORT_SEGMENT_MAP, storageKey),
        SportSegment.class);
  }

  @Override
  public List<VirtualSportEvents> getVirtualSportData(String storageKey) {
    try {
      storageKey = URLDecoder.decode(storageKey, "UTF-8");
      return fromJson(
          getDistributedInstance().getValue(VIRTUAL_SPORTS_STRUCTURE_MAP, storageKey), List.class);
    } catch (UnsupportedEncodingException e) {
      log.error("Can't find UTF-8 encoding."); // UTF-8 is always supported
      return Collections.emptyList();
    }
  }

  public <T> T fromJson(String json, Class<T> classOfT) {
    if (json == null) {
      return null;
    }
    try {
      return gson.fromJson(json, classOfT);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error(String.format("Error parsing %s.", classOfT.getSimpleName()), e);
      throw e;
    }
  }
}
