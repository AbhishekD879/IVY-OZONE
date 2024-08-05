package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.configuration.ModelMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.crm.CrmServiceImpl;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AnswerDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDto;
import com.ladbrokescoral.oxygen.questionengine.dto.crm.CoinResponse;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserAnswerDto;
import com.ladbrokescoral.oxygen.questionengine.exception.NotFoundException;
import com.ladbrokescoral.oxygen.questionengine.exception.QuizSubmissionException;
import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;
import com.ladbrokescoral.oxygen.questionengine.model.cms.PredefinedAnswer;
import com.ladbrokescoral.oxygen.questionengine.repository.UserAnswerRepository;
import com.ladbrokescoral.oxygen.questionengine.service.QuizHistoryService;
import com.ladbrokescoral.oxygen.questionengine.service.QuizRewardService;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.util.TestUtils;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import reactor.core.publisher.Mono;
import uk.co.jemos.podam.api.PodamFactory;
import uk.co.jemos.podam.api.PodamFactoryImpl;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.mockito.Mockito.times;

@RunWith(MockitoJUnitRunner.class)
public class UserAnswerServiceImplTest {

    private static final String SOURCE_ID = "/123";
    private static final String ID = "12345";
    @Mock
    private QuizHistoryService historyService;

    @Mock
    private QuizService quizService;

    @Mock
    private UserAnswerRepository repository;

    @Mock
    private QuizRewardService rewardService;

    @Rule
    public ExpectedException thrown = ExpectedException.none();

    private UserAnswerServiceImpl userAnswerService;

    private PodamFactory factory = new PodamFactoryImpl();
    @Mock
    CrmServiceImpl crmService;

    @Before
    public void setUp() {
        userAnswerService = new UserAnswerServiceImpl(quizService, repository, ModelMapperFactory.getInstance(), rewardService, crmService);
    }

    @Test
    public void findById() {

        UserAnswer.Id userAnswerId = new UserAnswer.Id("testQuiz", "test");
        UserAnswer foundUA = factory.manufacturePojo(UserAnswer.class);

        when(repository.findById(userAnswerId)).thenReturn(Optional.of(foundUA));

        UserAnswerDto result = userAnswerService.getById(userAnswerId);

        assertNotNull(result);

    }

    @Test
    public void testfindById() {

        UserAnswer.Id userAnswerId = new UserAnswer.Id("testQuiz", "test");
        UserAnswer foundUA = factory.manufacturePojo(UserAnswer.class);

        when(repository.findById(userAnswerId)).thenReturn(Optional.of(foundUA));

        Optional<UserAnswerDto> result = userAnswerService.findById(userAnswerId);

        assertNotNull(result);

    }

    @Test(expected = NotFoundException.class)
    public void findByIdNotExists() {

        UserAnswer.Id userAnswerId = new UserAnswer.Id("testQuiz", "test");

        when(repository.findById(userAnswerId)).thenReturn(Optional.empty());

        userAnswerService.getById(userAnswerId);
    }

    @Test
    public void findByQuizIdOrderByCreatedDateDescTest() {
        List<UserAnswer> userAnswers = new ArrayList<>();
        UserAnswer answer = new UserAnswer();
        answer.setQuizId("234dsfdsfdsf");
        userAnswers.add(answer);
        when(repository.findByQuizIdOrderByCreatedDateDesc(any())).thenReturn(userAnswers);
        userAnswers = userAnswerService.findByQuizIdOrderByCreatedDateDesc("adfsdt343dsfdsf");
        assertNotNull(userAnswers);
    }

    @Test
    public void save() {
        AppQuizHistoryDto quizHistory = getQuizHistory();
        quizHistory.getLive().setEntryDeadline(Instant.now().plus(1, ChronoUnit.DAYS));
        CoinResponse coinResponse = new CoinResponse();
        coinResponse.setRewardErrorCode("ER000");
        when(crmService.getAward(any())).thenReturn("Success");
        when(quizService.findLiveQuiz(any())).thenReturn(Optional.of(quizHistory.getLive()));
        when(repository.findById(any())).thenReturn(Optional.empty());
        UserAnswer userAnswer = factory.manufacturePojo(UserAnswer.class);
        when((repository.save(any()))).thenReturn(userAnswer);

        UserAnswerDto result = userAnswerService.save(getQuizSubmitModel().setQuestionIdToAnswerId(quizHistory.getLive().getFirstQuestion()
                .flatten()
                .collect(Collectors.toMap(QuestionDto::getId, question -> question.getAnswers()
                        .stream()
                        .findAny()
                        .map(AnswerDto::getId)
                        .map(Collections::singletonList)
                        .get())
                )
        ));

        assertNotNull(result);
        assertEquals(userAnswer.getQuizId(), result.getQuizId());
        assertEquals(userAnswer.getUsername(), result.getUsername());

    }

