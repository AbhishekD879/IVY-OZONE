package com.ladbrokescoral.oxygen.cms.api.service.impl;

import static com.ladbrokescoral.oxygen.cms.util.PathUtil.*;

import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheServiceProvider;
import com.newrelic.api.agent.NewRelic;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicBoolean;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class CacheImageServiceImpl extends ImageServiceImpl {

  private static final String IMAGES_BASE_PATH = "cms/";
  private static final String IMAGES_BASE_PATH_DESKTOP = concatPath(IMAGES_BASE_PATH, "desktop/");
  private static final String IMAGES_BASE_PATH_MOBILE = concatPath(IMAGES_BASE_PATH, "mobile/");

  private final BrandCacheServiceProvider cacheServiceProvider;

  @Autowired
  public CacheImageServiceImpl(BrandCacheServiceProvider cacheServiceProvider) {
    this.cacheServiceProvider = cacheServiceProvider;
  }

  @Override
  public boolean removeImage(String brand, String path) {
    AtomicBoolean anyDeleted = new AtomicBoolean();
    cacheServiceProvider
        .getCacheService(brand)
        .forEach(
            cacheService -> {
              if (doDeleteFile(cacheService, path)) {
                cacheService.purgeCache(brand, path, "");
                anyDeleted.set(true);
              }
            });
    return anyDeleted.get();
  }

  @Override
  protected String getRootUrl(String brand) {
    String cacheRootUrl =
        cacheServiceProvider.getCacheService(brand).stream()
            .map(BrandCacheService::getRootUrl)
            .filter(StringUtils::isNotBlank)
            .findFirst()
            .orElse("");
    return concatUri(cacheRootUrl, IMAGES_BASE_PATH);
  }

  private Boolean doDeleteFile(BrandCacheService brandCacheService, String path) {
    return brandCacheService.deleteFile(concatPath(IMAGES_BASE_PATH, path))
        && brandCacheService.deleteFile(concatPath(IMAGES_BASE_PATH_MOBILE, path))
        && brandCacheService.deleteFile(concatPath(IMAGES_BASE_PATH_DESKTOP, path));
  }

  @Override
  public boolean uploadImage(String brand, InputStream imageStream, String imageName, String path) {
    if (Objects.isNull(imageStream)) {
      return false;
    }
    AtomicBoolean anyUploaded = new AtomicBoolean();
    try {
      byte[] fileBytes = IOUtils.toByteArray(imageStream);
      cacheServiceProvider
          .getCacheService(brand)
          .forEach(
              cacheService -> {
                // will set to true if file was uploaded to any cacheService
                if (doUploadFile(cacheService, path, imageName, fileBytes)) {
                  cacheService.purgeCache(brand, path, imageName);
                  anyUploaded.set(true);
                }
              });
    } catch (IOException e) {
      log.error("Failed to read image stream", e);
      NewRelic.noticeError(e);
    }
    return anyUploaded.get();
  }

  private Boolean doUploadFile(
      BrandCacheService brandCacheService, String path, String imageName, byte[] fileBytes) {

    return brandCacheService.uploadFile(
            concatPath(IMAGES_BASE_PATH, path), imageName, new ByteArrayInputStream(fileBytes))
        && brandCacheService.uploadFile(
            concatPath(IMAGES_BASE_PATH_MOBILE, path),
            imageName,
            new ByteArrayInputStream(fileBytes))
        && brandCacheService.uploadFile(
            concatPath(IMAGES_BASE_PATH_DESKTOP, path),
            imageName,
            new ByteArrayInputStream(fileBytes));
  }
}
