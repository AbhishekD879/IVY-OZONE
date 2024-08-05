package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import com.ladbrokescoral.oxygen.questionengine.dto.AbstractAnswerDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AnswerDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDetailsDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.service.BigQueryStreamingService;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.BigQueryEntriesTable;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.BigQueryQuestionsTable;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.BigQueryResultsTable;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryEntries;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryGameId;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryQuestions;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryResults;
import com.ladbrokescoral.oxygen.questionengine.util.Utils;
import io.vavr.CheckedFunction1;
import io.vavr.collection.Stream;
import io.vavr.control.Try;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.Instant;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
@Slf4j
@RequiredArgsConstructor
@ConditionalOnProperty("application.enableBigQueryStreaming")
public class BigQueryStreamingServiceImpl implements BigQueryStreamingService {
  private final BigQueryQuestionsTable questionsTable;
  private final BigQueryEntriesTable entriesTable;
  private final BigQueryResultsTable resultsTable;
  private final QuizService quizService;
  private final ApplicationProperties properties;

  @Override
  @Retryable(backoff = @Backoff(delay = 15_000))
  public void streamUserEntry(QuizSubmitDto quizSubmitDto) throws IOException {
    BigQueryEntries entries = quizService.findLiveQuiz(quizSubmitDto.getSourceId())
        .map(liveQuiz -> toEntries(quizSubmitDto, liveQuiz))
        .orElseThrow(() -> new IllegalStateException("Cannot stream user entries to BigQuery for non live Quiz. Context: " + quizSubmitDto));

    entriesTable.insertAll(Collections.singletonList(entries));
  }

  @Override
  @Retryable(backoff = @Backoff(delay = 60_000))
  public void streamCmsConfiguration() throws IOException {
    List<BigQueryQuestions> questions = Stream.ofAll(quizService.findLiveQuizzes())
        .filter(liveQuiz -> liveQuiz.getDisplayFrom().isBefore(Instant.now()))
        .flatMap(this::flattenQuiz)
        .map(this::toQuestions)
        .collect(Collectors.groupingBy(BigQueryQuestions::id))
        .entrySet()
        .stream()
        .filter(resultsById -> doesNotExistYet(resultsById.getValue(), questionsTable::read, resultsById.getKey(), BigQueryQuestions::getUploadedDate))
        .map(Map.Entry::getValue)
        .flatMap(List::stream)
        .toList();
     log.info("Before save big query Size:'{}' and Object is: '{}' " ,questions.size(), questions);
     questionsTable.insertAll(questions);
  }

  @Override
  @Retryable(backoff = @Backoff(delay = 60_000))
  public void streamResults() throws IOException {
    List<BigQueryResults> results = Stream.ofAll(quizService.findLiveQuizzes())
        .filter(liveQuiz -> liveQuiz.getEntryDeadline().isBefore(Instant.now()))
        .filter(this::isResulted)
        .flatMap(this::flattenQuiz)
        .filter(flatQuiz -> flatQuiz.answer.isCorrectAnswer())
        .map(this::toResults)
        .collect(Collectors.groupingBy(BigQueryResults::id))
        .entrySet()
        .stream()
        .filter(resultsById -> doesNotExistYet(resultsById.getValue(), resultsTable::read, resultsById.getKey(), BigQueryResults::getResultedDate))
        .map(Map.Entry::getValue)
        .flatMap(List::stream)
        .toList();
    resultsTable.insertAll(results);
  }

  private boolean isResulted(QuizDto quizDto) {
    return quizDto.getFirstQuestion().flatten()
        .allMatch(question -> question.getAnswers().stream()
            .anyMatch(AbstractAnswerDto::isCorrectAnswer)
        );
  }

  private Stream<FlatQuiz> flattenQuiz(QuizDto liveQuiz) {
    return Stream.ofAll((Iterable<? extends QuestionDto>) liveQuiz.getFirstQuestion().flatten().toList())
        .zipWithIndex()
        .flatMap(questionToItsIndex -> Stream.ofAll(questionToItsIndex._1.getAnswers())
            .zipWithIndex()
            .map(answerToItsIndex -> new FlatQuiz()
                .setQuiz(liveQuiz)
                .setQuestion(questionToItsIndex._1)
                .setQuestionNumber(questionToItsIndex._2 + 1)
                .setAnswer(answerToItsIndex._1)
                .setAnswerOption(Utils.toAlphabeticRepresentation(answerToItsIndex._2))
            )
        );
  }

