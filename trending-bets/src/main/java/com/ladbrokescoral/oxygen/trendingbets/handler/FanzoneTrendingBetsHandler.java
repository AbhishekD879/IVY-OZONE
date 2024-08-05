package com.ladbrokescoral.oxygen.trendingbets.handler;

import com.ladbrokescoral.oxygen.trendingbets.service.FanzoneBetsService;
import java.util.function.Function;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("fanzoneTrendingBets")
@RequiredArgsConstructor
@Slf4j
public class FanzoneTrendingBetsHandler implements ApiHandler {

  private final FanzoneBetsService betsService;

  @Override
  public Mono<ServerResponse> handle(ServerRequest request) {
    String teamId = request.pathVariable("teamId");
    return betsService
        .processFanzoneTrendingBets(teamId)
        .map(fzBets -> ServerResponse.ok().bodyValue(fzBets))
        .flatMap(Function.identity())
        .onErrorResume(this::error);
  }

  private Mono<ServerResponse> error(Throwable ex) {
    return ServerResponse.status(HttpStatus.INTERNAL_SERVER_ERROR)
        .bodyValue(ex.getMessage() != null ? ex.getMessage() : "");
  }
}
