package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.service.FileUploaderService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@Validated
@RestController
@SuppressWarnings("java:S4684")
public class FileUploaderController implements Abstract {

  private final FileUploaderService fileUploaderService;

  public FileUploaderController(FileUploaderService fileUploaderService) {
    this.fileUploaderService = fileUploaderService;
  }

  @PutMapping(path = "/file-upload-s3/{brand}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
  public ResponseEntity<String> saveCSVFileToS3(
      @PathVariable String brand,
      @ValidFileType({"csv"}) @RequestParam("file") MultipartFile file) {
    if (file.isEmpty()) {
      throw new IllegalStateException("Cannot upload empty file");
    }
    return new ResponseEntity<>(fileUploaderService.saveToS3(brand, file), HttpStatus.OK);
  }
}
