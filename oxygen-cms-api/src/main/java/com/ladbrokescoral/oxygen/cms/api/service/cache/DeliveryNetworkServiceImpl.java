package com.ladbrokescoral.oxygen.cms.api.service.cache;

import static com.ladbrokescoral.oxygen.cms.api.entity.UploadItem.Action.DELETE;
import static com.ladbrokescoral.oxygen.cms.api.entity.UploadItem.Action.UPLOAD;
import static com.ladbrokescoral.oxygen.cms.util.PathUtil.concatPath;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.ladbrokescoral.oxygen.cms.api.entity.UploadItem;
import com.ladbrokescoral.oxygen.cms.configuration.CFCacheTagProperties;
import com.newrelic.api.agent.NewRelic;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

@Slf4j
@Component("deliveryNetworkService")
@Primary
public class DeliveryNetworkServiceImpl implements DeliveryNetworkService {

  private static final String CMS_DATA_PATH = "cms/";
  private static final String CMS_DATA_MOBILE_PATH = "cms/mobile/";
  private static final String CMS_DATA_DESKTOP_PATH = "cms/desktop/";
  public static final String INTERRUPTED_WHILE_PUBLISHING_CONTENT =
      "Interrupted while publishing content: ";

  private final DeliveryNetworkExecutor deliveryNetworkExecutor;
  private final ObjectWriter objectWriter;
  private final CFCacheTagProperties cfCacheTagProperties;

  @Autowired
  public DeliveryNetworkServiceImpl(
      DeliveryNetworkExecutor deliveryNetworkExecutor,
      ObjectMapper objectMapper,
      CFCacheTagProperties cfCacheTagProperties) {
    this.deliveryNetworkExecutor = deliveryNetworkExecutor;
    this.objectWriter = objectMapper.writer();
    this.cfCacheTagProperties = cfCacheTagProperties;
  }

  public DeliveryNetworkServiceImpl(
      DeliveryNetworkExecutor deliveryNetworkExecutor,
      ObjectWriter objectWriter,
      CFCacheTagProperties cfCacheTagProperties) {
    this.deliveryNetworkExecutor = deliveryNetworkExecutor;
    this.objectWriter = objectWriter;
    this.cfCacheTagProperties = cfCacheTagProperties;
  }

  @Override
  public <T> void upload(String brand, String path, String fileName, T object) {
    try {
      NewRelic.incrementCounter(fileName);
      String content = objectWriter.writeValueAsString(object);
      addUploadItem(brand, concatPath(CMS_DATA_PATH, path), fileName, content);
      addUploadItem(brand, concatPath(CMS_DATA_MOBILE_PATH, path), fileName, content);
      addUploadItem(brand, concatPath(CMS_DATA_DESKTOP_PATH, path), fileName, content);
      log.info("Added {}/{} to delivery queue. Size: {}", path, fileName, content.length());
    } catch (InterruptedException ex) {
      log.error(INTERRUPTED_WHILE_PUBLISHING_CONTENT, ex);
      Thread.currentThread().interrupt();
    } catch (Exception e) {
      log.error("Can't publish content due to the error: ", e);
    }
  }

  public <T> void uploadCFContent(String brand, String path, String fileName, T object) {
    try {
      NewRelic.incrementCounter(fileName);
      String content = objectWriter.writeValueAsString(object);
      addUploadItem(
          brand,
          concatPath(CMS_DATA_PATH, path),
          fileName,
          content,
          cfCacheTagProperties.getTags().get(brand));
      log.info("Added {}/{} to delivery queue. Size: {}", path, fileName, content.length());
    } catch (InterruptedException ex) {
      log.error(INTERRUPTED_WHILE_PUBLISHING_CONTENT, ex);
      Thread.currentThread().interrupt();
    } catch (Exception e) {
      log.error("Can't publish content due to the error: ", e);
    }
  }

  @Override
  public void delete(String brand, String path, String fileName) {
    try {
      NewRelic.incrementCounter("delete-" + fileName);
      addDeleteItem(brand, concatPath(CMS_DATA_PATH, path), fileName);
      addDeleteItem(brand, concatPath(CMS_DATA_MOBILE_PATH, path), fileName);
      addDeleteItem(brand, concatPath(CMS_DATA_DESKTOP_PATH, path), fileName);
      log.info("Added {} to delivery queue", path);
    } catch (InterruptedException ex) {
      log.error(INTERRUPTED_WHILE_PUBLISHING_CONTENT, ex);
      Thread.currentThread().interrupt();
    } catch (Exception e) {
      log.error("Can't delete content due to the error: ", e);
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

  private void addDeleteItem(String brand, String path, String fileName)
      throws InterruptedException {
    deliveryNetworkExecutor.addItem(
        UploadItem.builder().action(DELETE).brand(brand).path(path).fileName(fileName).build());
  }

  private void addUploadItem(
      String brand, String path, String fileName, String content, String cacheTag)
      throws InterruptedException {
    deliveryNetworkExecutor.addItem(
        UploadItem.builder()
            .action(UPLOAD)
            .brand(brand)
            .path(path)
            .fileName(fileName)
            .cacheTag(cacheTag)
            .json(content)
            .build());
  }
}
