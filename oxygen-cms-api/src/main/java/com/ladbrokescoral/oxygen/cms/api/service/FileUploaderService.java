package com.ladbrokescoral.oxygen.cms.api.service;

import com.amazonaws.AmazonServiceException;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Service
public class FileUploaderService {

  private final String promoSandboxCoralS3Bucket;

  private final String promoSandboxLadbrokesS3Bucket;

  private final AmazonS3 s3Client;

  public FileUploaderService(
      @Value(value = "${promoleaderboard.aws.s3.coral.bucket}") String promoSandboxCoralS3Bucket,
      @Value(value = "${promoleaderboard.aws.s3.ladbrokes.bucket}")
          String promoSandboxLadbrokesS3Bucket,
      @Value(value = "${promoleaderboard.aws.s3.region}") String promoSandboxS3Region) {
    this.promoSandboxCoralS3Bucket = promoSandboxCoralS3Bucket;
    this.promoSandboxLadbrokesS3Bucket = promoSandboxLadbrokesS3Bucket;
    this.s3Client =
        AmazonS3ClientBuilder.standard()
            .withCredentials(Util.awsS3CredentialsProvider())
            .withRegion(promoSandboxS3Region)
            .build();
  }

  public String saveToS3(String brand, MultipartFile file) {

    Map<String, String> metadata = new HashMap<>();
    metadata.put("Content-Type", file.getContentType());
    metadata.put("Content-Length", String.valueOf(file.getSize()));
    String fileName = String.format("%s", file.getOriginalFilename());
    String promoSandBoxBucket =
        Brand.BMA.equalsIgnoreCase(brand)
            ? promoSandboxCoralS3Bucket
            : promoSandboxLadbrokesS3Bucket;
    try {
      upload(promoSandBoxBucket, fileName, Optional.of(metadata), file.getInputStream());
    } catch (Exception e) {
      log.error("Failed to upload file to S3", e);
      throw new FileUploadException("Exception occurred while uploading file to S3: " + e);
    }
    return "File uploaded successfully to S3";
  }

  public void upload(
      String path,
      String fileName,
      Optional<Map<String, String>> optionalMetaData,
      InputStream inputStream) {
    ObjectMetadata objectMetadata = new ObjectMetadata();
    optionalMetaData.ifPresent(
        (Map<String, String> map) -> {
          if (!map.isEmpty()) {
            map.forEach(objectMetadata::addUserMetadata);
          }
        });
    try {
      log.info("uploading file path:{}, filename:{},metadata :{}", path, fileName, objectMetadata);
      s3Client.putObject(
          PathUtil.normalize(path), PathUtil.normalize(fileName), inputStream, objectMetadata);
      log.info("Successfully uploaded file :{} into path:{}", fileName, path);
    } catch (AmazonServiceException e) {
      throw new IllegalStateException("Failed to upload the file", e);
    }
  }
}
