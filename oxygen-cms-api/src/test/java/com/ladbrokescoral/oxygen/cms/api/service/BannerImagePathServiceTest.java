package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.Matchers.any;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.entity.Banner;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.service.impl.BannerImageService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl.Size;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.io.IOException;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.web.multipart.MultipartFile;

public class BannerImagePathServiceTest {

  private static final String IMAGE_JPG = "image/jpg";
  private static final Long SIZE = 100L;
  private static final String IMAGES_UPLOADS = "/images/uploads";
  private static final String SMALL_BANNERS_PATH = "/images/uploads/banners/small";
  private static final String MEDIUM_BANNERS_PATH = "/images/uploads/banners/medium";
  private static final String DESKTOP_BANNERS_PATH = "/images/uploads/banners/desktop";

  private static final String SMALL = "640x200";
  private static final String MEDIUM = "491x190";
  private static final String DESKTOP = "720x150";

  @Mock private MultipartFile testFile;
  @Mock private ImageServiceImpl imageService;

  @Mock private Filename filenameMock;

  @Mock private Banner bannerMock;

  private BannerImageService bannerImageService;

  @Before
  public void init() throws IOException {
    MockitoAnnotations.initMocks(this);

    when(testFile.getContentType()).thenReturn(IMAGE_JPG);
    when(testFile.getOriginalFilename()).thenReturn("file.jpg");
    when(testFile.getSize()).thenReturn(SIZE);
    when(testFile.getBytes()).thenReturn(new byte[] {1, 1, 1});

    bannerImageService =
        new BannerImageService(
            imageService,
            ImagePath.builder()
                .smallPath(SMALL_BANNERS_PATH)
                .imagesCorePath(IMAGES_UPLOADS)
                .mediumPath(MEDIUM_BANNERS_PATH)
                .largePath(DESKTOP_BANNERS_PATH)
                .smallSize(new Size(SMALL))
                .mediumSize(new Size(MEDIUM))
                .largeSize(new Size(DESKTOP))
                .build());
  }

  @Test
  public void updateMediumAndSmallImagesTest() {
    when(bannerMock.getBrand()).thenReturn("bma");
    when(filenameMock.getFilename()).thenReturn("");
    when(imageService.upload(eq(bannerMock.getBrand()), any(), any(), any()))
        .thenReturn(Optional.of(filenameMock));
    bannerImageService.updateMediumAndSmallImages(bannerMock, testFile);
    verify(filenameMock, times(2)).getFilename();
    verify(bannerMock).setUriSmall(any());
    verify(bannerMock).setUriMedium(any());
    verify(bannerMock).setFilename(any());
  }

  @Test
  public void updateImagesRcombTest() {
    when(bannerMock.getBrand()).thenReturn("rcomb");
    when(filenameMock.getFilename()).thenReturn("");
    when(imageService.upload(eq(bannerMock.getBrand()), any(), any(), any()))
        .thenReturn(Optional.of(filenameMock));
    bannerImageService.updateMediumAndSmallImages(bannerMock, testFile);
    verify(bannerMock, times(0)).setUriSmall(any());
    verify(bannerMock, times(0)).setUriMedium(any());
    verify(bannerMock).setFilename(any());
  }

  @Test
  public void updateDesktopImageTest() {
    when(bannerMock.getBrand()).thenReturn("bma");
    when(filenameMock.getFilename()).thenReturn("");
    when(imageService.upload(eq(bannerMock.getBrand()), any(), any(), any()))
        .thenReturn(Optional.of(filenameMock));
    bannerImageService.updateDesktopImage(bannerMock, testFile);
    verify(filenameMock, times(1)).getFilename();
    verify(bannerMock).setDesktopUriMedium(any());
    verify(bannerMock).setDesktopFilename(any());
  }

  @Test
  public void updateDesktopImageRcombTest() {
    when(bannerMock.getBrand()).thenReturn("rcomb");
    when(filenameMock.getFilename()).thenReturn("");
    when(imageService.upload(eq(bannerMock.getBrand()), any(), any(), any()))
        .thenReturn(Optional.of(filenameMock));
    bannerImageService.updateDesktopImage(bannerMock, testFile);
    verify(bannerMock, times(0)).setDesktopUriMedium(any());
    verify(bannerMock).setDesktopFilename(any());
  }

  @Test
  public void removeMediumAndSmallImagesTest() {
    when(imageService.removeImage(anyString(), any())).thenReturn(true);
    when(bannerMock.getUriSmall()).thenReturn("");
    when(bannerMock.getUriMedium()).thenReturn("");

    bannerImageService.removeMediumAndSmallImages(bannerMock);
    verify(bannerMock).setUriSmall(null);
    verify(bannerMock).setUriMedium(null);
  }

  @Test
  public void removeDesktopImageTest() {
    when(imageService.removeImage(anyString(), any())).thenReturn(true);
    when(bannerMock.getDesktopUriMedium()).thenReturn("");

    bannerImageService.removeDesktopImage(bannerMock);
    verify(bannerMock).setDesktopUriMedium(null);
  }
}
