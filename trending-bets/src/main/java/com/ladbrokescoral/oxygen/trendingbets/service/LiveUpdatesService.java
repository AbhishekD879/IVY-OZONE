package com.ladbrokescoral.oxygen.trendingbets.service;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class LiveUpdatesService {

  private final LiveServService liveServService;

  @Autowired
  public LiveUpdatesService(@Lazy LiveServService liveServService) {
    this.liveServService = liveServService;
  }

  public void subscriberForEvent(Stream<String> events, String eventId) {

    events
        .filter(channel -> TrendingBetsContext.setSubscribedChannels(channel) == null)
        .forEach(
            (String channel) ->
                CompletableFuture.runAsync(
                    () -> liveServService.subscribe(channel, Long.valueOf(eventId))));
  }
}
