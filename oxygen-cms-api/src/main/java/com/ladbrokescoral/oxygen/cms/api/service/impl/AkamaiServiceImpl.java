package com.ladbrokescoral.oxygen.cms.api.service.impl;

import com.akamai.netstorage.NetStorage;
import com.akamai.netstorage.NetStorageException;
import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheService;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;

@Slf4j
public class AkamaiServiceImpl implements BrandCacheService {

  private final String uploadCpCode;
  private final String akamaiPath;

  private final CachePurgeService purgeService;
  private final NetStorage netStorage;

  AkamaiServiceImpl(
      NetStorage netStorage, String akamaiPath, String uploadCpCode, CachePurgeService cdnService) {
    this.netStorage = netStorage;
    this.akamaiPath = akamaiPath;
    this.uploadCpCode = uploadCpCode;
    this.purgeService = cdnService;
  }

  @Override
  @Trace(dispatcher = true, metricName = "akamaiUploadJSON")
  public boolean uploadJSON(String relativePath, String fileName, String json) {

    log.info(
        "Uploading {} to Akamai {} with payload {}",
        fileName,
        buildPath(akamaiPath, relativePath, fileName),
        json);

    InputStream stream = new ByteArrayInputStream(json.getBytes(StandardCharsets.UTF_8));

    return uploadFile(akamaiPath, relativePath, fileName, stream);
  }

  private boolean uploadFile(
      String rootPath, String relativePath, String fileName, InputStream fileStream) {
    try {
      if (StringUtils.isNotBlank(uploadCpCode)) {
        return uploadWithCpCode(
            buildPath(rootPath, relativePath, fileName), uploadCpCode, fileStream);
      } else {
        return netStorage.upload(buildPath(rootPath, relativePath, fileName), fileStream);
      }
    } catch (NetStorageException | IOException e) {
      log.error(
          "File wasn`t uploaded by path {}: ", buildPath(rootPath, relativePath, fileName), e);
      NewRelic.noticeError(e);
    }
    return false;
  }

  /**
   * @param path full path to upload
   * @param cpCode required to upload to ObjectStore
   * @param fileStream - stream to upload
   * @return confirmation the stream was uploaded
   * @throws NetStorageException
   * @throws IOException
   */
  private Boolean uploadWithCpCode(String path, String cpCode, InputStream fileStream)
      throws NetStorageException, IOException {
    Map<String, String> additionalParams = new HashMap<>();
    additionalParams.put("cpcode", cpCode);
    return netStorage.upload(
        path,
        fileStream,
        additionalParams,
        Date.from(Instant.now()),
        null,
        null,
        null,
        null,
        false);
  }

  @Override
  @Trace(dispatcher = true, metricName = "akamaiUploadFile")
  public boolean uploadFile(String relativePath, String fileName, InputStream fileStream) {
    log.info("Uploading {} to Akamai {}", fileName, buildPath(akamaiPath, relativePath, fileName));
    return uploadFile(akamaiPath, relativePath, fileName, fileStream);
  }

  // used only for images in one place
  @Override
  public boolean deleteFile(String relativePathAndName) {
    try {
      return netStorage.delete(buildPath(relativePathAndName));
    } catch (NetStorageException | IOException e) {
      log.error("Unable to deleteFile file: ", e);
      NewRelic.noticeError(e);
    }
    return false;
  }

  private String buildPath(String rootPath, String relativePath, String fileName) {
    return PathUtil.concatPath(rootPath, relativePath, fileName);
  }

  private String buildPath(String relativePathAndName) {
    return PathUtil.concatPath(akamaiPath, relativePathAndName);
  }

  @Override
  public void purgeCache(String brand, String path, String fileName) {
    purgeService.purgeCache(brand, path, fileName);
  }

  @Override
  public String getRootUrl() {
    return purgeService.getRootUrl();
  }

  @Override
  public void shutdown() {
    purgeService.shutdown();
  }
}
