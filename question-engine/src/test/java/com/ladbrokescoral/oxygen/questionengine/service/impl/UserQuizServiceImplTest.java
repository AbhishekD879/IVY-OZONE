package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.configuration.ModelMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserQuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;
import com.ladbrokescoral.oxygen.questionengine.model.UserQuizSearchParams;
import com.ladbrokescoral.oxygen.questionengine.repository.UserAnswerRepository;
import com.ladbrokescoral.oxygen.questionengine.service.QuizHistoryService;
import com.ladbrokescoral.oxygen.questionengine.service.UpsellService;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import uk.co.jemos.podam.api.PodamFactory;
import uk.co.jemos.podam.api.PodamFactoryImpl;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@RunWith(MockitoJUnitRunner.class)
public class UserQuizServiceImplTest {
  private static final int HISTORY_PREVIOUS_LIMIT = 5;

  @Mock
  private QuizHistoryService historyService;

  @Mock
  private UserAnswerRepository userAnswerRepository;

  @Mock
  private UpsellService upsellService;

  private PodamFactory factory = new PodamFactoryImpl();

  @Spy
  private ModelMapper modelMapper = ModelMapperFactory.getInstance();

  @InjectMocks
  private UserQuizServiceImpl service;

  @Before
  public void setUp() throws Exception {
    when(upsellService.findUpsellFor(any())).thenReturn(Optional.empty());
  }

  @Test
  public void findUserQuizWithAnswers() {
    AppQuizHistoryDto quizHistory = getQuizHistory();
    quizHistory.getLive().setId("12345");
    UserAnswer userAnswer = getUserAnswer();
    userAnswer.setQuizId("12345");

    when(historyService.findQuizHistory("/123")).thenReturn(quizHistory);
    when(userAnswerRepository.findById(any())).thenReturn(Optional.of(userAnswer));
    when(userAnswerRepository.findByUsernameSourceIdOrderedByCreatedDateDesc(any())).thenReturn(Collections.singletonList(userAnswer));

    UserQuizHistoryDto userQuizWithAnswers = service.findUserHistory(new UserQuizSearchParams("testUser", "/123"), HISTORY_PREVIOUS_LIMIT);

    assertEquals(0, userQuizWithAnswers.getPreviousCount());
    assertNotNull(userQuizWithAnswers.getLive());
  }

  @Test
  public void findUserQuizWithNoLive() {
    AppQuizHistoryDto quizHistory = getQuizHistory();
    quizHistory.setLive(null);
    UserAnswer userAnswer = getUserAnswer();
    userAnswer.setQuizId("12345");

    when(historyService.findQuizHistory("/123")).thenReturn(quizHistory);
    when(userAnswerRepository.findByUsernameSourceIdOrderedByCreatedDateDesc(any())).thenReturn(Collections.singletonList(userAnswer));

    UserQuizHistoryDto userQuizWithAnswers = service.findUserHistory(new UserQuizSearchParams("testUser", "/123"), HISTORY_PREVIOUS_LIMIT);

    assertEquals(1, userQuizWithAnswers.getPreviousCount());
    
    verify(userAnswerRepository, never()).findById(any());
  }

  @Test
  public void findUserQuizWithAnswersNoAnswers() {
    AppQuizHistoryDto quizHistory = getQuizHistory();
    quizHistory.getLive().setId("12345");

    when(historyService.findQuizHistory("/123")).thenReturn(quizHistory);
    when(userAnswerRepository.findById(any())).thenReturn(Optional.empty());
    when(userAnswerRepository.findByUsernameSourceIdOrderedByCreatedDateDesc(any())).thenReturn(Collections.emptyList());

    UserQuizHistoryDto userQuizWithAnswers = service.findUserHistory(new UserQuizSearchParams("testUser", "/123"), HISTORY_PREVIOUS_LIMIT);

    assertEquals(0, userQuizWithAnswers.getPreviousCount());
    assertNotNull(userQuizWithAnswers.getLive());
  }

  @Test
  public void findLiveQuiz() {
    AppQuizHistoryDto quizHistory = getQuizHistory();
    quizHistory.getLive().setId("12345");

    UserAnswer userAnswer = getUserAnswer();
    userAnswer.setQuizId("12345");
    
    when(historyService.findQuizHistory("/123")).thenReturn(quizHistory);
    when(userAnswerRepository.findById(any())).thenReturn(Optional.of(userAnswer));

    Optional<UserQuizDto> liveQuiz = service.findLiveQuiz(new UserQuizSearchParams("testUser", "/123"));

    assertTrue(liveQuiz.isPresent());
    assertEquals("12345", liveQuiz.get().getId());
  }
  

  private AppQuizHistoryDto getQuizHistory() {
    AppQuizHistoryDto quizHistory = factory.manufacturePojo(AppQuizHistoryDto.class);

    quizHistory.setPreviousCount(5);
    quizHistory.getLive().firstQuestion().setId("1");

    return quizHistory;
  }

  private UserAnswer getUserAnswer() {
    UserAnswer userAnswer = factory.manufacturePojo(UserAnswer.class);

    Map<String, List<String>> questionIdToAnswerId = new HashMap<>();
    questionIdToAnswerId.put("1", Collections.emptyList());
    userAnswer.setQuestionIdToAnswerId(questionIdToAnswerId);
    return userAnswer;
  }
}
