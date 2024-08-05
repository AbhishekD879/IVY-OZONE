package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.google.common.collect.ImmutableMap;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AnswerDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.EventDetailsDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.BigQueryEntriesTable;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.BigQueryQuestionsTable;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.BigQueryResultsTable;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryEntries;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryGameId;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryQuestions;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryResults;
import com.ladbrokescoral.oxygen.questionengine.util.Utils;
import io.vavr.Tuple2;
import io.vavr.collection.HashMap;
import io.vavr.collection.Stream;
import org.apache.commons.lang3.RandomStringUtils;
import org.apache.commons.lang3.RandomUtils;
import org.assertj.core.api.InstanceOfAssertFactories;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import uk.co.jemos.podam.api.PodamFactory;
import uk.co.jemos.podam.api.PodamFactoryImpl;

import java.io.IOException;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@RunWith(MockitoJUnitRunner.class)
public class BigQueryStreamingServiceImplTest {
  private final String brand = "test";
  private final PodamFactory factory = new PodamFactoryImpl();

  @Mock
  private BigQueryQuestionsTable questionsTable;

  @Mock
  private BigQueryEntriesTable entriesTable;

  @Mock
  private BigQueryResultsTable resultsTable;

  @Mock
  private QuizService quizService;

  @Mock
  private ApplicationProperties properties;

  @Captor
  private ArgumentCaptor<List<BigQueryEntries>> entriesCaptor;

  @Captor
  private ArgumentCaptor<List<BigQueryQuestions>> questionsCaptor;

  @Captor
  private ArgumentCaptor<List<BigQueryResults>> resultsCaptor;

  @InjectMocks
  private BigQueryStreamingServiceImpl bigQueryStreamingService;

  @Before
  public void setUp() {
    when(properties.getBrand()).thenReturn(brand);
  }

  @Test
  public void streamUserEntryHappyPath() throws IOException {
    String sourceId = "/test/app";
    QuestionDto questionTree = initQuestionTree(4);
    QuizDto quiz = new QuizDto().setFirstQuestion(questionTree);

    quiz.setSourceId(sourceId)
        .setId(UUID.randomUUID().toString())
        .setSourceId(sourceId)
        .setDisplayFrom(Instant.now())
        .setEntryDeadline(Instant.now().minus(3, ChronoUnit.DAYS))
        .setEventDetails(new EventDetailsDto()
            .setEventName("HomeTeam vs AwayTeam")
            .setEventId(String.valueOf(RandomUtils.nextLong(1000000, 99999999)))
        );

    QuizSubmitDto submission = factory.manufacturePojo(QuizSubmitDto.class)
        .setSourceId(sourceId)
        .setUsername(RandomStringUtils.randomAlphanumeric(10))
        .setCustomerId(String.valueOf(RandomUtils.nextLong(1000000, 99999999)))
        .setQuizId(quiz.getId())
        .setQuestionIdToAnswerId(ImmutableMap.of(
            "q1", Collections.singletonList("a1-3"),
            "q2", Collections.singletonList("a2-1"),
            "q3", Collections.singletonList("a3-2"),
            "q4", Collections.singletonList("a4-4")
        ));

    when(quizService.findLiveQuiz(sourceId)).thenReturn(Optional.of(quiz));
    doNothing()
        .when(entriesTable)
        .insertAll(entriesCaptor.capture());
    bigQueryStreamingService.streamUserEntry(submission);

    List<BigQueryEntries> actual = entriesCaptor.getValue();
    assertThat(actual).asList()
        .hasSize(1)
        .first()
        .asInstanceOf(InstanceOfAssertFactories.type(BigQueryEntries.class))
        .matches(entries -> entries.getCustomerId().equals(submission.getCustomerId()), "Customer Id to match")
        .matches(entries -> entries.getUsername().equals(submission.getUsername()), "Username to match")
        .matches(entries -> entries.getEventId().equals(quiz.getEventDetails().getEventId()), "Event Id to match")
        .matches(entries -> entries.getGame().equals(submission.getSourceId()), "Source Id to match")
        .matches(entries -> entries.getBrand().equals(brand), "Brand Id to match")
        .matches(entries -> entries.getCreatedDate() != null, "Created Date to not be null")
        .matches(entries -> entries.getGameStartDate().equals(quiz.getDisplayFrom().truncatedTo(ChronoUnit.SECONDS)), "Game Start Date to match")
        .matches(entries -> entries.getGameEndDate().equals(quiz.getEntryDeadline().truncatedTo(ChronoUnit.SECONDS)), "Game Emd Date to match")
        .matches(entries -> entries.getGameId().equals(quiz.getId()), "Game Id Date to match")
        .matches(entries -> entries.getPredictions().equals("1C;2A;3B;4D"), "User Predictions to match");
  }

