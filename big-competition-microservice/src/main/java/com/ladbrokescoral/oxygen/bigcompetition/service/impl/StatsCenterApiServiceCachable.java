package com.ladbrokescoral.oxygen.bigcompetition.service.impl;

import com.ladbrokescoral.oxygen.betradar.client.entity.Match;
import com.ladbrokescoral.oxygen.betradar.client.entity.ResultsTable;
import com.ladbrokescoral.oxygen.betradar.client.entity.SeasonMatches;
import com.ladbrokescoral.oxygen.betradar.client.service.StatsCenterApiClient;
import com.ladbrokescoral.oxygen.bigcompetition.service.StatsCenterApiService;
import com.ladbrokescoral.oxygen.bigcompetition.util.Utils;
import java.util.List;
import java.util.Optional;
import lombok.AllArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
// @Slf4j
@AllArgsConstructor
public class StatsCenterApiServiceCachable implements StatsCenterApiService {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private final StatsCenterApiClient statsCenterApiClient;

  @Override
  @Cacheable(value = RESULT_TABLES)
  public Optional<List<ResultsTable>> getResultTables(
      Integer sportId, Integer areaId, Integer competitionId, Integer seasonId) {
    return cachePutResultTables(sportId, areaId, competitionId, seasonId);
  }

  @CachePut(value = RESULT_TABLES)
  public Optional<List<ResultsTable>> cachePutResultTables(
      Integer sportId, Integer areaId, Integer competitionId, Integer seasonId) {
    ASYNC_LOGGER.info(
        "Cache refreshed 'getResultTables({}, {}, {}, {})'",
        sportId,
        areaId,
        competitionId,
        seasonId);
    Utils.newRelicLogTransaction("/StatsCenter-getResultTables");
    return statsCenterApiClient.getResultTables(sportId, areaId, competitionId, seasonId);
  }

  @Override
  @Cacheable(value = SEASON_MATCHES)
  public Optional<List<SeasonMatches>> getSeasonMatches(
      Integer seasonId, Integer skip, Integer limit) {
    Utils.newRelicLogTransaction("/StatsCenter-getSeasonMathces");
    return statsCenterApiClient.getSeasonMathces(seasonId, skip, limit);
  }

  @Cacheable(value = MATCH)
  public Optional<Match> getMatchDetails(String eventId) {
    Utils.newRelicLogTransaction("/StatsCenter-getMatch");
    return statsCenterApiClient.getMatch(eventId);
  }
}
