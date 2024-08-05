package com.ladbrokescoral.oxygen.betradar.client.service;

import com.ladbrokescoral.oxygen.betradar.client.entity.*;
import java.util.List;
import java.util.Optional;

public interface StatsCenterApiClient {
  Optional<BrCompetitionSeason> getAllCompetitions(Integer category, Integer clazz, Integer type);

  Optional<List<StatsSeason>> getAllSeasons(Integer sportId, Integer areaId, Integer competitionId);

  Optional<List<ResultsTable>> getResultTables(
      Integer sportId, Integer areaId, Integer competitionId, Integer seasonId);

  Optional<List<SeasonMatches>> getSeasonMathces(Integer seasonId, Integer skip, Integer limit);

  Optional<Match> getMatch(String eventId);
}