  @Test
  public void streamUserEntryNoEventDetails() throws IOException {
    String sourceId = "/test/app";
    QuestionDto questionTree = initQuestionTree(3);
    QuizDto quiz = new QuizDto().setFirstQuestion(questionTree);

    quiz.setSourceId(sourceId)
        .setId(UUID.randomUUID().toString())
        .setSourceId(sourceId)
        .setDisplayFrom(Instant.now())
        .setEntryDeadline(Instant.now().minus(3, ChronoUnit.DAYS));

    QuizSubmitDto submission = factory.manufacturePojo(QuizSubmitDto.class)
        .setSourceId(sourceId)
        .setUsername(RandomStringUtils.randomAlphanumeric(10))
        .setCustomerId(String.valueOf(RandomUtils.nextLong(1000000, 99999999)))
        .setQuizId(quiz.getId())
        .setQuestionIdToAnswerId(ImmutableMap.of(
            "q1", Collections.singletonList("a1-2"),
            "q2", Collections.singletonList("a2-2"),
            "q3", Collections.singletonList("a3-1")
        ));

    when(quizService.findLiveQuiz(sourceId)).thenReturn(Optional.of(quiz));
    doNothing()
        .when(entriesTable)
        .insertAll(entriesCaptor.capture());
    bigQueryStreamingService.streamUserEntry(submission);

    List<BigQueryEntries> actual = entriesCaptor.getValue();
    assertThat(actual).asList()
        .hasSize(1)
        .first()
        .asInstanceOf(InstanceOfAssertFactories.type(BigQueryEntries.class))
        .matches(entries -> entries.getCustomerId().equals(submission.getCustomerId()), "Customer Id to match")
        .matches(entries -> entries.getUsername().equals(submission.getUsername()), "Username to match")
        .matches(entries -> entries.getEventId() == null, "Event Id to be null")
        .matches(entries -> entries.getGame().equals(submission.getSourceId()), "Source Id to match")
        .matches(entries -> entries.getBrand().equals(brand), "Brand Id to match")
        .matches(entries -> entries.getCreatedDate() != null, "Created Date to not be null")
        .matches(entries -> entries.getGameStartDate().equals(quiz.getDisplayFrom().truncatedTo(ChronoUnit.SECONDS)), "Game Start Date to match")
        .matches(entries -> entries.getGameEndDate().equals(quiz.getEntryDeadline().truncatedTo(ChronoUnit.SECONDS)), "Game End Date to match")
        .matches(entries -> entries.getGameId().equals(quiz.getId()), "Game Id Date to match")
        .matches(entries -> entries.getPredictions().equals("1B;2B;3A"), "User Predictions to match");
  }

  @Test(expected = IllegalStateException.class)
  public void streamUserEntryNoLiveQuiz() throws IOException {
    bigQueryStreamingService.streamUserEntry(new QuizSubmitDto());
  }

