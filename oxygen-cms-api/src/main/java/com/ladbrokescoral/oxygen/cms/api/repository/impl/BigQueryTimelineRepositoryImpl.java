package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.google.api.services.bigquery.Bigquery;
import com.google.api.services.bigquery.model.TableDataInsertAllRequest;
import com.google.api.services.bigquery.model.TableDataInsertAllResponse;
import com.ladbrokescoral.oxygen.cms.api.entity.TimelineBigQueryChangelog;
import com.ladbrokescoral.oxygen.cms.api.exception.ThirdPartyException;
import com.ladbrokescoral.oxygen.cms.api.repository.BigQueryTimelineRepository;
import com.ladbrokescoral.oxygen.cms.configuration.BigQueryProperties;
import java.util.Collections;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.ObjectUtils;

@Slf4j
@RequiredArgsConstructor
public class BigQueryTimelineRepositoryImpl implements BigQueryTimelineRepository {
  private final Bigquery bigquery;
  private final BigQueryProperties properties;

  @Override
  public void save(TimelineBigQueryChangelog changelog) {
    try {
      TableDataInsertAllResponse response =
          bigquery
              .tabledata()
              .insertAll(
                  properties.getProjectId(),
                  properties.getTimelineDatasetId(),
                  properties.getTimelineChangelogTableId(),
                  new TableDataInsertAllRequest()
                      .setRows(
                          Collections.singletonList(
                              new TableDataInsertAllRequest.Rows().setJson(changelog.asJson()))))
              .execute();
      if (ObjectUtils.isNotEmpty(response.getInsertErrors())) {
        throw new IllegalStateException(
            String.format(
                "Failed to insert the following record to BigQuery: %s. Reason: %s",
                changelog, response.toPrettyString()));
      }
      log.info("Successfully streamed data to BigQuery. Record: {}", changelog);
    } catch (Exception ex) {
      log.error("Failed to insert the following record to BigQuery: {}. Reason: {}", changelog, ex);
      throw new ThirdPartyException(ex);
    }
  }
}
