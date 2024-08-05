package com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery;

import com.google.api.services.bigquery.Bigquery;
import com.google.api.services.bigquery.model.TableCell;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.BigQueryProperties;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryGameId;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryResults;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Repository;

import java.util.List;

@Lazy
@Repository
public class BigQueryResultsTable extends AbstractBigQueryTable<BigQueryResults, BigQueryGameId> {
  public BigQueryResultsTable(Bigquery bigquery, BigQueryProperties properties) {
    super(bigquery, properties.getProjectId(), properties.getDatasetId(), properties.getResultsTableId());
  }

  @Override
  protected BigQueryResults fromCells(List<TableCell> cells) {
    return new BigQueryResults().populateFromCells(cells);
  }
}