  @Test
  public void steamCmsConfigurationHappyPath() throws IOException {
    int depth = 4;
    String sourceId = "/test/app";
    QuestionDto questionTree = initQuestionTree(depth);
    QuizDto quiz = new QuizDto().setFirstQuestion(questionTree);

    quiz.setSourceId(sourceId)
        .setId(UUID.randomUUID().toString())
        .setSourceId(sourceId)
        .setDisplayFrom(Instant.now().minus(7, ChronoUnit.DAYS))
        .setEntryDeadline(Instant.now().minus(1, ChronoUnit.DAYS))
        .setEventDetails(new EventDetailsDto()
            .setEventName("HomeTeam vs AwayTeam")
            .setEventId(String.valueOf(RandomUtils.nextLong(1000000, 99999999)))

        );

    when(quizService.findLiveQuizzes()).thenReturn(Collections.singletonList(quiz));
    when(questionsTable.read(new BigQueryGameId(quiz.getId()))).thenReturn(Collections.emptyList());
    doNothing()
        .when(questionsTable)
        .insertAll(questionsCaptor.capture());

    bigQueryStreamingService.streamCmsConfiguration();

    List<BigQueryQuestions> actual = questionsCaptor.getValue();
    List<QuestionDto> expectedQuestions = questionTree.flatten().collect(Collectors.toList());
    AnswerDto[][] expectedAnswersMatrix = new AnswerDto[depth][depth];
    Stream.ofAll(expectedQuestions)
        .zipWithIndex()
        .forEach(questionByIndex -> Stream.ofAll(questionByIndex._1.getAnswers())
            .zipWithIndex()
            .forEach(answerByIndex -> expectedAnswersMatrix[questionByIndex._2][answerByIndex._2] = answerByIndex._1)
        );

    assertThat(actual).asList().hasSize(16);
    Stream.ofAll(actual)
        .zipWithIndex((questions, index) -> new Object() {
          final int questionIndex = questionIndex(index, depth);
          final int answerIndex = answerIndex(index, depth);
          final BigQueryQuestions actual = questions;
        })
        .forEach(actualByIndexes -> assertThat(actualByIndexes.actual)
            .matches(questions -> questions.getQuestionNumber().equals(actualByIndexes.questionIndex + 1), "Question Number to match")
            .matches(questions -> questions.getQuestionText().equals(expectedQuestions.get(actualByIndexes.questionIndex).getText()), "Question Text to match")
            .matches(questions -> questions.getAnswerOption().equals(Utils.toAlphabeticRepresentation(actualByIndexes.answerIndex)), "Answer Option to match")
            .matches(questions -> questions.getAnswerText().equals(expectedAnswersMatrix[actualByIndexes.questionIndex][actualByIndexes.answerIndex].getText()), "Answer Text to match")
            .matches(questions -> questions.getEventName().equals("HomeTeam vs AwayTeam"), "Event Name to match")
            .matches(questions -> questions.getGameStartDate().equals(quiz.getDisplayFrom().truncatedTo(ChronoUnit.SECONDS)), "Game Start Date to match")
            .matches(questions -> questions.getGameEndDate().equals(quiz.getEntryDeadline().truncatedTo(ChronoUnit.SECONDS)), "Game End Date to match")
            .matches(questions -> questions.getBrand().equals(brand), "Brand Id to match")
            .matches(questions -> questions.getUploadedDate() != null, "Uploaded Date to not be null")
            .matches(questions -> questions.getGame().equals(quiz.getSourceId()), "Source Id to match")
            .matches(questions -> questions.getGameId().equals(quiz.getId()), "Quiz Id to match")
        );
  }

