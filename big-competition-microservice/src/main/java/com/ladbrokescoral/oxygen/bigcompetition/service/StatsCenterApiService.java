package com.ladbrokescoral.oxygen.bigcompetition.service;

import com.ladbrokescoral.oxygen.betradar.client.entity.Match;
import com.ladbrokescoral.oxygen.betradar.client.entity.ResultsTable;
import com.ladbrokescoral.oxygen.betradar.client.entity.SeasonMatches;
import java.util.List;
import java.util.Optional;

public interface StatsCenterApiService {
  String RESULT_TABLES = "resultTables";
  String SEASON_MATCHES = "seasonMatches";
  String MATCH = "match";

  Optional<List<ResultsTable>> getResultTables(
      Integer sportId, Integer areaId, Integer competitionId, Integer seasonId);

  Optional<List<SeasonMatches>> getSeasonMatches(Integer seasonId, Integer skip, Integer limit);

  Optional<Match> getMatchDetails(String eventId);
}
