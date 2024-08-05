package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.TimelineFileType;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Template;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelinePostPageRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineTemplateRepository;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class TimelineTemplateServiceTest extends BDDMockito {

  public static final String TEMPLATE_ID = "3454332234";
  public static final String TIMELINE_IMAGE_PATH = "/image/path";

  private TimelineTemplateService service;

  @Mock TimelineTemplateRepository repository;

  @Mock TimelinePostPageRepository postsRepository;

  @Mock ImageService imageService;

  @Mock SvgImageParser imageParser;

  Template template;

  @Mock MultipartFile imageFile;

  @Mock MultipartFile svgImageFile;

  Filename uploadedImageInfo;

  @Before
  public void setUp() {
    template = new Template();
    template.setId(TEMPLATE_ID);
    template.setBrand("ladbrokes");

    uploadedImageInfo = new Filename();
    when(imageService.upload(anyString(), any(MultipartFile.class), anyString()))
        .thenReturn(Optional.of(uploadedImageInfo));

    when(imageParser.parse(any(MultipartFile.class))).thenReturn(Optional.of(new Svg()));

    service =
        new TimelineTemplateService(
            repository, postsRepository, imageService, imageParser, TIMELINE_IMAGE_PATH);
  }

  @Test
  public void testAttachingTopRightCornerImage() {
    service.uploadAndSetRightCornerImage(template, imageFile);

    verify(imageService).upload(template.getBrand(), imageFile, TIMELINE_IMAGE_PATH);
    verify(repository).save(template);
    assertEquals(uploadedImageInfo, template.getTopRightCornerImage());
  }

  @Test(expected = FileUploadException.class)
  public void testAttachingTopRightCornerImageFailedUploading() {
    when(imageService.upload(anyString(), any(MultipartFile.class), anyString()))
        .thenReturn(Optional.empty());

    service.uploadAndSetRightCornerImage(template, imageFile);
  }

  @Test(expected = FileUploadException.class)
  public void testAttachingHeaderIconSvgImageUploadingFailure() {
    when(imageService.upload(anyString(), any(MultipartFile.class), anyString()))
        .thenReturn(Optional.empty());

    service.uploadAndSetSvgImage(template, svgImageFile);
  }

  @Test
  public void testAttachingTopRightCornerSvgImage() {
    service.uploadAndSetSvgImage(template, svgImageFile);

    verify(imageParser).parse(svgImageFile);
    verify(imageService).upload(template.getBrand(), svgImageFile, TIMELINE_IMAGE_PATH);
    verify(repository).save(template);
    assertEquals(uploadedImageInfo, template.getTopRightCornerImage());
  }

  @Test(expected = FileUploadException.class)
  public void testDeletingTrcImageFailure() {

    Filename imageFile = new Filename();
    imageFile.setPath("/path/");
    imageFile.setFilename("filename");
    template.setTopRightCornerImage(imageFile);

    service.deleteImage(template, TimelineFileType.TOP_RIGHT_CORNER);
  }

  @Test(expected = BadRequestException.class)
  public void testAttachingSvgImageParsingError() {
    when(imageParser.parse(any(MultipartFile.class))).thenReturn(Optional.empty());

    service.uploadAndSetSvgImage(template, svgImageFile);
  }

  @Test(expected = BadRequestException.class)
  public void testAttachingSvgImageParsingException() {
    when(imageParser.parse(any(MultipartFile.class))).thenThrow(new SvgImageParseException());

    service.uploadAndSetSvgImage(template, svgImageFile);
  }

  @Test
  public void testDeletingTopRightCornerImage() {

    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);

    Filename imageFile = new Filename();
    imageFile.setPath("/path/");
    imageFile.setFilename("filename");
    imageFile.setFullPath("/fullPath/path");
    template.setTopRightCornerImage(imageFile);

    service.deleteImage(template, TimelineFileType.TOP_RIGHT_CORNER);

    verify(imageService).removeImage(anyString(), anyString());
  }

  @Test
  public void testDeletingHeaderIconImage() {
    template.setPostIconSvgId("466445");

    service.deleteImage(template, TimelineFileType.HEADER_ICON);

    assertNull(template.getPostIconSvgId());
  }
}
