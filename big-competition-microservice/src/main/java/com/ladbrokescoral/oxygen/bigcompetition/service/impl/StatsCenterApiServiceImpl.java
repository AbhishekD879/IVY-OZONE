package com.ladbrokescoral.oxygen.bigcompetition.service.impl;

import com.ladbrokescoral.oxygen.betradar.client.entity.Match;
import com.ladbrokescoral.oxygen.betradar.client.entity.ResultsTable;
import com.ladbrokescoral.oxygen.betradar.client.entity.SeasonMatches;
import com.ladbrokescoral.oxygen.bigcompetition.dto.StatsResultTableReqParams;
import com.ladbrokescoral.oxygen.bigcompetition.service.StatsCenterApiService;
import java.util.*;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
// @Slf4j
public class StatsCenterApiServiceImpl implements StatsCenterApiService {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private StatsCenterApiServiceCachable statsCenterApiServiceCachable;
  private Map<StatsResultTableReqParams, Long> regParams = new HashMap<>();
  private int refreshRate;
  private int cacheRefreshCountAfterItThreadValueUnused;

  @Autowired
  public StatsCenterApiServiceImpl(
      StatsCenterApiServiceCachable statsCenterApiServiceCachable,
      @Value("${statscenter.cache.refresh.rate}") int refreshRate,
      @Value("${statscenter.cache.refresh.count.after.it.thread.value.unused}")
          int cacheRefreshCountAfterItThreadValueUnused) {
    this.statsCenterApiServiceCachable = statsCenterApiServiceCachable;
    this.refreshRate = refreshRate;
    this.cacheRefreshCountAfterItThreadValueUnused = cacheRefreshCountAfterItThreadValueUnused;
  }

  @Override
  public Optional<List<ResultsTable>> getResultTables(
      Integer sportId, Integer areaId, Integer competitionId, Integer seasonId) {
    StatsResultTableReqParams statsResultTableReqParams =
        new StatsResultTableReqParams()
            .setSportId(sportId)
            .setAreaId(areaId)
            .setCompetitionId(competitionId)
            .setSeasonId(seasonId);
    regParams.put(statsResultTableReqParams, Calendar.getInstance().getTimeInMillis());
    return statsCenterApiServiceCachable.getResultTables(sportId, areaId, competitionId, seasonId);
  }

  @Override
  public Optional<List<SeasonMatches>> getSeasonMatches(
      Integer seasonId, Integer skip, Integer limit) {
    return statsCenterApiServiceCachable.getSeasonMatches(seasonId, skip, limit);
  }

  @Scheduled(fixedRateString = "${statscenter.cache.refresh.rate}")
  public void refreshStatsResultTables() {
    long count =
        regParams.entrySet().stream()
            .filter(this::doesCacheWasCalledAtListOneDuringNCacheRefreshes)
            .map(Map.Entry::getKey)
            .map(
                param ->
                    statsCenterApiServiceCachable.cachePutResultTables(
                        param.getSportId(),
                        param.getAreaId(),
                        param.getCompetitionId(),
                        param.getSeasonId()))
            .count();
    ASYNC_LOGGER.info("Updated stats center cache items {}", count);
  }

  private boolean doesCacheWasCalledAtListOneDuringNCacheRefreshes(
      Map.Entry<StatsResultTableReqParams, Long> e) {
    long lastPing = e.getValue();
    long now = Calendar.getInstance().getTimeInMillis();
    return now < lastPing + refreshRate * cacheRefreshCountAfterItThreadValueUnused;
  }

  public Optional<Match> getMatchDetails(String eventId) {
    return statsCenterApiServiceCachable.getMatchDetails(eventId);
  }
}
