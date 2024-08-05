package com.ladbrokescoral.oxygen.trendingbets.handler;

import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("trendingBets")
@RequiredArgsConstructor
@Slf4j
public class TrendingBetsApiHandler implements ApiHandler {

  @Override
  public Mono<ServerResponse> handle(ServerRequest request) {
    String channelId = request.pathVariable("channelId");
    return Optional.ofNullable(TrendingBetsContext.getTrendingBets().get(channelId))
        .map(trendingBetsDto -> ServerResponse.ok().bodyValue(trendingBetsDto))
        .orElse(ServerResponse.badRequest().bodyValue("Channel ID is not present"));
  }
}
