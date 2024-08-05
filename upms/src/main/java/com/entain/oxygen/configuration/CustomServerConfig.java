package com.entain.oxygen.configuration;

import java.util.Objects;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.web.embedded.netty.NettyReactiveWebServerFactory;
import org.springframework.boot.web.embedded.netty.NettyServerCustomizer;
import org.springframework.boot.web.server.WebServerFactoryCustomizer;
import org.springframework.context.ApplicationContext;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.HttpHandler;
import org.springframework.http.server.reactive.ReactorHttpHandlerAdapter;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.server.adapter.WebHttpHandlerBuilder;
import reactor.netty.http.server.HttpServer;

/** custom configuration to disable Http TRACE method in reactor netty Http server */
@Component
@Slf4j
@RequiredArgsConstructor
public class CustomServerConfig
    implements WebServerFactoryCustomizer<NettyReactiveWebServerFactory> {

  private final ApplicationContext applicationContext;

  @Override
  public void customize(NettyReactiveWebServerFactory factory) {
    HttpHandler next = WebHttpHandlerBuilder.applicationContext(applicationContext).build();
    HttpHandler handler =
        (ServerHttpRequest request, ServerHttpResponse response) -> {
          if (Objects.requireNonNull(request.getMethod())
              .name()
              .equalsIgnoreCase(HttpMethod.TRACE.name())) {
            response.setStatusCode(HttpStatus.METHOD_NOT_ALLOWED);
            return response.setComplete();
          }
          return next.handle(request, response);
        };
    factory.addServerCustomizers(new ReactiveNettyServerCustomizers(handler));
  }

  static class ReactiveNettyServerCustomizers implements NettyServerCustomizer {
    private final HttpHandler handler;

    public ReactiveNettyServerCustomizers(HttpHandler handler) {
      this.handler = handler;
    }

    @Override
    public HttpServer apply(HttpServer httpServer) {
      log.info("Custom Server Config:: applying Custom Server config");
      ReactorHttpHandlerAdapter reactorHttpHandlerAdapter = new ReactorHttpHandlerAdapter(handler);
      return httpServer.handle(reactorHttpHandlerAdapter);
    }
  }
}