  @Test
  public void steamCmsConfigurationExistingQueryFails() throws IOException {
    int depth = 4;
    String sourceId = "/test/app";
    QuestionDto questionTree = initQuestionTree(depth);
    QuizDto quiz = new QuizDto().setFirstQuestion(questionTree);

    quiz.setSourceId(sourceId)
        .setId(UUID.randomUUID().toString())
        .setSourceId(sourceId)
        .setDisplayFrom(Instant.now().minus(7, ChronoUnit.DAYS))
        .setEntryDeadline(Instant.now().minus(1, ChronoUnit.DAYS))
        .setEventDetails(new EventDetailsDto()
            .setEventName("HomeTeam vs AwayTeam")
            .setEventId(String.valueOf(RandomUtils.nextLong(1000000, 99999999)))
        );

    when(quizService.findLiveQuizzes()).thenReturn(Collections.singletonList(quiz));
    when(questionsTable.read(new BigQueryGameId(quiz.getId()))).thenThrow(IllegalStateException.class);
    doNothing()
        .when(questionsTable)
        .insertAll(questionsCaptor.capture());

    bigQueryStreamingService.streamCmsConfiguration();

    List<BigQueryQuestions> actual = questionsCaptor.getValue();
    List<QuestionDto> expectedQuestions = questionTree.flatten().collect(Collectors.toList());
    AnswerDto[][] expectedAnswersMatrix = new AnswerDto[depth][depth];
    Stream.ofAll(expectedQuestions)
        .zipWithIndex()
        .forEach(questionByIndex -> Stream.ofAll(questionByIndex._1.getAnswers())
            .zipWithIndex()
            .forEach(answerByIndex -> expectedAnswersMatrix[questionByIndex._2][answerByIndex._2] = answerByIndex._1)
        );

    assertThat(actual).asList().hasSize(16);
    Stream.ofAll(actual)
        .zipWithIndex((questions, index) -> new Object() {
          final int questionIndex = questionIndex(index, depth);
          final int answerIndex = answerIndex(index, depth);
          final BigQueryQuestions actual = questions;
        })
        .forEach(actualByIndexes -> assertThat(actualByIndexes.actual)
            .matches(questions -> questions.getQuestionNumber().equals(actualByIndexes.questionIndex + 1), "Question Number to match")
            .matches(questions -> questions.getQuestionText().equals(expectedQuestions.get(actualByIndexes.questionIndex).getText()), "Question Text to match")
            .matches(questions -> questions.getAnswerOption().equals(Utils.toAlphabeticRepresentation(actualByIndexes.answerIndex)), "Answer Option to match")
            .matches(questions -> questions.getAnswerText().equals(expectedAnswersMatrix[actualByIndexes.questionIndex][actualByIndexes.answerIndex].getText()), "Answer Text to match")
            .matches(questions -> questions.getEventName().equals("HomeTeam vs AwayTeam"), "Event Name to match")
            .matches(questions -> questions.getGameStartDate().equals(quiz.getDisplayFrom().truncatedTo(ChronoUnit.SECONDS)), "Game Start Date to match")
            .matches(questions -> questions.getGameEndDate().equals(quiz.getEntryDeadline().truncatedTo(ChronoUnit.SECONDS)), "Game End Date to match")
            .matches(questions -> questions.getBrand().equals(brand), "Brand Id to match")
            .matches(questions -> questions.getUploadedDate() != null, "Uploaded Date to not be null")
            .matches(questions -> questions.getGame().equals(quiz.getSourceId()), "Source Id to match")
            .matches(questions -> questions.getGameId().equals(quiz.getId()), "Quiz Id to match")
        );
  }

  @Test
  public void steamCmsConfigurationAlreadyExist() throws IOException {
    int depth = 5;
    String sourceId = "/test/app";
    QuestionDto questionTree = initQuestionTree(depth);
    QuizDto quiz = new QuizDto().setFirstQuestion(questionTree);

    quiz.setSourceId(sourceId)
        .setId(UUID.randomUUID().toString())
        .setSourceId(sourceId)
        .setDisplayFrom(Instant.now().minus(7, ChronoUnit.DAYS))
        .setEntryDeadline(Instant.now().minus(1, ChronoUnit.DAYS));

    List<BigQueryQuestions> existing = Stream.ofAll(questionTree.flatten())
        .zipWithIndex()
        .flatMap(questionByIndex -> Stream.ofAll(questionByIndex._1.getAnswers())
            .zipWithIndex()
            .map(answerByIndex -> new BigQueryQuestions()
                .setQuestionNumber(questionByIndex._2 + 1)
                .setQuestionText(questionByIndex._1.getText())
                .setAnswerOption(Utils.toAlphabeticRepresentation(answerByIndex._2))
                .setAnswerText(answerByIndex._1.getText())
                .setGameStartDate(quiz.getDisplayFrom())
                .setGameEndDate(quiz.getEntryDeadline())
                .setBrand(brand)
                .setUploadedDate(Instant.now().minus(5, ChronoUnit.MINUTES))
                .setGame(quiz.getSourceId())
                .setGameId(quiz.getId())
            )
        )
        .collect(Collectors.toList());

    when(quizService.findLiveQuizzes()).thenReturn(Collections.singletonList(quiz));
    when(questionsTable.read(new BigQueryGameId(quiz.getId()))).thenReturn(existing);

    bigQueryStreamingService.streamCmsConfiguration();

    verify(questionsTable).insertAll(argThat(List::isEmpty));
  }

