package com.ladbrokescoral.oxygen.trendingbets.configuration;

import com.ladbrokescoral.oxygen.trendingbets.handler.ApiHandler;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.web.reactive.function.server.*;

@Configuration
public class RouteConfig {

  private static final String API_BASE_PATH = "/api";

  @Bean
  public RouterFunction<ServerResponse> trendingBetsBetslip(
      @Qualifier("trendingBets") ApiHandler handler) {
    return route(HttpMethod.GET, api("/trendingbets/betslip/{channelId}"), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> trendingStatistics(
      @Qualifier("trendingStats") ApiHandler handler) {
    return RouterFunctions.route()
        .GET(api("/trendingstats"), handler::handle)
        .GET(api("/trendingstats/{stats}"), handler::handle)
        .build();
  }

  @Bean
  public RouterFunction<ServerResponse> forYouTrendingBets(
      @Qualifier("fyTrendingBets") ApiHandler handler) {
    return route(HttpMethod.GET, api("/fy/tb"), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> fzTrendingBets(
      @Qualifier("fanzoneTrendingBets") ApiHandler handler) {
    return route(HttpMethod.GET, api("/fanzone/tb/{teamId}"), handler);
  }

  @Bean
  public RouterFunction<ServerResponse> popularacca(@Qualifier("popularAccas") ApiHandler handler) {
    return route(HttpMethod.POST, api("/popular-acca"), handler);
  }

  private RouterFunction<ServerResponse> route(HttpMethod method, String path, ApiHandler handler) {
    RequestPredicate pathPredicate = RequestPredicates.path(path);
    return RouterFunctions.route(
        RequestPredicates.method(method).and(pathPredicate), handler::handle);
  }

  private static String api(String apiPath) {
    return API_BASE_PATH + apiPath;
  }
}
