package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.FacadeHandler;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("options")
public class OptionsHandler implements FacadeHandler {

  @Override
  public Mono<ServerResponse> handle(ServerRequest request) {
    return ServerResponse.ok().build();
  }

  public Mono<ServerResponse> handle(ServerRequest request, HttpMethod... methods) {
    return ServerResponse.ok()
        .header("allow", Stream.of(methods).map(HttpMethod::name).collect(Collectors.joining(",")))
        .build();
  }
}
