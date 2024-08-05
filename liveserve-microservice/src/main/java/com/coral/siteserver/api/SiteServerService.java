package com.coral.siteserver.api;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.EventNotFoundExceptions;
import com.coral.siteserver.model.Children;
import com.coral.siteserver.model.Event;
import com.coral.siteserver.model.SSResponse;
import com.google.common.collect.Lists;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import retrofit2.Call;
import retrofit2.Response;

@Slf4j
public class SiteServerService {
  private final String apiVersion;
  private final int maxNumberOfRetries;
  private final CallsAPI api;
  private int pageSize = 100;

  @Value("${siteserver.priceboost.simplefilter.value}")
  private String hasPriceStreamValue;

  @Value("${siteserver.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Value("${siteserver.priceboost.simplefilter.key}")
  private String hasPriceStreamKey;

  public SiteServerService(CallsAPI api, String apiVersion, int maxNumberOfRetries) {
    this.api = api;
    this.apiVersion = apiVersion;
    this.maxNumberOfRetries = maxNumberOfRetries;
  }

  private Optional<SSResponse> invokeSyncRequest(Call<SSResponse> call) {
    Response<SSResponse> response = null;
    int counter = 0;
    boolean retry;
    do {
      retry = false;
      try {
        Call<SSResponse> localCall = call.clone();
        response = localCall.execute();
        if (!response.isSuccessful()) {
          throw new SiteServerException("Error response");
        }
      } catch (SiteServerException e) {
        throw new SiteServerException(e);
      } catch (Exception e) {
        log.error("Can't get data from SiteServer API: for URL " + call.request().url(), e);
        NewRelic.noticeError(e);
        if (counter < this.maxNumberOfRetries) {
          retry = true;
          counter++;
          log.info(
              "Retry {} for getting data from SiteServer API: {}", counter, call.request().url());
        }
      }
    } while (retry);
    if (response != null && response.isSuccessful()) {
      return Optional.ofNullable(response.body());
    } else {
      return Optional.empty();
    }
  }

  @Trace(metricName = "EventToMarketForMarket")
  public Call<SSResponse> getMarketCall(long id) {
    return api.getEventToMarketForMarket(this.apiVersion, String.valueOf(id), true, true);
  }

  @Trace(metricName = "EventToOutcomeForOutcome")
  public Call<SSResponse> getSelectionCall(long id) {
    return api.getEventToOutcomeForOutcome(
        this.apiVersion, String.valueOf(id), getSimpleFilter(), true, true);
  }

  private List<String> getSimpleFilter() {
    SimpleFilter filter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addHasPricestream(hasPriceStreamKey, hasPriceStreamValue, isPriceBoostEnabled)
                .build();
    return filter.getQueryMap();
  }

  @Trace(metricName = "Events")
  private Call<SSResponse> getEventsCall(String ids) {
    return api.getEvents(this.apiVersion, ids, false);
  }

  @Trace(metricName = "Events")
  public List<Long> getEventIdS(List<Long> ids) {
    return pagedCalls(
        ids,
        pageSize,
        input ->
            this.invokeSyncRequest(
                    getEventsCall(
                        input.stream().map(String::valueOf).collect(Collectors.joining(","))))
                .orElseGet(SSResponse::new)
                .getChildren()
                .stream()
                .filter(e -> e.getEvent() != null)
                .map(Children::getEvent)
                .map(e -> Long.parseLong(e.getId()))
                .collect(Collectors.toCollection(ArrayList::new)));
  }

  @Trace(metricName = "Events")
  public long getEventId(Call<SSResponse> call) throws EventNotFoundExceptions {
    return Long.parseLong(doGetEvents(call).orElseThrow(EventNotFoundExceptions::new).getId());
  }

  protected Optional<Event> doGetEvents(Call<SSResponse> call) {
    return this.invokeSyncRequest(call).orElseGet(SSResponse::new).getChildren().stream()
        .map(Children::getEvent)
        .filter(Objects::nonNull)
        .findFirst();
  }

  protected static <T, H> List<T> pagedCalls(List<H> data, int pageSize, SiteServeCall<T, H> call) {
    List<List<H>> lists = Lists.partition(data, pageSize);
    return lists.stream()
        .flatMap(
            m -> {
              List<T> list = call.call(m);
              return list.stream();
            })
        .collect(Collectors.toCollection(ArrayList::new));
  }

  public void setPageSize(int pageSize) {
    if (pageSize <= 0) {
      throw new IllegalArgumentException("pageSize <= 0");
    }
    this.pageSize = pageSize;
  }

  private interface SiteServeCall<T, H> {

    List<T> call(List<H> lists);
  }
}
