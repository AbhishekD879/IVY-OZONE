package com.ladbrokescoral.oxygen.questionengine.job;

import com.ladbrokescoral.oxygen.questionengine.configuration.annotation.ExcludeFromIntegrationTests;
import com.ladbrokescoral.oxygen.questionengine.service.EventDetailsService;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@ExcludeFromIntegrationTests
public class RequestScoresScheduler {
  
  private final EventDetailsService eventDetailsService;

  @Scheduled(fixedDelayString = "${application.requestScoresPeriod}")
  public void requestScores() {
    eventDetailsService.requestEventDetails();
  }

}
