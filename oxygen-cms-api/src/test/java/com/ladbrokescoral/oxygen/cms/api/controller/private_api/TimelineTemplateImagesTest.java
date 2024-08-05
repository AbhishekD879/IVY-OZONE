package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertEquals;

import com.ladbrokescoral.oxygen.cms.api.entity.TimelineFileType;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Template;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineTemplateService;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class TimelineTemplateImagesTest extends BDDMockito {

  public static final String TEMPLATE_ID = "98789987";
  public static final String BRAND = "ladbrokes";

  @Mock private MultipartFile multipartFile;
  @Mock private TimelineTemplateService templateService;

  private Template template;

  @InjectMocks private TimelineTemplateController controller;

  @Before
  public void init() {

    template = new Template();
    template.setId(TEMPLATE_ID);

    when(templateService.findOne(any())).thenReturn(Optional.of(template));
  }

  @Test
  public void testGetByBrand() {
    when(templateService.findByBrand(any())).thenReturn(Arrays.asList());

    controller.getTemplatesByBrand(BRAND);

    verify(templateService).findByBrand(BRAND);
  }

  @Test
  public void testSvgImageUploading() {
    when(multipartFile.getOriginalFilename()).thenReturn("sth.svg");

    controller.uploadImage(TEMPLATE_ID, "HEADER_ICON", multipartFile);

    verify(templateService).uploadAndSetSvgImage(template, multipartFile);
  }

  @Test
  public void testJpgImageUploading() {
    when(multipartFile.getOriginalFilename()).thenReturn("sth.jpg");

    controller.uploadImage(TEMPLATE_ID, "HEADER_ICON", multipartFile);

    verify(templateService).uploadAndSetRightCornerImage(template, multipartFile);
  }

  @Test
  public void testUploadingImageForUnexistingTemplate() {
    when(templateService.findOne(any())).thenReturn(Optional.empty());

    ResponseEntity<Template> responseEntity =
        controller.uploadImage(TEMPLATE_ID, "HEADER_ICON", multipartFile);

    verify(templateService, times(0)).uploadAndSetRightCornerImage(any(), any());
    assertEquals(HttpStatus.NOT_FOUND, responseEntity.getStatusCode());
  }

  @Test
  public void testDeleteImage() {
    controller.deleteTimelineImageForTemplate(TEMPLATE_ID, "HEADER_ICON");

    verify(templateService).deleteImage(template, TimelineFileType.HEADER_ICON);
  }

  @Test
  public void testDeleteImageForUnexistingTemplate() {
    when(templateService.findOne(any())).thenReturn(Optional.empty());

    ResponseEntity<Template> responseEntity =
        controller.deleteTimelineImageForTemplate(TEMPLATE_ID, "HEADER_ICON");

    verify(templateService, times(0)).deleteImage(any(), any());
    assertEquals(HttpStatus.NOT_FOUND, responseEntity.getStatusCode());
  }
}
