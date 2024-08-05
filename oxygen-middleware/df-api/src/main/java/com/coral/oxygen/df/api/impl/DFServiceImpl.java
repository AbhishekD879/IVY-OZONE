package com.coral.oxygen.df.api.impl;

import com.coral.oxygen.df.api.DFService;
import com.coral.oxygen.df.api.HealthStatus;
import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import com.coral.oxygen.middleware.pojos.model.df.RaceEvents;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.io.IOException;
import java.util.Collection;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;
import org.springframework.util.ObjectUtils;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.jackson.JacksonConverterFactory;

@Slf4j
public class DFServiceImpl implements DFService {

  private static final String LOCALE = "en-GB";
  private static final String DELIMITER = ",";

  private DFEndpoint endpoint;

  private HealthStatus healthStatus = HealthStatus.OUT_OF_SERVICE;

  private String version;

  private String apiKey;

  public DFServiceImpl(String baseUrl, String version, String apiKey, OkHttpClient okHttpClient) {
    this.version = version;
    this.apiKey = apiKey;

    ObjectMapper mapper =
        Jackson2ObjectMapperBuilder.json()
            .featuresToEnable(DeserializationFeature.ACCEPT_SINGLE_VALUE_AS_ARRAY)
            .build();

    this.endpoint =
        new Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(okHttpClient)
            .addConverterFactory(JacksonConverterFactory.create(mapper))
            .build()
            .create(DFEndpoint.class);
  }

  private <T> Optional<T> executeRequest(Call<T> call) throws IOException {
    Response<T> response = call.execute();
    if (!response.isSuccessful()) {
      Object body = response.errorBody() != null ? response.errorBody().string() : null;
      log.warn("Response code: {}, errorBody: {}.", response.code(), body);
      return Optional.empty();
    }
    return Optional.ofNullable(response.body());
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<RaceEvent> getRaceEvent(Integer category, Long eventId) {
    return getRaceEvent(category, eventId, "/df-race-event-" + category);
  }

  @Trace(dispatcher = true)
  @Override
  public Optional<Map<Long, RaceEvent>> getRaceEvents(Integer category, Collection<Long> eventIds) {
    return getRaceEvents(eventIds, category, "/df-race-events-" + category);
  }

  private Optional<RaceEvent> getRaceEvent(int category, Long eventId, String transactionName) {
    try {
      NewRelic.setTransactionName(null, transactionName);
      Call<RaceEvents> raceEventCall =
          endpoint.getRaceEvent(version, category, String.valueOf(eventId), LOCALE, apiKey);
      RaceEvents raceEvents = executeRequest(raceEventCall).orElse(new RaceEvents());
      validateResponse(raceEvents, eventId);
      setHealthOK();
      return Optional.ofNullable(raceEvents.getDocument().getEventMap().get(eventId));
    } catch (IOException e) {
      handleError(String.valueOf(eventId), transactionName, e);
      return Optional.empty();
    }
  }

  private Optional<Map<Long, RaceEvent>> getRaceEvents(
      Collection<Long> eventIds, int category, String tranName) {
    Optional<Map<Long, RaceEvent>> eventMap = Optional.empty();
    if (!ObjectUtils.isEmpty(eventIds)) {
      eventMap = doGetRaceEvents(eventIds, category, tranName);
    }
    return eventMap;
  }

  private Optional<Map<Long, RaceEvent>> doGetRaceEvents(
      Collection<Long> eventIds, int category, String tranName) {
    String commaSeparatedEventIds = getCommaSeparatedEventIds(eventIds);
    try {
      NewRelic.setTransactionName(null, tranName);
      Call<RaceEvents> raceEventCall =
          endpoint.getRaceEvent(version, category, commaSeparatedEventIds, LOCALE, apiKey);
      RaceEvents raceEvents = executeRequest(raceEventCall).orElse(new RaceEvents());
      setHealthOK();
      validateResponse(raceEvents, commaSeparatedEventIds);
      return Optional.ofNullable(raceEvents.getDocument().getEventMap());
    } catch (IOException e) {
      handleError(commaSeparatedEventIds, tranName, e);
      return Optional.empty();
    }
  }

  private void validateResponse(RaceEvents raceEvents, String eventIds) throws DFApiException {
    if (ObjectUtils.isEmpty(raceEvents.getDocument())) {
      throw new DFApiException("Can't find data in response for ids :" + eventIds);
    }
  }

  private String getCommaSeparatedEventIds(Collection<Long> eventIds) {
    return eventIds.size() > 1
        ? eventIds.stream().map(String::valueOf).collect(Collectors.joining(DELIMITER))
        : String.valueOf(eventIds.iterator().next());
  }

  private void handleError(String eventIds, String transactionName, IOException e) {
    setHealthFail();
    log.error(
        "Error while loading data by eventId {} with transaction {}", eventIds, transactionName, e);
    NewRelic.noticeError(e);
  }

  private void validateResponse(RaceEvents raceEvents, Long eventId) throws DFApiException {
    if ((raceEvents.isError()) || !containsEventId(raceEvents, eventId)) {
      throw new DFApiException("Can't find data in response for event :" + eventId);
    }
  }

  private boolean containsEventId(RaceEvents events, Long eventId) {
    return !ObjectUtils.isEmpty(events.getDocument())
        && events.getDocument().getEventMap().containsKey(eventId);
  }

  @Override
  public HealthStatus getHealthStatus() {
    return healthStatus;
  }

  private void setHealthOK() {
    healthStatus = HealthStatus.OK;
  }

  private void setHealthFail() {
    healthStatus = HealthStatus.OUT_OF_SERVICE;
  }

  private class DFApiException extends IOException {

    DFApiException(Throwable t) {
      super(t);
    }

    DFApiException(String msg) {
      super(msg);
    }
  }
}
