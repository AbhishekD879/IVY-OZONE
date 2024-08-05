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
@EqualsAndHashCode(callSuper = true, exclude = "createdDate")
@Accessors(chain = true)
public class BigQueryEntries extends AbstractBigQueryModel<BigQueryEntries> {
  private Instant gameStartDate;
  private Instant gameEndDate;
  private String customerId;
  private String username;
  private Instant createdDate;
  private String eventId;
  private String predictions;

  @Override
  public Map<String, Object> asJson() {
    Map<String, Object> json = super.asJson();

    json.put(Column.GAME_START_DATE.columnName, formatTime(gameStartDate));
    json.put(Column.GAME_END_DATE.columnName, formatTime(gameEndDate));
    json.put(Column.CUSTOMER_ID.columnName, customerId);
    json.put(Column.USERNAME.columnName, username);
    json.put(Column.CREATED_DATE.columnName, formatTime(createdDate));
    json.put(Column.EVENT_ID.columnName, eventId);
    json.put(Column.PREDICTIONS.columnName, predictions);

    return json;
  }

  @Override
  public BigQueryEntries populateFromCells(List<TableCell> cells) {
    return super.populateFromCells(cells)
        .setGameStartDate(super.getCellValueOrNullIfEmpty(cells.get(Column.GAME_START_DATE.columnPosition), value -> parseTime(value.toString())))
        .setGameEndDate(super.getCellValueOrNullIfEmpty(cells.get(Column.GAME_END_DATE.columnPosition), value -> parseTime(value.toString())))
        .setCustomerId(super.getCellValueOrNullIfEmpty(cells.get(Column.CUSTOMER_ID.columnPosition), String.class::cast))
        .setUsername(super.getCellValueOrNullIfEmpty(cells.get(Column.USERNAME.columnPosition), String.class::cast))
        .setCreatedDate(super.getCellValueOrNullIfEmpty(cells.get(Column.CREATED_DATE.columnPosition), value -> parseTime(value.toString())))
        .setEventId(super.getCellValueOrNullIfEmpty(cells.get(Column.EVENT_ID.columnPosition), String.class::cast))
        .setPredictions(super.getCellValueOrNullIfEmpty(cells.get(Column.PREDICTIONS.columnPosition), String.class::cast));
  }


  public BigQueryEntries setGameStartDate(Instant gameStartDate) {
    this.gameStartDate = withSecondsPrecision(gameStartDate);
    return this;
  }

  public BigQueryEntries setGameEndDate(Instant gameEndDate) {
    this.gameEndDate = withSecondsPrecision(gameEndDate);
    return this;
  }

  public BigQueryEntries setCreatedDate(Instant createdDate) {
    this.createdDate = withSecondsPrecision(createdDate);
    return this;
  }

  @RequiredArgsConstructor
  private enum Column {
    GAME_START_DATE("GameStartDate", 3),
    GAME_END_DATE("GameEndDate", 4),
    CUSTOMER_ID("CustomerID", 5),
    USERNAME("Username", 6),
    CREATED_DATE("CreatedDate", 7),
    EVENT_ID("EventID", 8),
    PREDICTIONS("Predictions", 9);

    final String columnName;
    final int columnPosition;
  }
}
