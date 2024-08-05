package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.model.cms.EventDetails;
import com.ladbrokescoral.oxygen.questionengine.service.EventDetailsService;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.service.SiteServerService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;

import java.util.Collections;

@Slf4j
@Service
@AllArgsConstructor
public class EventDetailsServiceImpl implements EventDetailsService {
  private static final String SITE_SERVE_EVENT_NAME_DELIMITER = "|";

  private final SiteServerService ssService;
  private final CmsService cmsService;
  private final QuizService quizService;

  @Override
  public void requestEventDetails() {
    quizService.findLiveQuizzes()
        .stream()
        .filter(quiz -> quiz.getEventDetails() != null)
        .filter(quiz -> StringUtils.isNotEmpty(quiz.getEventDetails().getEventId()))
        .filter(QuizDto::isEventScoresEmpty)
        .forEach(this::updateQuizEventDetails);
  }
  
  private void updateQuizEventDetails(QuizDto quiz) {
    ssService.getEventDetails(quiz.getEventDetails().getEventId()).ifPresent(event -> {
      updateEventDetails(quiz, event);
      updateEventDetailsByScores(quiz, event);
    });
  }

  private void updateEventDetailsByScores(QuizDto quiz, Event event) {
    if (ssService.isMatchFinished(event)) {
      cmsService.updateQuizEventDetails(quiz.getId(), 
          getEventDetails(event).setActualScores(ssService.findScoresForEvent(event)));
    }
  }

  private void updateEventDetails(QuizDto quiz, Event event) {
    if (quiz.isEventStartTimeEmpty()) {
      cmsService.updateQuizEventDetails(quiz.getId(), getEventDetails(event));
    }
  }

  private EventDetails getEventDetails(Event event) {
    return new EventDetails()
        .setEventId(event.getId())
        .setEventName(StringUtils.remove(event.getName(), SITE_SERVE_EVENT_NAME_DELIMITER))
        .setStartTime(event.getStartTime())
        .setActualScores(Collections.emptyList()); 
  }

}
