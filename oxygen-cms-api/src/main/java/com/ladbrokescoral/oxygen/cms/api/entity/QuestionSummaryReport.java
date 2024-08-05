package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.google.api.services.bigquery.model.TableCell;
import java.util.List;
import java.util.function.Function;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@JsonPropertyOrder({
  "quizId",
  "sourceId",
  "questionNumber",
  "userOption",
  "totalNumberOfEntries",
  "numberOfEntries",
  "percentOfTotalEntries"
})
public class QuestionSummaryReport {

  private String quizId;
  private String sourceId;
  private Integer questionNumber;
  private String userOption;
  private Integer totalNumberOfEntries;
  private Integer numberOfEntries;
  private String percentOfTotalEntries;

  @RequiredArgsConstructor
  public enum BigQueryColumn {
    QUIZ_ID("QuizID", 0, String.class::cast),
    SOURCE_ID("SourceID", 1, String.class::cast),
    QUESTION_NUMBER("QuestionNumber", 2, value -> Integer.parseInt(value.toString())),
    USER_OPTION("UserOption", 3, String.class::cast),
    NUMBER_OF_ENTRIES("NumberOfEntries", 4, value -> Integer.parseInt(value.toString()));

    final String columnName;
    final int columnPosition;
    final Function<Object, ?> converter;

    @SuppressWarnings("unchecked")
    public <T> T of(List<TableCell> cells) {
      Object cellValue = cells.get(columnPosition).getV();

      /*
       Apparently, BigQuery return empty objects whereas values are in fact empty.
      */
      if (cellValue.getClass().equals(Object.class)) {
        return null;
      }
      return (T) converter.apply(cellValue);
    }
  }
}
