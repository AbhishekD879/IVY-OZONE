package com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model;

import com.google.api.services.bigquery.model.TableCell;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.RequiredArgsConstructor;
import lombok.ToString;
import lombok.experimental.Accessors;

import java.time.Instant;
import java.util.List;
import java.util.Map;

@Data
@EqualsAndHashCode(callSuper = true, exclude = "resultedDate")
@ToString(callSuper = true)
@Accessors(chain = true)
public class BigQueryResults extends AbstractBigQueryModel<BigQueryResults> {
  private Instant resultedDate;
  private Integer questionNumber;
  private String answerOption;

  @Override
  public Map<String, Object> asJson() {
    Map<String, Object> json = super.asJson();

    json.put(Column.RESULTED_DATE.columnName, formatTime(resultedDate));
    json.put(Column.QUESTION_NUMBER.columnName, questionNumber);
    json.put(Column.ANSWER_OPTION.columnName, answerOption);

    return json;
  }

  @Override
  public BigQueryResults populateFromCells(List<TableCell> cells) {
    return super.populateFromCells(cells)
        .setResultedDate(super.getCellValueOrNullIfEmpty(cells.get(Column.RESULTED_DATE.columnPosition), value -> parseTime(value.toString())))
        .setQuestionNumber(super.getCellValueOrNullIfEmpty(cells.get(Column.QUESTION_NUMBER.columnPosition), value -> Integer.valueOf(value.toString())))
        .setAnswerOption(super.getCellValueOrNullIfEmpty(cells.get(Column.ANSWER_OPTION.columnPosition), String.class::cast));
  }

  public BigQueryResults setResultedDate(Instant resultedDate) {
    this.resultedDate = withSecondsPrecision(resultedDate);
    return this;
  }

  @RequiredArgsConstructor
  private enum Column {
    RESULTED_DATE("ResultedDate", 3),
    QUESTION_NUMBER("Question_Number", 4),
    ANSWER_OPTION("Answer_Option", 5);

    final String columnName;
    final int columnPosition;
  }
}
