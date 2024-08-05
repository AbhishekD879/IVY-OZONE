package com.entain.oxygen.filter;

import com.entain.oxygen.service.BppService;
import com.entain.oxygen.util.RequestContextHolderUtils;
import java.util.Optional;
import java.util.function.Function;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.reactive.function.server.HandlerFilterFunction;
import org.springframework.web.reactive.function.server.HandlerFunction;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SynchronousSink;

@Component
@Slf4j
@RequiredArgsConstructor
public class PreferenceFilter implements HandlerFilterFunction<ServerResponse, ServerResponse> {

  private final BppService bppService;

  @Override
  public Mono<ServerResponse> filter(ServerRequest request, HandlerFunction<ServerResponse> next) {
    String token = Optional.ofNullable(request.headers().firstHeader("token")).orElse("");
    long startTime = System.currentTimeMillis();
    if (!StringUtils.hasLength(token)) {
      log.error("token absent in the request header");
      return ServerResponse.status(HttpStatus.BAD_REQUEST).bodyValue("Token Required");
    }

    return this.bppService
        .favUserdata(token)
        .handle(
            (String username, SynchronousSink<Mono<ServerResponse>> sink) -> {
              long executionTime = System.currentTimeMillis() - startTime;
              log.debug("request: {} : bpp call time: {} ms", request.path(), executionTime);
              sink.next(
                  next.handle(request)
                      .contextWrite(
                          context ->
                              RequestContextHolderUtils.putTokenInContext(context, username)));
            })
        .flatMap(Function.identity())
        .onErrorResume(
            (Throwable exception) -> {
              log.error("Filter::failed to get resp from BPP :: User not Found");
              return ServerResponse.status(HttpStatus.INTERNAL_SERVER_ERROR)
                  .bodyValue(exception.getMessage());
            });
  }
}
