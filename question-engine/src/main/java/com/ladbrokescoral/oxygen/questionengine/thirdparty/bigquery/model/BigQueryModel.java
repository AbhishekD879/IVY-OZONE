package com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model;

import com.google.api.services.bigquery.model.TableCell;

import java.util.List;
import java.util.Map;

public interface BigQueryModel<I extends BigQueryModel.Id, S extends BigQueryModel<I, S>> {
  I id();

  Map<String, Object> asJson();

  S populateFromCells(List<TableCell> cells);

  interface Id {
    Object get();

    String columnName();
  }
}
