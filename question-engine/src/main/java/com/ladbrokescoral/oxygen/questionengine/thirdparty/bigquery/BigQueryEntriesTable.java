package com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery;

import com.google.api.services.bigquery.Bigquery;
import com.google.api.services.bigquery.model.TableCell;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.BigQueryProperties;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryGameId;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryEntries;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Repository;

import java.util.List;

@Lazy
@Repository
public class BigQueryEntriesTable extends AbstractBigQueryTable<BigQueryEntries, BigQueryGameId> {
  public BigQueryEntriesTable(Bigquery bigquery, BigQueryProperties properties) {
    super(bigquery, properties.getProjectId(), properties.getDatasetId(), properties.getEntriesTableId());
  }

  protected BigQueryEntries fromCells(List<TableCell> cells) {
    return new BigQueryEntries().populateFromCells(cells);
  }
}
