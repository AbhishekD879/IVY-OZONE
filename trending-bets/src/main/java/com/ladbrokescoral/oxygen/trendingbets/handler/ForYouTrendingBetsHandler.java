package com.ladbrokescoral.oxygen.trendingbets.handler;

import com.coral.bpp.api.exception.BppUnauthorizedException;
import com.coral.bpp.api.service.BppApiAsync;
import com.ladbrokescoral.oxygen.trendingbets.model.PersonalizedBetsDto;
import com.ladbrokescoral.oxygen.trendingbets.service.ForYouBetsService;
import java.util.Optional;
import java.util.function.Function;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SynchronousSink;

@Component
@Qualifier("fyTrendingBets")
@RequiredArgsConstructor
@Slf4j
public class ForYouTrendingBetsHandler implements ApiHandler {

  private final BppApiAsync bppApiAsync;

  private final ForYouBetsService betsService;

  @Override
  public Mono<ServerResponse> handle(ServerRequest request) {
    Optional<String> optionalToken = getToken(request);
    return optionalToken
        .map(
            token ->
                getUserName(token)
                    .handle(
                        (String userName, SynchronousSink<Mono<PersonalizedBetsDto>> sink) -> {
                          try {
                            sink.next(betsService.processTrendingBets(userName));
                          } catch (Exception e) {
                            log.error("Exception in fetching persolized bets ", e);
                            sink.error(e);
                          }
                        })
                    .flatMap(Function.identity())
                    .map(items -> ServerResponse.ok().bodyValue(items))
                    .flatMap(Function.identity())
                    .onErrorResume(this::error))
        .orElse(ServerResponse.badRequest().bodyValue("token not present"));
  }

  private Mono<String> getUserName(String token) {
    return bppApiAsync.getUserData(token).map(user -> user.getSportBookUserName());
  }

  private Mono<ServerResponse> error(Throwable ex) {
    if (ex.getCause() != null) {
      ex = ex.getCause();
    }
    HttpStatus status =
        ex instanceof BppUnauthorizedException
            ? HttpStatus.UNAUTHORIZED
            : HttpStatus.INTERNAL_SERVER_ERROR;
    return ServerResponse.status(status).bodyValue(ex.getMessage() != null ? ex.getMessage() : "");
  }
}
