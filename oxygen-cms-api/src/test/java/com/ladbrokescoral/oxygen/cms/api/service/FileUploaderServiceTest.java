package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;

import com.amazonaws.AmazonServiceException;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentMatcher;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.multipart.MultipartFile;

class FileUploaderServiceTest {

  private FileUploaderService fileUploaderService;
  private AmazonS3 mockS3Client;
  private static final String ACCESS_S3_KEY_ENV_VAR = "AWS_S3_ACCESS_KEY_ID";
  private static final String SECRET_S3_KEY_ENV_VAR = "AWS_S3_SECRET_ACCESS_KEY";

  @BeforeEach
  public void setup() {
    mockS3Client = mock(AmazonS3.class);
    fileUploaderService = new FileUploaderService("bucket1", "bucket2", "us-east-1");
    ReflectionTestUtils.setField(fileUploaderService, "s3Client", mockS3Client);
  }

  @Test
  void testSaveToS3_SuccessCondition() throws IOException {
    MultipartFile mockFile = mock(MultipartFile.class);
    when(mockFile.getContentType()).thenReturn("text/plain");
    when(mockFile.getSize()).thenReturn(1000L);
    when(mockFile.getOriginalFilename()).thenReturn("test.txt");
    when(mockFile.getInputStream()).thenReturn(mock(InputStream.class));
    String result = fileUploaderService.saveToS3("BMA", mockFile);
    result = fileUploaderService.saveToS3("LADBROKES", mockFile);
    assertEquals("File uploaded successfully to S3", result);
  }

  @Test
  void testSaveToS3_FailCondiiton() throws IOException {
    MultipartFile mockFile = mock(MultipartFile.class);
    when(mockFile.getInputStream()).thenThrow(new IOException());
    assertThrows(FileUploadException.class, () -> fileUploaderService.saveToS3("BMA", mockFile));
  }

  @Test
  void testUpload_SuccessCondition() {
    InputStream mockInputStream = mock(InputStream.class);
    ArgumentMatcher<ObjectMetadata> metadataMatcher =
        metadata -> metadata.getUserMetadata() != null && metadata.getUserMetadata().isEmpty();
    fileUploaderService.upload("path", "file.txt", Optional.of(new HashMap<>()), mockInputStream);
    verify(mockS3Client)
        .putObject(eq("path"), eq("file.txt"), eq(mockInputStream), argThat(metadataMatcher));
  }

  @Test
  void testUpload_FailCondition() {
    MockMultipartFile file =
        new MockMultipartFile("data", "filename.txt", "text/csv", "some csv".getBytes());
    Map<String, String> metadata = new HashMap<>();
    metadata.put("Content-Type", file.getContentType());
    metadata.put("Content-Length", String.valueOf(file.getSize()));
    doThrow(AmazonServiceException.class)
        .when(mockS3Client)
        .putObject(anyString(), anyString(), any(InputStream.class), any(ObjectMetadata.class));
    try {
      fileUploaderService.upload(
          "path", "file.txt", Optional.of(metadata), mock(InputStream.class));
    } catch (IllegalStateException e) {
      assertEquals("Failed to upload the file", e.getMessage());
    }
  }
}
