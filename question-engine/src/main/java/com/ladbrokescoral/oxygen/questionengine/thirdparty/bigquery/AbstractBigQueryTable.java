package com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery;

import com.google.api.services.bigquery.Bigquery;
import com.google.api.services.bigquery.model.QueryParameter;
import com.google.api.services.bigquery.model.QueryParameterType;
import com.google.api.services.bigquery.model.QueryParameterValue;
import com.google.api.services.bigquery.model.QueryRequest;
import com.google.api.services.bigquery.model.QueryResponse;
import com.google.api.services.bigquery.model.TableCell;
import com.google.api.services.bigquery.model.TableDataInsertAllRequest;
import com.google.api.services.bigquery.model.TableDataInsertAllResponse;
import com.google.api.services.bigquery.model.TableRow;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;

import java.io.IOException;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;


@Slf4j
@RequiredArgsConstructor
public abstract class AbstractBigQueryTable<M extends BigQueryModel<I, M>, I extends BigQueryModel.Id> implements BigQueryTable<M, I> {
  private final Bigquery bigquery;
  private final String projectId;
  private final String datasetId;
  private final String tableId;

  @Override
  public void insertAll(List<M> entities) throws IOException {
    if (CollectionUtils.isNotEmpty(entities)) {
      try {
        TableDataInsertAllResponse response = bigquery
            .tabledata()
            .insertAll(projectId, datasetId, tableId,
                new TableDataInsertAllRequest().setRows(entities.stream()
                    .map(entity -> new TableDataInsertAllRequest.Rows().setJson(entity.asJson()))
                    .collect(Collectors.toList())
                ))
            .execute();
        if (CollectionUtils.isNotEmpty(response.getInsertErrors())) {
          throw new IllegalStateException(String.format("Failed to insert the following records to BigQuery: %s. Reason: %s",
              entities,
              response.toPrettyString())
          );
        }
        log.info("Successfully streamed data to BigQuery. Records: {}", entities);
      } catch (Exception ex) {
        log.error("Failed to insert the following records to BigQuery: {}. Reason: {}", entities, ex);
        throw ex;
      }
    }
  }

  @Override
  public List<M> read(I id) throws IOException {
    if (id == null) {
      throw new IllegalArgumentException("id must not be null");
    }

    try {
      QueryResponse response = bigquery.jobs()
          .query(projectId, new QueryRequest().setParameterMode("POSITIONAL")
              .setQuery(String.format("SELECT * FROM %s.%s WHERE %s  = ?", datasetId, tableId, id.columnName()))
              .setUseLegacySql(false)
              .setQueryParameters(Collections.singletonList(
                  new QueryParameter()
                      .setParameterType(new QueryParameterType().setType("STRING"))
                      .setParameterValue(new QueryParameterValue().setValue(id.get().toString()))))
          )
          .execute();
      if (CollectionUtils.isNotEmpty(response.getErrors())) {
        throw new IllegalStateException(String.format("Failed to read records from to BigQuery. Reason: %s", response.toPrettyString()));
      }
      if (CollectionUtils.isEmpty(response.getRows())) {
        return Collections.emptyList();
      }
      return response.getRows().stream()
          .map(TableRow::getF)
          .map(this::fromCells)
          .collect(Collectors.toList());
    } catch (Exception ex) {
      log.error("Failed to query records BigQuery by id: {}. Reason: {}", id, ex);
      throw ex;
    }
  }

  protected abstract M fromCells(List<TableCell> cells);
}