  @Test
  public void steamCmsConfigurationValuesChanged() throws IOException {
    int depth = 5;
    String sourceId = "/test/app";
    QuestionDto questionTree = initQuestionTree(depth);
    QuizDto quiz = new QuizDto().setFirstQuestion(questionTree);
    quiz.setSourceId(sourceId)
        .setId(UUID.randomUUID().toString())
        .setSourceId(sourceId)
        .setDisplayFrom(Instant.now().minus(7, ChronoUnit.DAYS))
        .setEntryDeadline(Instant.now().minus(1, ChronoUnit.DAYS))
        .setEventDetails(new EventDetailsDto()
            .setEventName("HomeTeam vs AwayTeam")
            .setEventId(String.valueOf(RandomUtils.nextLong(1000000, 99999999)))

        );
    List<BigQueryQuestions> existing = Stream.ofAll(questionTree.flatten())
        .zipWithIndex()
        .flatMap(questionByIndex -> Stream.ofAll(questionByIndex._1.getAnswers())
            .zipWithIndex()
            .map(answerByIndex -> new BigQueryQuestions()
                .setQuestionNumber(questionByIndex._2 + 1)
                .setQuestionText(questionByIndex._1.getText())
                .setAnswerOption(Utils.toAlphabeticRepresentation(answerByIndex._2))
                .setAnswerText(answerByIndex._1.getText())
                .setEventName("HomeTeam vs AwayTeam")
                .setGameStartDate(quiz.getDisplayFrom())
                .setGameEndDate(quiz.getEntryDeadline())
                .setBrand(brand)
                .setUploadedDate(Instant.now().minus(5, ChronoUnit.MINUTES))
                .setGame(quiz.getSourceId())
                .setGameId(quiz.getId())
            )
        )
        .collect(Collectors.toList());

    when(questionsTable.read(new BigQueryGameId(quiz.getId()))).thenReturn(existing);

    quiz.getEventDetails().setEventName("CHANGED HomeTeam vs AwayTeam");

    when(quizService.findLiveQuizzes()).thenReturn(Collections.singletonList(quiz));
    doNothing()
        .when(questionsTable)
        .insertAll(questionsCaptor.capture());

    bigQueryStreamingService.streamCmsConfiguration();

    List<BigQueryQuestions> actual = questionsCaptor.getValue();
    List<QuestionDto> expectedQuestions = questionTree.flatten().collect(Collectors.toList());
    AnswerDto[][] expectedAnswersMatrix = new AnswerDto[depth][depth];
    Stream.ofAll(expectedQuestions)
        .zipWithIndex()
        .forEach(questionByIndex -> Stream.ofAll(questionByIndex._1.getAnswers())
            .zipWithIndex()
            .forEach(answerByIndex -> expectedAnswersMatrix[questionByIndex._2][answerByIndex._2] = answerByIndex._1)
        );

    assertThat(actual).asList().hasSize(25);
    Stream.ofAll(actual)
        .zipWithIndex((questions, index) -> new Object() {
          final int questionIndex = questionIndex(index, depth);
          final int answerIndex = answerIndex(index, depth);
          final BigQueryQuestions actual = questions;
        })
        .forEach(actualByIndexes -> assertThat(actualByIndexes.actual)
            .matches(questions -> questions.getQuestionNumber().equals(actualByIndexes.questionIndex + 1), "Question Number to match")
            .matches(questions -> questions.getQuestionText().equals(expectedQuestions.get(actualByIndexes.questionIndex).getText()), "Question Text to match")
            .matches(questions -> questions.getAnswerOption().equals(Utils.toAlphabeticRepresentation(actualByIndexes.answerIndex)), "Answer Option to match")
            .matches(questions -> questions.getAnswerText().equals(expectedAnswersMatrix[actualByIndexes.questionIndex][actualByIndexes.answerIndex].getText()), "Answer Text to match")
            .matches(questions -> questions.getEventName().equals("CHANGED HomeTeam vs AwayTeam"), "Event Name to match")
            .matches(questions -> questions.getGameStartDate().equals(quiz.getDisplayFrom().truncatedTo(ChronoUnit.SECONDS)), "Game Start Date to match")
            .matches(questions -> questions.getGameEndDate().equals(quiz.getEntryDeadline().truncatedTo(ChronoUnit.SECONDS)), "Game End Date to match")
            .matches(questions -> questions.getBrand().equals(brand), "Brand Id to match")
            .matches(questions -> questions.getUploadedDate() != null, "Uploaded Date to not be null")
            .matches(questions -> questions.getGame().equals(quiz.getSourceId()), "Source Id to match")
            .matches(questions -> questions.getGameId().equals(quiz.getId()), "Quiz Id to match")
        );
  }

