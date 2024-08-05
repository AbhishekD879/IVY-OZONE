package com.entain.oxygen.tasks;

import com.egalacoral.spark.siteserver.model.Event;
import com.entain.oxygen.configuration.CachingConfiguration;
import com.entain.oxygen.dto.ChildrenDto;
import com.entain.oxygen.service.siteserver.SiteServerService;
import com.entain.oxygen.util.EventTransformerUtil;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import java.util.List;
import java.util.Objects;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnBean;
import org.springframework.cache.CacheManager;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@ConditionalOnBean(value = {CachingConfiguration.class})
@Slf4j
public class HorseRacingDataCacheTask {

  private final SiteServerService siteServerService;
  private final CacheManager cacheManager;

  @Value("${user-stable-cache.caches[0].cacheName}")
  private String uKIECache;

  private static final String SS_UK_IE_CACHE_KEY = "uk_ie_ss_horse";
  private final MasterSlaveExecutor masterSlaveExecutor;

  @Scheduled(cron = "${upms.cron.expression}", zone = "${time.zone}")
  public void runJob() {
    try {
      masterSlaveExecutor.executeIfMaster(this::executeHorseEvents, this::slaveAction);
    } catch (Exception e) {
      log.error("Caught error in masterSlave execution", e);
    }
  }

  private void executeHorseEvents() {
    log.debug("ss object : " + siteServerService);
    long beg = System.currentTimeMillis();
    List<Event> horseEvents = siteServerService.getHorseEvents();
    List<ChildrenDto> eventDtoList = EventTransformerUtil.copyEventsToEventDtos(horseEvents);
    long end = System.currentTimeMillis();

    log.debug("SS response empty : " + horseEvents.isEmpty());
    log.debug("Time taken fo SS call : " + (end - beg) + "ms");

    // Putting SS data to cache
    Objects.requireNonNull(cacheManager.getCache(uKIECache)).put(SS_UK_IE_CACHE_KEY, eventDtoList);
  }

  public void slaveAction() {
    log.info("Slave");
  }
}
