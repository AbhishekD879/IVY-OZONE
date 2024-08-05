package com.coral.oxygen.middleware.common.configuration.cfcache;

import com.amazonaws.SdkClientException;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.nio.charset.StandardCharsets;
import lombok.extern.slf4j.Slf4j;
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
  public boolean uploadJSON(String relativePath, String fileName, String json) {
    String key = getKey(relativePath, fileName);
    try (InputStream inputStream =
        new ByteArrayInputStream(json.getBytes(StandardCharsets.UTF_8))) {
      doUpload("cms-json", key, "application/json", inputStream);
      return true;
    } catch (SdkClientException e) {
      log.error("Issue with uploading file with key {} to AWS S3 bucket: ", key, e);
    } catch (Exception e) {
      log.error("Failed to read json as stream: ", e);
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