  @Test
  public void steamResultsHappyPath() throws IOException {
    int depth = 3;
    String sourceId = "/test/app";
    QuestionDto questionTree = initQuestionTree(depth);
    QuizDto quiz = new QuizDto().setFirstQuestion(questionTree);
    quiz.setSourceId(sourceId)
        .setId(UUID.randomUUID().toString())
        .setSourceId(sourceId)
        .setDisplayFrom(Instant.now().minus(7, ChronoUnit.DAYS))
        .setEntryDeadline(Instant.now().minus(1, ChronoUnit.DAYS))
        .setEventDetails(new EventDetailsDto()
            .setEventName("HomeTeam vs AwayTeam")
            .setEventId(String.valueOf(RandomUtils.nextLong(1000000, 99999999)))

        );
    Integer[] correctAnswersIndexes = Stream.ofAll(questionTree.flatten().collect(Collectors.toList()))
        .map(question -> Stream.ofAll(question.getAnswers())
            .zipWithIndex()
            .drop(RandomUtils.nextInt(0, depth))
            .peek(answerByIndex -> answerByIndex._1().setCorrectAnswer(true))
            .map(Tuple2::_2)
            .get()
        )
        .toJavaArray(Integer[]::new);

    when(resultsTable.read(new BigQueryGameId(quiz.getId()))).thenReturn(Collections.emptyList());
    when(quizService.findLiveQuizzes()).thenReturn(Collections.singletonList(quiz));
    doNothing()
        .when(resultsTable)
        .insertAll(resultsCaptor.capture());

    bigQueryStreamingService.streamResults();

    List<BigQueryResults> actual = resultsCaptor.getValue();

    assertThat(actual).asList().hasSize(depth);
    for (int i = 0; i < actual.size(); i++) {
      int questionIndex = i;

      assertThat(actual.get(i))
          .matches(questions -> questions.getQuestionNumber().equals(questionIndex + 1), "Question Number to match")
          .matches(questions -> questions.getAnswerOption().equals(Utils.toAlphabeticRepresentation(correctAnswersIndexes[questionIndex])), "Answer Option to match")
          .matches(questions -> questions.getBrand().equals(brand), "Brand Id to match")
          .matches(questions -> questions.getResultedDate() != null, "Resulted Date to not be null")
          .matches(questions -> questions.getGameId().equals(quiz.getId()), "Quiz Id to match");
    }
  }

  private QuestionDto initQuestionTree(int depth) {
    return Stream.rangeClosed(1, depth)
        .map(questionIndex -> new QuestionDto()
            .setId("q" + questionIndex)
            .setText("Question " + questionIndex)
            .setAnswers(
                Stream.rangeClosed(1, depth)
                    .map(answerIndex -> new AnswerDto()
                        .setId(String.format("a%s-%s", questionIndex, answerIndex))
                        .setText(String.format("Answer %s-%s", questionIndex, answerIndex))
                        .setQuestionAskedId("q" + questionIndex)
                    )
                    .map(AnswerDto.class::cast)
                    .collect(Collectors.toList())
            )
        )
        .map(QuestionDto.class::cast)
        .reduceRight((beforePrev, prev) -> {
          beforePrev.getAnswers().forEach(answer -> answer.setNextQuestionId(prev.getId()));
          beforePrev.setNextQuestions(HashMap.of(prev.getId(), prev).toJavaMap());

          return beforePrev;
        });
  }

  private int questionIndex(int iteration, int depth) {
    return iteration / depth;
  }

  private int answerIndex(int iteration, int depth) {
    return iteration - questionIndex(iteration, depth) * depth;
  }
}
