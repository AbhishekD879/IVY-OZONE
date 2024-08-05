package com.entain.oxygen.router;

import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("options")
public class OptionsHandler {

  public Mono<ServerResponse> handle(HttpMethod... methods) {
    return ServerResponse.ok()
        .header("allow", Stream.of(methods).map(HttpMethod::name).collect(Collectors.joining(",")))
        .build();
  }
}
