package com.ladbrokescoral.oxygen.cms.configuration;

import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Data
@Lazy
@Component
@ConfigurationProperties("google-cloud.big-query")
public class BigQueryProperties {
  private String clientId;
  private String clientEmail;

  /*
   Infrastructure-manged.
  */
  @Value("${GCLOUD_PRIVATE_KEY}")
  private String privateKey;

  private String privateKeyId;
  private String projectId;
  private String questionEngineDatasetId;
  private String timelineDatasetId;
  private String entriesTableId;
  private String timelineChangelogTableId;
}