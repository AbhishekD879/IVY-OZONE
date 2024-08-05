package com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery;

import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryModel;

import java.io.IOException;
import java.util.List;

public interface BigQueryTable<M extends BigQueryModel<I, M>, I extends BigQueryModel.Id> {
  void insertAll(List<M> entities) throws IOException;

  List<M> read(I id) throws IOException;
}
