package com.entain.oxygen.router;

import static org.springframework.http.HttpMethod.*;
import static org.springframework.web.reactive.function.server.RequestPredicates.*;
import static org.springframework.web.reactive.function.server.RouterFunctions.nest;
import static org.springframework.web.reactive.function.server.RouterFunctions.route;

import com.entain.oxygen.filter.PreferenceFilter;
import com.entain.oxygen.handler.UserStableHandler;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.ServerResponse;

@Configuration
@Slf4j
@SuppressWarnings("java:S2211")
public class UserStableRouter {

  private final PreferenceFilter preferenceFilter;

  public UserStableRouter(PreferenceFilter preferenceFilter) {
    this.preferenceFilter = preferenceFilter;
  }

  @Bean
  RouterFunction<ServerResponse> routes(UserStableHandler userStableHandler) {
    return nest(
        path("/api/my-stable"),
        nest(
            accept(MediaType.APPLICATION_JSON),
            route(POST("/addHorse"), userStableHandler::saveOperation)
                .andRoute(
                    GET("/getMyStableDataWithoutNotes/{brand}"), userStableHandler::getOperation)
                .andRoute(
                    GET("/getNoteByHorseId/{brand}/{horseId}"),
                    userStableHandler::getHorseNotesById)
                .andRoute(PUT("/updateHorseNote"), userStableHandler::updateOperation)
                .andRoute(
                    DELETE("/deleteByHorseId/{brand}/{horseId}"),
                    userStableHandler::deleteOperation)
                .andRoute(GET("/cached/horseData"), userStableHandler::getCachedHorseInfo)
                .filter(
                    (request, next) -> {
                      long startTime = System.currentTimeMillis();
                      if ("/api/my-stable/cached/horseData".equals(request.uri().getPath())) {
                        return next.handle(request);

                      } else {
                        return preferenceFilter
                            .filter(request, next)
                            .doOnTerminate(
                                () -> {
                                  long endTime = System.currentTimeMillis();
                                  long executionTime = endTime - startTime;
                                  log.debug(
                                      "Total exec time for "
                                          + request.uri().getPath()
                                          + " : "
                                          + executionTime
                                          + "ms");
                                });
                      }
                    })));
  }
}
