package com.entain.oxygen.router;

import com.entain.oxygen.filter.PreferenceFilter;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.web.reactive.function.server.*;

@Configuration
public class UserPreferenceRouter extends RouteConfig {

  private static final String ROUTE_PATH = "/oddsPreference";
  private final PreferenceFacadeHandler facadeHandler;
  private final OptionsHandler optionsHandler;

  public UserPreferenceRouter(
      OptionsHandler optionsHandler,
      PreferenceFilter preferenceFilter,
      @Qualifier("userPreferenceHandler") PreferenceFacadeHandler facadeHandler) {
    super(optionsHandler, preferenceFilter);
    this.facadeHandler = facadeHandler;
    this.optionsHandler = optionsHandler;
  }

  @Bean
  public RouterFunction<ServerResponse> saveOddsPreference() {
    return route(HttpMethod.POST, ROUTE_PATH, facadeHandler::saveOperation);
  }

  @Bean
  public RouterFunction<ServerResponse> getOddsPreference() {
    return route(HttpMethod.GET, ROUTE_PATH + "/{brand}", facadeHandler::getOperation);
  }

  @Bean
  public RouterFunction<ServerResponse> getAllOddsPreferencesByBrandHandle() {
    return routerFunction(
        HttpMethod.GET,
        ROUTE_PATH + "/preferences/brand/{brand}",
        facadeHandler::getAllOddsPreferencesByBrand);
  }

  @Bean
  public RouterFunction<ServerResponse> getAllOddsPreferences() {
    return routerFunction(HttpMethod.GET, ROUTE_PATH, facadeHandler::getAllOddsPreference);
  }

  @Bean
  public RouterFunction<ServerResponse> updateOddsPreference() {
    return route(HttpMethod.PUT, ROUTE_PATH, facadeHandler::updateOperation);
  }

  @Bean
  public RouterFunction<ServerResponse> deleteOddsPreference() {
    return route(HttpMethod.DELETE, ROUTE_PATH + "/{brand}", facadeHandler::deleteOperation);
  }

  private RouterFunction<ServerResponse> routerFunction(
      HttpMethod httpMethod, String routePath, HandlerFunction<ServerResponse> function) {
    RequestPredicate pathPredicate = RequestPredicates.path(routePath);
    return RouterFunctions.route(RequestPredicates.method(httpMethod).and(pathPredicate), function)
        .andRoute(
            RequestPredicates.method(HttpMethod.OPTIONS).and(pathPredicate),
            request -> optionsHandler.handle(httpMethod));
  }
}
