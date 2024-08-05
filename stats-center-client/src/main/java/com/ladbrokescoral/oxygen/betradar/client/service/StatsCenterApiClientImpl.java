package com.ladbrokescoral.oxygen.betradar.client.service;

import com.ladbrokescoral.oxygen.betradar.client.entity.BrCompetitionSeason;
import com.ladbrokescoral.oxygen.betradar.client.entity.Match;
import com.ladbrokescoral.oxygen.betradar.client.entity.ResultsTable;
import com.ladbrokescoral.oxygen.betradar.client.entity.SeasonMatches;
import com.ladbrokescoral.oxygen.betradar.client.entity.StatsSeason;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.jackson.JacksonConverterFactory;

@Slf4j
public class StatsCenterApiClientImpl implements StatsCenterApiClient {

  private StatsCenterApiEndpoint statsCenterApiEndpoint;

  public StatsCenterApiClientImpl(String statsCenterBaseUrl) {
    OkHttpClient httpClient = new OkHttpClient.Builder().build();

    Retrofit retrofit =
        new Retrofit.Builder()
            .baseUrl(statsCenterBaseUrl)
            .addConverterFactory(JacksonConverterFactory.create())
            .client(httpClient)
            .build();
    statsCenterApiEndpoint = retrofit.create(StatsCenterApiEndpoint.class);
  }

  @Override
  public Optional<BrCompetitionSeason> getAllCompetitions(
      Integer category, Integer clazz, Integer type) {
    return invokeSyncRequest(statsCenterApiEndpoint.getAllCompetitions(category, clazz, type));
  }

  @Override
  public Optional<List<StatsSeason>> getAllSeasons(
      Integer sportId, Integer areaId, Integer competitionId) {
    return invokeSyncRequest(statsCenterApiEndpoint.getAllSeasons(sportId, areaId, competitionId));
  }

  @Override
  public Optional<List<ResultsTable>> getResultTables(
      Integer sportId, Integer areaId, Integer competitionId, Integer seasonId) {
    return invokeSyncRequest(
        statsCenterApiEndpoint.getResultTables(sportId, areaId, competitionId, seasonId));
  }

  @Override
  public Optional<List<SeasonMatches>> getSeasonMathces(
      Integer seasonId, Integer skip, Integer limit) {
    return invokeSyncRequest(statsCenterApiEndpoint.getSeasonMatches(seasonId, skip, limit));
  }

  @Override
  public Optional<Match> getMatch(String eventId) {
    return invokeSyncRequest(statsCenterApiEndpoint.getMatch(eventId));
  }

  private <T> Optional<T> invokeSyncRequest(Call<T> call) {
    try {
      Response<T> response = call.execute();
      if (response.isSuccessful()) {
        return Optional.ofNullable(response.body());
      } else {
        if (HttpURLConnection.HTTP_NOT_FOUND == response.code()) {
          log.warn(
              "Can't get data from stats-center-api. Not found for URL " + call.request().url());
        } else {
          log.error(
              "Can't get data from stats-center-api. Response is unsuccessful for URL "
                  + call.request().url());
        }
        return Optional.empty();
      }
    } catch (IOException e) {
      log.error(
          "Can't get data from stats-center-api. Error occurred for URL " + call.request().url(),
          e);
      return Optional.empty();
    }
  }
}
