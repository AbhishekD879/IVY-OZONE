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
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true, exclude = "uploadedDate")
@Accessors(chain = true)
public class BigQueryQuestions extends AbstractBigQueryModel<BigQueryQuestions> {
  private Instant gameStartDate;
  private Instant gameEndDate;
  private String eventName;
  private Integer questionNumber;
  private String questionText;
  private String answerOption;
  private String answerText;
  private Instant uploadedDate;

  @Override
  public Map<String, Object> asJson() {
    Map<String, Object> json = super.asJson();

    json.put(Column.GAME_START_DATE.columnName, formatTime(gameStartDate));
    json.put(Column.GAME_END_DATE.columnName, formatTime(gameEndDate));
    json.put(Column.EVENT_NAME.columnName, eventName);
    json.put(Column.QUESTION_NUMBER.columnName, questionNumber);
    json.put(Column.QUESTION_TEXT.columnName, questionText);
    json.put(Column.ANSWER_OPTION.columnName, answerOption);
    json.put(Column.ANSWER_TEXT.columnName, answerText);
    json.put(Column.UPLOADED_DATE.columnName, formatTime(uploadedDate));

    return json;
  }

  @Override
  public BigQueryQuestions populateFromCells(List<TableCell> cells) {
    return super.populateFromCells(cells)
        .setGameStartDate(super.getCellValueOrNullIfEmpty(cells.get(Column.GAME_START_DATE.columnPosition), value -> parseTime(value.toString())))
        .setGameEndDate(super.getCellValueOrNullIfEmpty(cells.get(Column.GAME_END_DATE.columnPosition), value -> parseTime(value.toString())))
        .setEventName(super.getCellValueOrNullIfEmpty(cells.get(Column.EVENT_NAME.columnPosition), String.class::cast))
        .setQuestionNumber(super.getCellValueOrNullIfEmpty(cells.get(Column.QUESTION_NUMBER.columnPosition), value -> Integer.valueOf(value.toString())))
        .setQuestionText(super.getCellValueOrNullIfEmpty(cells.get(Column.QUESTION_TEXT.columnPosition), String.class::cast))
        .setAnswerOption(super.getCellValueOrNullIfEmpty(cells.get(Column.ANSWER_OPTION.columnPosition), String.class::cast))
        .setAnswerText(super.getCellValueOrNullIfEmpty(cells.get(Column.ANSWER_TEXT.columnPosition), String.class::cast))
        .setUploadedDate(super.getCellValueOrNullIfEmpty(cells.get(Column.UPLOADED_DATE.columnPosition), value -> parseTime(value.toString())));
  }

  public BigQueryQuestions setGameStartDate(Instant gameStartDate) {
    this.gameStartDate = withSecondsPrecision(gameStartDate);
    return this;
  }

  public BigQueryQuestions setGameEndDate(Instant gameEndDate) {
    this.gameEndDate = withSecondsPrecision(gameEndDate);
    return this;
  }

  public BigQueryQuestions setUploadedDate(Instant uploadedDate) {
    this.uploadedDate = withSecondsPrecision(uploadedDate);
    return this;
  }

  @RequiredArgsConstructor
  private enum Column {
    UPLOADED_DATE("UploadedDate", 3),
    GAME_START_DATE("GameStartDate", 4),
    GAME_END_DATE("GameEndDate", 5),
    EVENT_NAME("Event", 6),
    QUESTION_NUMBER("Question_Number", 7),
    QUESTION_TEXT("Question_Text", 8),
    ANSWER_OPTION("Answer_Option", 9),
    ANSWER_TEXT("Answer_Text", 10);

    final String columnName;
    final int columnPosition;
  }
}
