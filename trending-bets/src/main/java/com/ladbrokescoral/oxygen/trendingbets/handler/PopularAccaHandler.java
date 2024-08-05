package com.ladbrokescoral.oxygen.trendingbets.handler;

import com.ladbrokescoral.oxygen.trendingbets.dto.PopularAccaDto;
import com.ladbrokescoral.oxygen.trendingbets.service.PopularAccaService;
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
@Qualifier("popularAccas")
@RequiredArgsConstructor
@Slf4j
public class PopularAccaHandler implements ApiHandler {

  private final PopularAccaService popularAccaService;

  @Override
  public Mono<ServerResponse> handle(ServerRequest request) {

    return request
        .bodyToMono(PopularAccaDto.class)
        .map(popularAccaService::processRequest)
        .map(response -> ServerResponse.ok().bodyValue(response))
        .flatMap(Function.identity())
        .onErrorResume(this::error);
  }

  private Mono<ServerResponse> error(Throwable ex) {
    return ServerResponse.status(HttpStatus.INTERNAL_SERVER_ERROR)
        .bodyValue("exception occured while processing request ::" + ex.getMessage());
  }
}
