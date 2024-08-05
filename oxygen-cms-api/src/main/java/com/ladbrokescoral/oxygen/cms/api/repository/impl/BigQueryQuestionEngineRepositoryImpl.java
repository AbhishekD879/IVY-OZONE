package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.google.api.services.bigquery.Bigquery;
import com.google.api.services.bigquery.model.QueryParameter;
import com.google.api.services.bigquery.model.QueryParameterType;
import com.google.api.services.bigquery.model.QueryParameterValue;
import com.google.api.services.bigquery.model.QueryRequest;
import com.google.api.services.bigquery.model.QueryResponse;
import com.google.api.services.bigquery.model.TableCell;
import com.google.api.services.bigquery.model.TableRow;
import com.ladbrokescoral.oxygen.cms.api.entity.QuestionSummaryReport;
import com.ladbrokescoral.oxygen.cms.api.repository.BigQueryQuestionEngineRepository;
import com.ladbrokescoral.oxygen.cms.configuration.BigQueryProperties;
import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.ObjectUtils;

@Slf4j
@RequiredArgsConstructor
public class BigQueryQuestionEngineRepositoryImpl implements BigQueryQuestionEngineRepository {
  private final Bigquery bigquery;
  private final BigQueryProperties properties;

  @Override
  public List<QuestionSummaryReport> findQuestionSummariesByQuizId(String quizId)
      throws IOException {
    if (ObjectUtils.isEmpty(quizId)) {
      throw new IllegalArgumentException("id must not be empty");
    }

    try {
      QueryResponse response =
          bigquery
              .jobs()
              .query(
                  properties.getProjectId(),
                  new QueryRequest()
                      .setParameterMode("POSITIONAL")
                      .setQuery(
                          String.format(
                              "WITH AnswerIndex AS (\n"
                                  + "  SELECT OFFSET AS Value\n"
                                  + "  FROM UNNEST(\n"
                                  + "    (\n"
                                  + "      SELECT SPLIT(Predictions, ';') AS UserAnswer\n"
                                  + "      FROM %s.%s\n"
                                  + "      WHERE GameID = ?\n"
                                  + "      ORDER BY LENGTH(Predictions) DESC\n"
                                  + "      LIMIT 1\n"
                                  + "    )\n"
                                  + "  )"
                                  + "  WITH OFFSET\n"
                                  + ")\n"
                                  + "SELECT GameID AS QuizID,\n"
                                  + "       Game AS SourceID, \n"
                                  + "       CASE\n"
                                  + "         WHEN (LENGTH(Predictions) = 0 OR Predictions = 'null') \n"
                                  + "         THEN 0\n"
                                  + "         ELSE CAST(REGEXP_EXTRACT(SPLIT(Predictions, ';')[OFFSET(AnswerIndex.Value)], '^[0-9]+') AS NUMERIC)\n"
                                  + "         END \n"
                                  + "       AS QuestionNumber,\n"
                                  + "       CASE\n"
                                  + "         WHEN (LENGTH(Predictions) = 0 OR Predictions = 'null') \n"
                                  + "         THEN 'Chose not to take a Quiz'\n"
                                  + "         ELSE REGEXP_EXTRACT(SPLIT(Predictions, ';')[OFFSET(AnswerIndex.Value)], '[a-zA-Z]+')\n"
                                  + "         END \n"
                                  + "       AS UserOption,\n"
                                  + "       COUNTIF((LENGTH(Predictions) != 0 AND Predictions != 'null') OR AnswerIndex.Value = 0) AS NumberOfEntries\n"
                                  + "FROM %s.%s AS Entries\n"
                                  + "JOIN AnswerIndex\n"
                                  + "ON LENGTH(Predictions) = 0\n"
                                  + "  OR Predictions = 'null'\n"
                                  + "  OR ARRAY_LENGTH(SPLIT(Entries.Predictions, ';')) > AnswerIndex.Value\n"
                                  + "WHERE GameID = ?\n"
                                  + "GROUP BY Game,\n"
                                  + "         GameID,\n"
                                  + "         QuestionNumber,\n"
                                  + "         UserOption\n"
                                  + "ORDER BY QuestionNumber ASC,\n"
                                  + "         UserOption ASC\n",
                              properties.getQuestionEngineDatasetId(),
                              properties.getEntriesTableId(),
                              properties.getQuestionEngineDatasetId(),
                              properties.getEntriesTableId()))
                      .setUseLegacySql(false)
                      .setQueryParameters(
                          Arrays.asList(
                              new QueryParameter()
                                  .setParameterType(new QueryParameterType().setType("STRING"))
                                  .setParameterValue(new QueryParameterValue().setValue(quizId)),
                              new QueryParameter()
                                  .setParameterType(new QueryParameterType().setType("STRING"))
                                  .setParameterValue(new QueryParameterValue().setValue(quizId)))))
              .execute();
      if (ObjectUtils.isNotEmpty(response.getErrors())) {
        throw new IllegalStateException(
            String.format(
                "Failed to read records from to BigQuery. Reason: %s", response.toPrettyString()));
      }
      if (ObjectUtils.isEmpty(response.getRows())) {
        return Collections.emptyList();
      }
      return response.getRows().stream()
          .map(TableRow::getF)
          .map(this::toQuestionSummary)
          .collect(Collectors.toList());
    } catch (Exception ex) {
      log.error("Failed to query records BigQuery by id: {}. Reason: {}", quizId, ex);
      throw ex;
    }
  }

  private QuestionSummaryReport toQuestionSummary(List<TableCell> cells) {
    return new QuestionSummaryReport()
        .setQuizId(QuestionSummaryReport.BigQueryColumn.QUIZ_ID.of(cells))
        .setSourceId(QuestionSummaryReport.BigQueryColumn.SOURCE_ID.of(cells))
        .setQuestionNumber(QuestionSummaryReport.BigQueryColumn.QUESTION_NUMBER.of(cells))
        .setUserOption(QuestionSummaryReport.BigQueryColumn.USER_OPTION.of(cells))
        .setNumberOfEntries(QuestionSummaryReport.BigQueryColumn.NUMBER_OF_ENTRIES.of(cells));
  }
}
