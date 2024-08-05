package com.ladbrokescoral.oxygen.buildyourbetms.config;

import static org.springframework.http.HttpMethod.GET;
import static org.springframework.http.HttpMethod.OPTIONS;
import static org.springframework.http.HttpMethod.POST;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.FacadeHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.handler.impl.OptionsHandler;
import java.util.function.Function;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.web.reactive.function.server.RequestPredicate;
import org.springframework.web.reactive.function.server.RequestPredicates;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.RouterFunctions;
import org.springframework.web.reactive.function.server.ServerResponse;

/** Contains router functions */
@Configuration
@RequiredArgsConstructor
public class RouteConfig {
  private static final String API_BASE_PATH = "/api";

  @Qualifier("options")
  private final OptionsHandler optionsHandler;

  public static final String CORRELATION_ID_HEADER_KEY = "X-Correlation-Id";

  @Bean
  public RouterFunction<ServerResponse> leagues(@Qualifier("leagues") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/leagues")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> events(@Qualifier("events") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/events")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> event(@Qualifier("event") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/events/{id}")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> markets(@Qualifier("markets") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/markets")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> marketsGrouped(
      @Qualifier("markets-grouped") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/markets-grouped")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> marketsGroupedByGroupName(
      @Qualifier("markets-by-group-name") FacadeHandler handler) {
    return route(GET, api(version(2).apply("/markets-grouped")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> price(@Qualifier("price") FacadeHandler handler) {
    return route(POST, api(version(1).apply("/price")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> selections(@Qualifier("selections") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/selections")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> leaguesUpcoming(
      @Qualifier("leagues-upcoming") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/leagues-upcoming")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> players(@Qualifier("players") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/players")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> playerStatistics(
      @Qualifier("player-statistics") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/player-statistics")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> playerStatisticsByOptaId(
      @Qualifier("player-stats-by-opta-id") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/player-stats-by-opta-id")), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> statisticValueRange(
      @Qualifier("statistic-value-range") FacadeHandler handler) {
    return route(GET, api(version(1).apply("/statistic-value-range")), handler);
  }

  /**
   * adds additional OPTIONS handler for each request.
   *
   * @param method
   * @param path
   * @param handler
   * @return
   */
  private RouterFunction<ServerResponse> route(
      HttpMethod method, String path, FacadeHandler handler) {
    RequestPredicate pathPredicate = RequestPredicates.path(path);
    return RouterFunctions.route(
            RequestPredicates.method(method).and(pathPredicate), handler::handle)
        .andRoute(
            RequestPredicates.method(OPTIONS).and(pathPredicate),
            request -> optionsHandler.handle(request, method));
  }

  private static String api(String apiPath) {
    return API_BASE_PATH + apiPath;
  }

  private static Function<String, String> version(int version) {
    return api -> String.format("/v%d", version) + api;
  }
}
