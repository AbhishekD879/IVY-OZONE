package com.ladbrokescoral.oxygen.questionengine.internal.impl;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.questionengine.exception.NotFoundException;
import com.ladbrokescoral.oxygen.questionengine.internal.SportCollarDataMigration;
import com.ladbrokescoral.oxygen.questionengine.internal.SportCollarDataMigrationObjectMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Question;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.repository.UserAnswerRepository;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryEntries;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import com.ladbrokescoral.oxygen.questionengine.util.Utils;
import io.vavr.Tuple;
import io.vavr.Tuple2;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.time.Instant;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Spliterator;
import java.util.stream.Collectors;

@Component
@Slf4j
@RequiredArgsConstructor
public class SportCollarDataMigrationImpl implements SportCollarDataMigration {
  private static final String ALL_NEW_LINES_BUT_LAST = "(\n)(?!$)";
  private static final String PREDICTION_SEPARATOR = ";";
  private static final int BATCH_SIZE = 15_000;

  private final ObjectMapper mapper = SportCollarDataMigrationObjectMapperFactory.getInstance();
  private final CmsService cmsService;
  private final UserAnswerRepository userAnswerRepository;

  @Override
  public void migrate(String quizId, MultipartFile data) throws IOException {
    Quiz quiz = cmsService.findQuizById(quizId).orElseThrow(() -> new NotFoundException("No Quiz with id '%s found'", quizId));

    log.info("Starting data migration for Quiz '{}' with id '{}'", quiz.getTitle(), quiz.getId());

    List<BigQueryEntries> entries = toEntries(data);
    List<UserAnswer> answers = entries.stream()
        .map(entry -> toUserAnswer(quiz, entry))
        .collect(Collectors.toList());

    long recordsUpdated = Utils.splitIntoBatches(answers, BATCH_SIZE)
        .stream()
        .map(userAnswerRepository::saveAll)
        .map(Iterable::spliterator)
        .mapToLong(Spliterator::getExactSizeIfKnown)
        .sum();

    log.info("Finished data migration for Quiz '{}' with id '{}'. Total User Entries migrated: {}", quiz.getTitle(), quiz.getId(), recordsUpdated);
  }

  private List<BigQueryEntries> toEntries(MultipartFile data) throws IOException {
    return mapper.readValue(formatToArray(data), new TypeReference<List<BigQueryEntries>>() {});
  }

  private UserAnswer toUserAnswer(Quiz quiz, BigQueryEntries entries) {
    List<Question> questions = quiz.getFirstQuestion().flatten().collect(Collectors.toList());
    Map<String, List<String>> questionIdToAnswerId = Arrays.stream(entries.getPredictions().split(PREDICTION_SEPARATOR))
        .map(prediction -> Tuple.of(
            questions.get(questionIndex(prediction)).getId(),
            questions.get(questionIndex(prediction)).getAnswers().get(answerIndex(prediction)).getId())
        )
        .collect(Collectors.toMap(Tuple2::_1, questionIdByAnswerId -> Collections.singletonList(questionIdByAnswerId._2)));

    return new UserAnswer()
        .setQuizId(quiz.getId())
        .setUsername(entries.getUsername())
        .setUsernameSourceId(entries.getUsername() + quiz.getSourceId())
        .setCreatedDate(entries.getCreatedDate())
        .setModifiedDate(Instant.now())
        .setQuestionIdToAnswerId(questionIdToAnswerId);
  }

  private int questionIndex(String prediction) {
    return Character.getNumericValue(prediction.charAt(0)) - 1;
  }

  private int answerIndex(String prediction) {
    return Utils.fromAlphabeticRepresentation(prediction.charAt(1));
  }

  private String formatToArray(MultipartFile data) throws IOException {
    return "["
        + new String(data.getBytes()).replaceAll(ALL_NEW_LINES_BUT_LAST, ",")
        + "]";
  }
}
