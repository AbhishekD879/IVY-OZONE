package com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.configuration.ApiProperties;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;
import java.util.Collections;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import javax.annotation.PreDestroy;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.IOUtils;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Slf4j
@Component
public class BppMaintenanceService {

  private final ObjectMapper mapper;
  private final Map<String, ApiProperties.ApiConfiguration> bppAccessUrls;
  private final CloseableHttpClient httpClient;
  private static final int STATUS_CODE = 400;

  @Autowired
  public BppMaintenanceService(
      CloseableHttpClient httpClient, ApiProperties apiProperties, ObjectMapper mapper) {
    this.httpClient = httpClient;
    this.mapper = mapper;
    this.bppAccessUrls = apiProperties.getBppMaintenance();

    if (CollectionUtils.isEmpty(bppAccessUrls)) {
      log.error("BPP Urls were not configured for Maintenance notifications");
    }
  }

  public BppMaintenanceResponse sendNotification(String brand, BppMaintenanceRequest bppRequest)
      throws IOException {
    ApiProperties.ApiConfiguration brandConfig = bppAccessUrls.get(brand);
    String notificationUrl = brandConfig.getUrl();
    bppRequest.setSecret(brandConfig.getSecret());
    BppMaintenanceResponse response = null;
    try {
      response = doPost(notificationUrl, bppRequest);
    } catch (IOException e) {
      log.error("Failed to send maintenance notification to BPP {}", notificationUrl, e);
    }
    if (Objects.isNull(response) || response.getCode() >= STATUS_CODE) {
      log.debug("Retrying BPP maintenance notification ");
      response = doPost(notificationUrl, bppRequest);
    }
    return response;
  }

  private BppMaintenanceResponse doPost(String notificationUrl, BppMaintenanceRequest bppRequest)
      throws IOException {
    HttpPost request = new HttpPost(notificationUrl);
    request.setEntity(
        new StringEntity(mapper.writeValueAsString(bppRequest), ContentType.APPLICATION_JSON));
    try (CloseableHttpResponse response = httpClient.execute(request);
        InputStream is = response.getEntity().getContent(); ) {
      return new BppMaintenanceResponse(
          notificationUrl,
          response.getStatusLine().getStatusCode(),
          response.getStatusLine().getReasonPhrase(),
          contentAsString(is));
    }
  }

  private String contentAsString(InputStream content) throws IOException {
    if (Objects.isNull(content)) {
      return null;
    }
    return IOUtils.toString(content, Charset.defaultCharset());
  }

  public Set<String> getSupportedBrands() {
    return Optional.ofNullable(bppAccessUrls)
        .map(Map::keySet)
        .map(Collections::unmodifiableSet)
        .orElse(Collections.emptySet());
  }

  @PreDestroy
  public void close() {
    try {
      httpClient.close();
    } catch (IOException e) {
      log.warn("Failed to close BPP maintenance HttpClient", e);
    }
  }
}
