package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.service.FileUploaderService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

class FileUploaderControllerTest {

  @Mock private FileUploaderService fileUploaderService;

  private FileUploaderController fileUploaderController;

  @BeforeEach
  void setUp() {
    MockitoAnnotations.openMocks(this);
    fileUploaderController = new FileUploaderController(fileUploaderService);
  }

  @Test
  void saveTodo_ValidFile_ReturnsOk() throws Exception {
    String brand = "ladbrokes";
    MultipartFile file = new MockMultipartFile("dupliatefile.txt", "File Upload".getBytes());
    when(fileUploaderService.saveToS3(brand, file)).thenReturn("uploadedvalidfile");
    ResponseEntity<String> response = fileUploaderController.saveCSVFileToS3(brand, file);
    verify(fileUploaderService, times(1)).saveToS3(brand, file);
  }

  @Test
  void saveTodo_EmptyFile_ThrowsIllegalStateException() {
    String brand = "coral";
    MultipartFile file = new MockMultipartFile("duplicateFile.txt", "".getBytes());
    IllegalStateException exception =
        assertThrows(
            IllegalStateException.class, () -> fileUploaderController.saveCSVFileToS3(brand, file));
    assertEquals("Cannot upload empty file", exception.getMessage());
  }
}
