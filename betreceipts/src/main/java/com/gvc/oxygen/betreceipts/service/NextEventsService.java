package com.gvc.oxygen.betreceipts.service;

import com.egalacoral.spark.siteserver.model.Event;
import com.gvc.oxygen.betreceipts.config.NextRaceProps;
import com.gvc.oxygen.betreceipts.entity.TypeFlagCodes;
import com.gvc.oxygen.betreceipts.service.siteserve.NextEventsParameters;
import com.gvc.oxygen.betreceipts.service.siteserve.SiteServeService;
import com.gvc.oxygen.betreceipts.utils.NextRacesConstants;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Collections;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import reactor.core.publisher.Flux;

@Service
@Slf4j
public class NextEventsService {

  private NextRaceProps nextRaceProps;

  private SiteServeService siteServerService;

  @Autowired
  public NextEventsService(NextRaceProps nextRaceProps, SiteServeService siteServeService) {
    this.nextRaceProps = nextRaceProps;
    this.siteServerService = siteServeService;
  }

  public Flux<Event> getNextEvents() {
    return Flux.fromIterable(getNextEventsForTodayAndTomorrow());
  }

  /** Method for getting today or tomorrow events */
  private List<Event> getNextEventsForTodayAndTomorrow() {

    Instant tomorrow =
        Instant.now()
            .plus(NextRacesConstants.DAYS_TO_ADD, ChronoUnit.DAYS)
            .truncatedTo(ChronoUnit.DAYS);
    int remainingMinutes = (int) ChronoUnit.MINUTES.between(Instant.now(), tomorrow);
    // get events util tomorrow.
    return getSiteServerEvents(remainingMinutes);
  }

  private List<Event> getSiteServerEvents(int timePeriodMinutes) {
    NextEventsParameters.NextEventsParametersBuilder paramsBuilder = NextEventsParameters.builder();
    paramsBuilder
        .typeFlagCodes(
            TypeFlagCodes.of(NextRacesConstants.UK, NextRacesConstants.IE, NextRacesConstants.INT))
        .timePeriodMinutes(timePeriodMinutes)
        .categoryId(nextRaceProps.getCategoryId());
    NextEventsParameters params = paramsBuilder.build();

    List<String> classes = siteServerService.getActiveClassesForCategoryId(params.getCategoryId());
    if (CollectionUtils.isEmpty(classes)) {
      return Collections.emptyList();
    } else {
      return siteServerService.doGetNextRacesEvents(params, classes);
    }
  }
}
