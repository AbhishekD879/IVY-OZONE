package com.entain.oxygen.service;

import com.egalacoral.spark.siteserver.model.Event;
import com.entain.oxygen.dto.ChildrenDto;
import com.entain.oxygen.service.siteserver.SiteServerService;
import com.entain.oxygen.util.EventTransformerUtil;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class HorseRacingDataService {

  private CacheManager cacheManager;
  private SiteServerService siteServerService;

  @Autowired
  public HorseRacingDataService(CacheManager cacheManager, SiteServerService siteServerService) {
    this.cacheManager = cacheManager;
    this.siteServerService = siteServerService;
  }

  @Value("${user-stable-cache.caches[0].cacheName}")
  private String uKIECache;

  private static final String SS_UK_IE_CACHE_KEY = "uk_ie_ss_horse";

  public List<ChildrenDto> getCachedHorseData() {
    return Optional.ofNullable(cacheManager.getCache(uKIECache))
        .map(
            (Cache cache) -> {
              log.debug("Cache name : " + uKIECache);
              return Optional.ofNullable(cache.get(SS_UK_IE_CACHE_KEY, List.class))
                  .map(childrenDto -> (List<ChildrenDto>) childrenDto)
                  .orElseGet(
                      () -> {
                        List<ChildrenDto> eventDtoList = getEventDtoList();
                        log.debug("No data is present in cache");
                        Objects.requireNonNull(cacheManager.getCache(uKIECache))
                            .put(SS_UK_IE_CACHE_KEY, eventDtoList);
                        log.debug("Size of SS call : " + getEventDtoList().size());
                        return eventDtoList;
                      });
            })
        .orElseGet(
            () -> {
              log.debug(uKIECache + " cache not found");
              return getEventDtoList();
            });
  }

  private List<ChildrenDto> getEventDtoList() {
    List<Event> horseEvents = siteServerService.getHorseEvents();
    return EventTransformerUtil.copyEventsToEventDtos(horseEvents);
  }
}
