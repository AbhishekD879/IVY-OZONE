package com.ladbrokescoral.oxygen.cms.api.service.impl;

import com.amazonaws.SdkClientException;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.amazonaws.services.s3.model.DeleteObjectRequest;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheService;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.nio.charset.StandardCharsets;
import java.util.Locale;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.FilenameUtils;
import org.apache.commons.lang3.StringUtils;

@Slf4j
public class AmazonS3ServiceImpl implements BrandCacheService {

  private final CachePurgeService purgeService;
  private final AmazonS3 amazonClient;
  private final String bucketName;
  private final String basePath;
  private String instanceIP;
  private String instanceName;

  AmazonS3ServiceImpl(
      AmazonS3 amazonClient, String bucketName, String basePath, CachePurgeService purgeService) {
    this.amazonClient = amazonClient;
    this.bucketName = bucketName;
    this.basePath = StringUtils.defaultString(basePath, "");
    this.purgeService = purgeService;

    initInstanceData();
  }

  private void initInstanceData() {
    try {
      InetAddress localHost = InetAddress.getLocalHost();
      instanceIP = localHost.getHostAddress();
      instanceName = localHost.getHostName();
      log.info("S3 service initialized on instance IP {}, name {}", instanceIP, instanceName);
    } catch (UnknownHostException e) {
      log.warn("Failed to get instance address", e);
    }
  }

  @Override
  public boolean uploadFile(String relativePath, String fileName, InputStream fileStream) {
    try {
      doUpload("cms-image", getKey(relativePath, fileName), getContentType(fileName), fileStream);
      return true;
    } catch (SdkClientException e) {
      log.error("Issue with uploading file to AWS S3 bucket: ", e);
    }
    return false;
  }

  @Override
  public boolean uploadJSON(String relativePath, String fileName, String json) {
    String key = getKey(relativePath, fileName);
    try (InputStream inputStream =
        new ByteArrayInputStream(json.getBytes(StandardCharsets.UTF_8))) {
      doUpload("cms-json", key, getContentType(fileName), inputStream);
      return true;
    } catch (SdkClientException e) {
      log.error("Issue with uploading file with key {} to AWS S3 bucket: ", key, e);
    } catch (IOException e) {
      log.error("Failed to read json as stream: ", e);
    }
    return false;
  }

  @Override
  public boolean deleteFile(String path) {
    try {
      amazonClient.deleteObject(
          new DeleteObjectRequest(bucketName, getKey(PathUtil.normalize(path), null)));
      return true;
    } catch (SdkClientException e) {
      log.error("Issue with removing file {} from AWS S3 bucket: ", path, e);
    }
    return false;
  }

  private void doUpload(
      String internalDataType, String key, String contentType, InputStream inputStream) {
    log.info("Uploading {} to S3 {}", internalDataType, key);
    ObjectMetadata metadata = new ObjectMetadata();
    // probably should be title (headers received: x-amz-meta-x-amz-meta-title: cms-json)?
    metadata.addUserMetadata("x-amz-meta-title", internalDataType);
    metadata.addUserMetadata("cms-instance-ip", instanceIP);
    metadata.addUserMetadata("cms-instance-name", instanceName);
    metadata.setContentType(contentType);
    PutObjectRequest request = new PutObjectRequest(bucketName, key, inputStream, metadata);
    request.withCannedAcl(CannedAccessControlList.PublicRead);
    amazonClient.putObject(request);
  }

  private String getKey(String relativePath, String fileName) {
    String path = PathUtil.concatPath(basePath, relativePath, fileName);
    return removeLeadingSlash(path);
  }

  private String removeLeadingSlash(String path) {
    if (path.startsWith("/")) {
      path = path.substring(1);
    }
    return path;
  }

  private String getContentType(String fileName) {
    return Optional.ofNullable(fileName)
        .map(FilenameUtils::getExtension)
        .map(
            (String ext) -> {
              switch (ext.toLowerCase(Locale.ENGLISH)) {
                case "png":
                  return "image/png";
                case "jpeg":
                case "jpg":
                  return "image/jpeg";
                case "svg":
                  return "image/svg+xml";
                case "json":
                  return "application/json";
                default:
                  return null;
              }
            })
        .orElse("application/json");
  }

  @Override
  public void purgeCache(String brand, String path, String fileName) {
    purgeService.purgeCache(brand, path, fileName);
  }

  @Override
  public void purgeCache(String brand, String path, String fileName, String cacheTag) {
    purgeService.purgeCache(brand, path, fileName, cacheTag);
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
