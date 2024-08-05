package com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model;

import lombok.Data;
import lombok.RequiredArgsConstructor;

@Data
@RequiredArgsConstructor
public class BigQueryGameId implements BigQueryModel.Id {
  private final String gameId;

  @Override
  public String get() {
    return gameId;
  }

  @Override
  public String columnName() {
    return "GameID";
  }
}