    @Test
    public void saveNullLive() {
        AppQuizHistoryDto quizHistory = getQuizHistory();
        quizHistory.setLive(null);

        thrown.expect(QuizSubmissionException.class);
        thrown.expectMessage("You are trying to submit quiz that is no longer in live");

        userAnswerService.save(getQuizSubmitModel());

    }

    @Test
    public void saveDoNotShowAgain() {
        // validation is skipped for that case and quiz submit data is saved
        Map<String, List<String>> answersMap = new HashMap<String, List<String>>() {{
            put(PredefinedAnswer.DO_NOT_SHOW_AGAIN.name(), Arrays.asList("NOT_SHOW_AGAIN"));
        }};
        QuizSubmitDto quizSubmitDto = getQuizSubmitModel()
                .setQuestionIdToAnswerId(answersMap);
        when(repository.save(any())).thenReturn(new UserAnswer());
        CoinResponse coinResponse = new CoinResponse();
        coinResponse.setRewardErrorCode("ER099");
        when(crmService.getAward(quizSubmitDto)).thenReturn("Success");
        userAnswerService.save(quizSubmitDto);

        verify(repository, times(1)).save(any(UserAnswer.class));
    }

    @Test
    public void saveDoNotShowAgain_getAward() {
        // validation is skipped for that case and quiz submit data is saved
        Map<String, List<String>> answersMap = new HashMap<String, List<String>>() {{
            put(PredefinedAnswer.DO_NOT_SHOW_AGAIN.name(), Arrays.asList("NOT_SHOW_AGAIN"));
        }};
        QuizSubmitDto quizSubmitDto = getQuizSubmitModel()
                .setQuestionIdToAnswerId(answersMap);
        when(repository.save(any())).thenReturn(new UserAnswer());
        CoinResponse coinResponse = new CoinResponse();
        when(crmService.getAward(quizSubmitDto)).thenReturn("Success");
        userAnswerService.save(quizSubmitDto);

        verify(repository, times(1)).save(any(UserAnswer.class));
    }

    @Test
    public void saveDifferentQuizIds() {
        thrown.expect(QuizSubmissionException.class);
        thrown.expectMessage("You are trying to submit quiz that is no longer in live");

        userAnswerService.save(getQuizSubmitModel().setQuizId("123"));

    }

    @Test
    public void saveMissedDeadline() {
        AppQuizHistoryDto quizHistory = getQuizHistory();
        quizHistory.getLive().setEntryDeadline(Instant.now().minus(1, ChronoUnit.DAYS));

        when(quizService.findLiveQuiz(any())).thenReturn(Optional.of(quizHistory.getLive()));
        when(repository.findById(any())).thenReturn(Optional.empty());

        thrown.expect(QuizSubmissionException.class);
        thrown.expectMessage("Sorry, deadline for quiz submission is over");

        userAnswerService.save(getQuizSubmitModel());
    }

    @Test
    public void saveUserAnswersExist() {
        AppQuizHistoryDto quizHistory = getQuizHistory();
        quizHistory.getLive().setEntryDeadline(Instant.now().plus(1, ChronoUnit.DAYS));

        when(quizService.findLiveQuiz(any())).thenReturn(Optional.of(quizHistory.getLive()));
        when(repository.findById(any())).thenReturn(Optional.of(getUserAnswer()));

        thrown.expect(QuizSubmissionException.class);
        thrown.expectMessage("Quiz has already been submitted");

        userAnswerService.save(getQuizSubmitModel());
    }

    private QuizSubmitDto getQuizSubmitModel() {
        return factory.manufacturePojo(QuizSubmitDto.class)
                .setQuizId(ID)
                .setSourceId(SOURCE_ID);
    }

    @Test
    public void saveQuestionToAnswerIdDoesNotMatch() {
        AppQuizHistoryDto quizHistory = getQuizHistory();
        quizHistory.getLive().setEntryDeadline(Instant.now().plus(1, ChronoUnit.DAYS));

        when(quizService.findLiveQuiz(any())).thenReturn(Optional.of(quizHistory.getLive()));
        when(repository.findById(any())).thenReturn(Optional.empty());

        thrown.expect(QuizSubmissionException.class);
        thrown.expectMessage("Submitted answers do not match to the ones configured in CMS");

        userAnswerService.save(getQuizSubmitModel());
    }

    private AppQuizHistoryDto getQuizHistory() {
        AppQuizHistoryDto quizHistory = factory.manufacturePojo(AppQuizHistoryDto.class);

        TestUtils.buildTree(quizHistory.getLive().getFirstQuestion());
        quizHistory.setPreviousCount(5);
        quizHistory.getLive()
                .setId(ID)
                .firstQuestion()
                .setId("1");

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
