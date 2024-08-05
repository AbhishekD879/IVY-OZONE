package com.entain.oxygen.router;

import static org.springframework.http.HttpMethod.OPTIONS;

import com.entain.oxygen.filter.PreferenceFilter;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpMethod;
import org.springframework.web.reactive.function.server.*;

@AllArgsConstructor
public abstract class RouteConfig {

  private OptionsHandler optionsHandler;

  private PreferenceFilter preferenceFilter;

  public RouterFunction<ServerResponse> route(
      HttpMethod method, String path, HandlerFunction<ServerResponse> handler) {
    RequestPredicate pathPredicate = RequestPredicates.path(path);
    return RouterFunctions.route(RequestPredicates.method(method).and(pathPredicate), handler)
        .filter(preferenceFilter)
        .andRoute(
            RequestPredicates.method(OPTIONS).and(pathPredicate),
            request -> optionsHandler.handle(method));
  }
}