  private BigQueryEntries toEntries(QuizSubmitDto quizSubmitDto, QuizDto liveQuiz) {
    return new BigQueryEntries()
        .setBrand(properties.getBrand())
        .setGameId(liveQuiz.getId())
        .setGame(liveQuiz.getSourceId())
        .setGameStartDate(liveQuiz.getDisplayFrom())
        .setGameEndDate(liveQuiz.getEntryDeadline())
        .setUsername(quizSubmitDto.getUsername())
        .setCustomerId(quizSubmitDto.getCustomerId())
        .setCreatedDate(Instant.now())
        .setEventId(liveQuiz.getEventDetails() != null ? liveQuiz.getEventDetails().getEventId() : null)
        .setPredictions(toUserPredictions(quizSubmitDto, liveQuiz));
  }

  private String toUserPredictions(QuizSubmitDto submission, QuizDto liveQuiz) {
    Map<String, String> combinedIdsToPrediction = Stream.ofAll((Iterable<? extends QuestionDto>) liveQuiz.firstQuestion().flatten().toList())
        .zipWithIndex()
        .flatMap(questionToItsIndex -> Stream.ofAll(questionToItsIndex._1.getAnswers())
            .zipWithIndex()
            .map(answerToItsIndex -> new AbstractMap.SimpleImmutableEntry<>(
                questionToItsIndex._1.getId() + answerToItsIndex._1.getId(),
                (questionToItsIndex._2 + 1) + Utils.toAlphabeticRepresentation(answerToItsIndex._2)
            ))
        )
        .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));


    return submission.getQuestionIdToAnswerId().entrySet()
        .stream()
        .map(answerIdToQuestionIds -> answerIdToQuestionIds.getKey() + String.join("", answerIdToQuestionIds.getValue()))
        .map(combinedIdsToPrediction::get)
        .collect(Collectors.joining(";"));
  }

  private BigQueryResults toResults(FlatQuiz flatQuiz) {
    return new BigQueryResults()
        .setBrand(properties.getBrand())
        .setGameId(flatQuiz.quiz.getId())
        .setGame(flatQuiz.quiz.getSourceId())
        .setQuestionNumber(flatQuiz.questionNumber)
        .setAnswerOption(flatQuiz.answerOption)
        .setResultedDate(Instant.now());
  }

  private BigQueryQuestions toQuestions(FlatQuiz flatQuiz) {
    return new BigQueryQuestions()
        .setBrand(properties.getBrand())
        .setGameId(flatQuiz.quiz.getId())
        .setGame(flatQuiz.quiz.getSourceId())
        .setGameStartDate(flatQuiz.quiz.getDisplayFrom())
        .setGameEndDate(flatQuiz.quiz.getEntryDeadline())
        .setEventName(flatQuiz.quiz.getEventDetails() != null ? flatQuiz.quiz.getEventDetails().getEventName() : null)
        .setQuestionText(flatQuiz.question.getText())
        .setQuestionNumber(flatQuiz.questionNumber)
        .setAnswerText(flatQuiz.answer.getText())
        .setAnswerOption(flatQuiz.answerOption)
        .setUploadedDate(Instant.now());
  }

  private boolean isTeamNamesConfigured(QuestionDetailsDto defaultQuestionsDetails) {
    return defaultQuestionsDetails != null
        && StringUtils.isNotBlank(defaultQuestionsDetails.getHomeTeamName())
        && StringUtils.isNotBlank(defaultQuestionsDetails.getAwayTeamName());
  }

  private <T, U extends Comparable<U>> boolean doesNotExistYet(List<T> newRecords,
                                                               CheckedFunction1<BigQueryGameId, List<T>> existingRecordsQuery,
                                                               BigQueryGameId id,
                                                               Function<T, U> sortBy) {
    List<T> existingRecords = Try.of(() -> existingRecordsQuery.apply(id))
        .onFailure(ex -> log.error("Failed to query BigQuery for Quiz '{}'. Reason: '{}'", id.get(), ex.toString()))
        .getOrElse(Collections.emptyList())
        .stream()
        .sorted(Comparator.comparing(sortBy).reversed())
        .limit(newRecords.size())
        .toList();
    log.info("existingRecords size: '{}'  Existing Object : '{}'", existingRecords.size(),existingRecords);
    boolean doesNotExist = existingRecords.size() != newRecords.size() || !newRecords.containsAll(existingRecords);
    if (!doesNotExist) {
      log.info("The following records have already been streamed to BigQuery: {}", newRecords);
    }
    return doesNotExist;
  }

  @Setter
  @Accessors(chain = true)
  private static class FlatQuiz {
    QuizDto quiz;
    QuestionDto question;
    int questionNumber;
    AnswerDto answer;
    String answerOption;
  }
}
