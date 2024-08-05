package com.coral.oxygen.middleware.common.configuration.cfcache;

import static com.coral.oxygen.middleware.common.configuration.cfcache.PathUtil.concatPath;
import static com.coral.oxygen.middleware.pojos.model.cache.UploadItem.Action.UPLOAD;

import com.coral.oxygen.middleware.pojos.model.cache.UploadItem;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.newrelic.api.agent.NewRelic;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

@Slf4j
@Component("deliveryNetworkService")
@Primary
public class DeliveryNetworkServiceImpl implements DeliveryNetworkService {

  private static final String CMS_DATA_PATH = "cms";
  public static final String INTERRUPTED_WHILE_PUBLISHING_CONTENT =
      "Interrupted while publishing content: ";

  private final DeliveryNetworkExecutor deliveryNetworkExecutor;
  private final ObjectWriter objectWriter;

  @Autowired
  public DeliveryNetworkServiceImpl(
      DeliveryNetworkExecutor deliveryNetworkExecutor, ObjectWriter objectWriter) {
    this.deliveryNetworkExecutor = deliveryNetworkExecutor;
    this.objectWriter = objectWriter;
  }

  @Override
  public <T> void upload(String brand, String path, String fileName, T object) {
    try {
      NewRelic.incrementCounter(fileName);
      String content = objectWriter.writeValueAsString(object);
      addUploadItem(brand, concatPath(CMS_DATA_PATH, path), fileName, content);
      log.info("Added {}/{} to delivery queue. Size: {}", path, fileName, content.length());
    } catch (InterruptedException ex) {
      log.error(INTERRUPTED_WHILE_PUBLISHING_CONTENT, ex);
      Thread.currentThread().interrupt();
    } catch (Exception e) {
      log.error("Can't publish content due to the error: ", e);
    }
  }

  private void addUploadItem(String brand, String path, String fileName, String content)
      throws InterruptedException {
    deliveryNetworkExecutor.addItem(
        UploadItem.builder()
            .action(UPLOAD)
            .brand(brand)
            .path(path)
            .fileName(fileName)
            .json(content)
            .build());
  }
}
