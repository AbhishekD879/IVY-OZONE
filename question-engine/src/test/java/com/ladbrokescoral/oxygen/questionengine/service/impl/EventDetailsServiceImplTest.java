package com.ladbrokescoral.oxygen.questionengine.service.impl;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.service.EventDetailsService;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.service.SiteServerService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import java.util.Collections;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import uk.co.jemos.podam.api.PodamFactory;
import uk.co.jemos.podam.api.PodamFactoryImpl;

@RunWith(MockitoJUnitRunner.class)
public class EventDetailsServiceImplTest {

  @Mock
  private SiteServerService ssService;
  @Mock
  private CmsService cmsService;
  @Mock
  private QuizService quizService;

  private EventDetailsService eventDetailsService;

  private PodamFactory factory = new PodamFactoryImpl();

  @Before
  public void setUp() {
    eventDetailsService = new EventDetailsServiceImpl(ssService, cmsService, quizService);
  }

  @Test
  public void requestFinishedEventScoresNoLiveQuizzes() {

    when(quizService.findLiveQuizzes()).thenReturn(Collections.emptyList());

    eventDetailsService.requestEventDetails();

    verify(ssService, never()).getEventDetails(any());
    verify(cmsService, never()).updateQuizEventDetails(anyString(), any());
  }

  @Test
  public void testEventDetailsNullFilter() {
    QuizDto quiz = factory.manufacturePojo(QuizDto.class);
    quiz.setEventDetails(null);

    when(quizService.findLiveQuizzes()).thenReturn(Collections.singletonList(quiz));

    eventDetailsService.requestEventDetails();

    verify(ssService, never()).getEventDetails(any());
    verify(cmsService, never()).updateQuizEventDetails(anyString(), any());
  }

  @Test
  public void testQuizWithoutEvent() {
    QuizDto quiz = factory.manufacturePojo(QuizDto.class);
    quiz.getEventDetails().setEventId(null);

    when(quizService.findLiveQuizzes()).thenReturn(Collections.singletonList(quiz));

    eventDetailsService.requestEventDetails();

    verify(ssService, never()).getEventDetails(any());
    verify(cmsService, never()).updateQuizEventDetails(anyString(), any());
  }

  @Test
  public void testQuizWithEventIDWithoutStartTimeWithoutScoresAndNotFinishedEvent() {
    QuizDto quiz = factory.manufacturePojo(QuizDto.class);
    quiz.getEventDetails().setEventId("1234567");
    quiz.getEventDetails().setStartTime(null);
    quiz.getEventDetails().setActualScores(null);

    when(quizService.findLiveQuizzes()).thenReturn(Collections.singletonList(quiz));
    when(ssService.getEventDetails("1234567")).thenReturn(Optional.of(new Event()));

    eventDetailsService.requestEventDetails();

    verify(cmsService, times(1)).updateQuizEventDetails(anyString(), any());
  }

  @Test
  public void testQuizWithEventIDWithStartTimeWithoutScoresWithEventFinished() {
    QuizDto quiz = factory.manufacturePojo(QuizDto.class);
    quiz.getEventDetails().setEventId("1234567");
    quiz.getEventDetails().setStartTime("2019-10-09T13:30:00Z");
    quiz.getEventDetails().setActualScores(null);

    when(quizService.findLiveQuizzes()).thenReturn(Collections.singletonList(quiz));

    eventDetailsService.requestEventDetails();

    verify(cmsService, never()).updateQuizEventDetails(anyString(), any());
  }

  @Test
  public void testQuizWithEventDetailsFilled() {
    
    eventDetailsService.requestEventDetails();

    verify(ssService, never()).getEventDetails(any());
    verify(cmsService, never()).updateQuizEventDetails(anyString(), any());
  }

  @Test
  public void testMathcFinished() {
    QuizDto quiz = factory.manufacturePojo(QuizDto.class);
    quiz.getEventDetails().setEventId("1234567");
    quiz.getEventDetails().setStartTime("2019-10-09T13:30:00Z");
    quiz.getEventDetails().setActualScores(Collections.emptyList());
    
    when(quizService.findLiveQuizzes()).thenReturn(Collections.singletonList(quiz));
    when(ssService.getEventDetails("1234567")).thenReturn(Optional.of(new Event()));
    when(ssService.isMatchFinished(any())).thenReturn(true);
    
    eventDetailsService.requestEventDetails();
    
    verify(ssService, times(1)).getEventDetails("1234567");
    verify(ssService, times(1)).isMatchFinished(any());
    verify(ssService, times(1)).findScoresForEvent(any());
    verify(cmsService, times(1)).updateQuizEventDetails(anyString(), any());
  }
}
