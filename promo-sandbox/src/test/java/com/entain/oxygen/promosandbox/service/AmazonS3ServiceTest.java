package com.entain.oxygen.promosandbox.service;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.S3Object;
import com.entain.oxygen.promosandbox.config.S3BrandProperties;
import com.entain.oxygen.promosandbox.utils.IConstantsTest;
import com.entain.oxygen.promosandbox.utils.TestUtil;
import java.util.Date;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.retry.support.RetryTemplate;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(SpringExtension.class)
class AmazonS3ServiceTest {

  @Mock private AmazonS3 amazonS3;

  @Mock private S3BrandProperties s3BrandConfig;

  @InjectMocks private AmazonS3Service amazonS3Service;

  @BeforeEach
  void setup() {
    RetryTemplate retryTemplate = new RetryTemplate();
    ReflectionTestUtils.setField(amazonS3Service, "retryTemplate", retryTemplate);
  }

  @Test
  void downloadCsvFileTest() {
    S3Object s3Object = new S3Object();
    s3Object.setBucketName("test");
    s3Object.setObjectContent(TestUtil.readFromFile("/FSS_Leaderboard_20220528-7.csv"));
    ObjectMetadata metadata = new ObjectMetadata();
    metadata.setLastModified(new Date());
    s3Object.setObjectMetadata(metadata);
    when(s3BrandConfig.getBucket()).thenReturn("test");
    when(amazonS3.getObject(anyString(), anyString())).thenReturn(s3Object);
    assertEquals(
        2,
        amazonS3Service
            .fetchAmazonS3CsvData(IConstantsTest.PROMOTION_ID, "test.csv")
            .getRowList()
            .size());
  }

  @Test
  void downloadCsvFileInvalidContentTest() {
    S3Object s3Object = new S3Object();
    s3Object.setBucketName("test");
    ObjectMetadata metadata = new ObjectMetadata();
    metadata.setLastModified(new Date());
    s3Object.setObjectMetadata(metadata);
    when(s3BrandConfig.getBucket()).thenReturn("test");
    when(amazonS3.getObject(anyString(), anyString())).thenReturn(s3Object);
    assertNull(
        amazonS3Service.fetchAmazonS3CsvData(IConstantsTest.PROMOTION_ID, "test.csv").getRowList());
  }

  @Test
  void downloadCsvFileS3ObjectNullTest() {
    when(s3BrandConfig.getBucket()).thenReturn("test");
    when(amazonS3.getObject(anyString(), anyString())).thenReturn(null);
    assertNull(
        amazonS3Service.fetchAmazonS3CsvData(IConstantsTest.PROMOTION_ID, "test.csv").getRowList());
  }
}
