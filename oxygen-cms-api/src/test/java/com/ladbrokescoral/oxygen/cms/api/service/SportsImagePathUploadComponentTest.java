package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class SportsImagePathUploadComponentTest extends BDDMockito {

  @Mock private ImageService imageService;
  @Mock private SvgImageParser svgImageParser;

  @Mock private MultipartFile imageFile;

  private SportsImageUploadComponent component;
  private Sport sport;

  @Before
  public void init() {

    sport = new Sport();
    sport.setBrand("BMA");

    String corePath = "/images/uploads";
    Filename filename = new Filename();
    filename.setFilename("fileTest");

    given(imageService.upload(anyString(), any(MultipartFile.class), anyString()))
        .willReturn(Optional.of(filename));
    given(imageService.upload(anyString(), any(MultipartFile.class), anyString(), any()))
        .willReturn(Optional.of(filename));

    component =
        new SportsImageUploadComponent(
            imageService, svgImageParser, createSportsImageProperties(corePath), corePath);
  }

  @Test
  public void testSportsImageCreatedWithDefaultSizes() {

    component.setDefaultImageSizes(sport);

    assertEquals(Integer.valueOf(110), sport.getHeightSmall());
    assertEquals(Integer.valueOf(210), sport.getHeightMedium());
    assertEquals(Integer.valueOf(310), sport.getHeightLarge());
    assertEquals(Integer.valueOf(100), sport.getWidthSmall());
    assertEquals(Integer.valueOf(200), sport.getWidthMedium());
    assertEquals(Integer.valueOf(300), sport.getWidthLarge());

    assertEquals(Integer.valueOf(11), sport.getHeightSmallIcon());
    assertEquals(Integer.valueOf(21), sport.getHeightMediumIcon());
    assertEquals(Integer.valueOf(31), sport.getHeightLargeIcon());
    assertEquals(Integer.valueOf(10), sport.getWidthSmallIcon());
    assertEquals(Integer.valueOf(20), sport.getWidthMediumIcon());
    assertEquals(Integer.valueOf(30), sport.getWidthLargeIcon());
  }

  @Test
  public void testUploadImage() {

    component.attachImages(sport, imageFile, null, null);

    Mockito.verify(imageService).upload(sport.getBrand(), imageFile, "/images/uploads");
    Mockito.verify(imageService)
        .upload(sport.getBrand(), imageFile, "/small", new ImageServiceImpl.Size("100x110"));
    Mockito.verify(imageService)
        .upload(sport.getBrand(), imageFile, "/medium", new ImageServiceImpl.Size("200x210"));
    Mockito.verify(imageService)
        .upload(sport.getBrand(), imageFile, "/large", new ImageServiceImpl.Size("300x310"));

    assertEquals("/small/fileTest", sport.getUriSmall());
    assertEquals("/medium/fileTest", sport.getUriMedium());
    assertEquals("/large/fileTest", sport.getUriLarge());
  }

  @Test
  public void testUploadIcon() {

    component.attachImages(sport, null, imageFile, null);

    Mockito.verify(imageService).upload(sport.getBrand(), imageFile, "/images/uploads");
    Mockito.verify(imageService)
        .upload(sport.getBrand(), imageFile, "/icons/small", new ImageServiceImpl.Size("10x11"));
    Mockito.verify(imageService)
        .upload(sport.getBrand(), imageFile, "/icons/medium", new ImageServiceImpl.Size("20x21"));
    Mockito.verify(imageService)
        .upload(sport.getBrand(), imageFile, "/icons/large", new ImageServiceImpl.Size("30x31"));

    assertEquals("/icons/small/fileTest", sport.getUriSmallIcon());
    assertEquals("/icons/medium/fileTest", sport.getUriMediumIcon());
    assertEquals("/icons/large/fileTest", sport.getUriLargeIcon());
  }

  @Test
  public void testSvgIconUpload() {

    Svg svg = new Svg();
    svg.setId("123");
    svg.setSvg("<svg>test</svg>");

    Mockito.when(svgImageParser.parse(any())).thenReturn(Optional.of(svg));

    component.attachImages(sport, null, null, imageFile);
    Mockito.verify(imageService).upload(sport.getBrand(), imageFile, "/images/uploads/sports");

    assertEquals("<svg>test</svg>", sport.getSvg());
    assertEquals("123", sport.getSvgId());
    assertEquals("/images/uploads/sports", sport.getSvgFilename().getPath());
  }

  @Test
  public void testRemoveImages() {

    sport.setUriSmall("/small");
    sport.setUriMedium("/medium");
    sport.setUriLarge("/large");
    sport.setUriSmallIcon("/icons/small");
    sport.setUriMediumIcon("/icons/medium");
    sport.setUriLargeIcon("/icons/large");
    Filename svgFile = new Filename();
    svgFile.setPath("/svg");
    svgFile.setFilename("svgFile");
    sport.setSvgFilename(svgFile);
    sport.setFilename(new Filename());
    sport.setSvg("");
    sport.setSvgId("");
    sport.setIcon(new Filename());

    component.deleteImages(SportsImageUploadComponent.SportsImage.validValues(), sport);

    Mockito.verify(imageService).removeImage(sport.getBrand(), "/large");
    Mockito.verify(imageService).removeImage(sport.getBrand(), "/medium");
    Mockito.verify(imageService).removeImage(sport.getBrand(), "/small");

    Mockito.verify(imageService).removeImage(sport.getBrand(), "/icons/large");
    Mockito.verify(imageService).removeImage(sport.getBrand(), "/icons/medium");
    Mockito.verify(imageService).removeImage(sport.getBrand(), "/icons/small");

    Mockito.verify(imageService).removeImage(sport.getBrand(), "/svg/svgFile");

    assertNull(sport.getUriSmall());
    assertNull(sport.getUriMedium());
    assertNull(sport.getUriLarge());
    assertNull(sport.getUriSmallIcon());
    assertNull(sport.getUriMediumIcon());
    assertNull(sport.getUriLargeIcon());
    assertNull(sport.getSvgFilename());
    assertNull(sport.getSvg());
    //    assertNull(sport.getSvgId());
    assertNull(sport.getFilename());
    assertNull(sport.getIcon());
  }

  private SportImagesProperties createSportsImageProperties(String corePath) {
    return SportImagesProperties.builder()
        .path(corePath + "/sports")
        .small(SportImagesProperties.SizedImage.builder().path("/small").size("100x110").build())
        .medium(SportImagesProperties.SizedImage.builder().path("/medium").size("200x210").build())
        .large(SportImagesProperties.SizedImage.builder().path("/large").size("300x310").build())
        .icons(
            SportImagesProperties.IconImageProperties.builder()
                .small(
                    SportImagesProperties.SizedImage.builder()
                        .path("/icons/small")
                        .size("10x11")
                        .build())
                .medium(
                    SportImagesProperties.SizedImage.builder()
                        .path("/icons/medium")
                        .size("20x21")
                        .build())
                .large(
                    SportImagesProperties.SizedImage.builder()
                        .path("/icons/large")
                        .size("30x31")
                        .build())
                .build())
        .build();
  }
}
