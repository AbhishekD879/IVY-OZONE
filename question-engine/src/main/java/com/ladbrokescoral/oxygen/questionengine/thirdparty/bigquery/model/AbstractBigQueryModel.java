package com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model;

import com.google.api.services.bigquery.model.TableCell;
import lombok.Data;
import lombok.RequiredArgsConstructor;

import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

@Data
public abstract class AbstractBigQueryModel<S extends AbstractBigQueryModel<S>> implements BigQueryModel<BigQueryGameId, S> {
  /**
   * For some reason BigQuery truncates the millis part if it's zero, that's why we need to skip it for consistency.
   */
  private static final DateTimeFormatter TIME_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss").withZone(ZoneId.of("UTC"));

  private String brand;
  private String game;
  private String gameId;

  @Override
  public BigQueryGameId id() {
    return new BigQueryGameId(gameId);
  }

  @Override
  public Map<String, Object> asJson() {
    Map<String, Object> json = new HashMap<>();

    json.put(Column.BRAND.columnName, brand);
    json.put(Column.GAME.columnName, game);
    json.put(Column.GAME_ID.columnName, gameId);

    return json;
  }

  @Override
  public S populateFromCells(List<TableCell> cells) {
    return this.setBrand(this.getCellValueOrNullIfEmpty(cells.get(Column.BRAND.columnPosition), String.class::cast))
        .setGame(this.getCellValueOrNullIfEmpty(cells.get(Column.GAME.columnPosition), String.class::cast))
        .setGameId(this.getCellValueOrNullIfEmpty(cells.get(Column.GAME_ID.columnPosition), String.class::cast));
  }

  @SuppressWarnings("unchecked")
  public S setBrand(String brand) {
    this.brand = brand;
    return (S) this;
  }

  @SuppressWarnings("unchecked")
  public S setGame(String game) {
    this.game = game;
    return (S) this;
  }

  @SuppressWarnings("unchecked")
  public S setGameId(String gameId) {
    this.gameId = gameId;
    return (S) this;
  }

  protected final <T> T getCellValueOrNullIfEmpty(TableCell cell, Function<Object, T> converter) {
    Object cellValue = cell.getV();

    /*
      Apparently, BigQuery return empty objects whereas values is in fact empty.
     */
    if (cellValue.getClass().equals(Object.class)) {
      return null;
    }
    return converter.apply(cellValue);
  }

  protected final String formatTime(Instant time) {
    return TIME_FORMATTER.format(time);
  }

  protected final Instant withSecondsPrecision(Instant time) {
    return time.truncatedTo(ChronoUnit.SECONDS);
  }

  protected final Instant parseTime(String time) {
    return TIME_FORMATTER.parse(time, Instant::from);
  }

  @RequiredArgsConstructor
  private enum Column {
    BRAND("Brand", 0),
    GAME("Game", 1),
    GAME_ID("GameID", 2);

    final String columnName;
    final int columnPosition;
  }
}
