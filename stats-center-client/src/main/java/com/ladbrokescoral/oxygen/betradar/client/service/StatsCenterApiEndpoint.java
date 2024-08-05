package com.ladbrokescoral.oxygen.betradar.client.service;

import com.ladbrokescoral.oxygen.betradar.client.entity.*;
import java.util.List;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Headers;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface StatsCenterApiEndpoint {
  @GET("/api/brcompetitionseason/{category}/{clazz}/{type}")
  @Headers("Accept: application/json")
  Call<BrCompetitionSeason> getAllCompetitions(
      @Path("category") Integer category, @Path("clazz") Integer clazz, @Path("type") Integer type);

  @GET("/api/seasons/{sportId}/{areaId}/{competitionId}")
  @Headers("Accept: application/json")
  Call<List<StatsSeason>> getAllSeasons(
      @Path("sportId") Integer sportId,
      @Path("areaId") Integer areaId,
      @Path("competitionId") Integer competitionId);

  @GET("/api/resultstables/{sportId}/{areaId}/{competitionId}/{seasonId}")
  @Headers("Accept: application/json")
  Call<List<ResultsTable>> getResultTables(
      @Path("sportId") Integer sportId,
      @Path("areaId") Integer areaId,
      @Path("competitionId") Integer competitionId,
      @Path("seasonId") Integer seasonId);

  @GET("api/season/{seasonId}/matches/")
  @Headers("Accept: application/json")
  Call<List<SeasonMatches>> getSeasonMatches(
      @Path("seasonId") Integer seasonId,
      @Query("skip") Integer skip,
      @Query("limit") Integer limit);

  @GET("/api/match/{eventId}")
  @Headers("Accept: application/json")
  Call<Match> getMatch(@Path("eventId") String eventId);
}
