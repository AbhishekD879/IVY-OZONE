package com.ladbrokescoral.oxygen.buildyourbetms.handler;

import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.reactive.function.server.ServerRequest;
import reactor.core.publisher.Mono;

public abstract class BanachApiProxyHandler<T> implements FacadeHandler {

  private final BanachClient<Mono<T>> banachClient;

  @Autowired
  protected BanachApiProxyHandler(BanachClient<Mono<T>> banachClient) {
    this.banachClient = banachClient;
  }

  protected BanachClient<Mono<T>> getClient() {
    return banachClient;
  }

  protected String getCorrelationId(ServerRequest request) {
    List<String> correlationIdHeader = request.headers().header("X-Correlation-Id");
    if (!correlationIdHeader.isEmpty()) {
      return correlationIdHeader.get(correlationIdHeader.size() - 1);
    } else {
      return "unknown";
    }
  }
}
