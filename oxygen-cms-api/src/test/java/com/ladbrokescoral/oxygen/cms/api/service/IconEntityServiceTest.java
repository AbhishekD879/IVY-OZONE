package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.nio.file.Paths;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class IconEntityServiceTest extends BDDMockito {

  @Mock private ImageService imageService;
  @Spy private SportCategory sportCategory;
  @Mock private MultipartFile file;

  private ImageServiceImpl.Size smallSize = new ImageServiceImpl.Size("10x10");
  private ImageServiceImpl.Size mediumSize = new ImageServiceImpl.Size(20, 20);
  private ImageServiceImpl.Size largeSize = new ImageServiceImpl.Size("30x30");
  private Filename mockedFilename;

  private IconEntityService<SportCategory> service;

  @Before
  public void init() {

    sportCategory.setBrand("bma");

    String corePath = "testCorePath";
    service = new IconEntityService<>(imageService, corePath);
    mockedFilename = mock(Filename.class);

    doReturn(Optional.of(mockedFilename))
        .when(imageService)
        .upload(anyString(), any(), any(), any(), any());
    doReturn(Optional.of(mockedFilename))
        .when(imageService)
        .upload(anyString(), any(), any(), any());
    doReturn(Optional.of(mockedFilename))
        .when(imageService)
        .upload(anyString(), eq(file), eq(corePath));
    doReturn(Optional.empty())
        .when(imageService)
        .upload(anyString(), eq(file), eq("largeIconsPath"), eq(largeSize));

    when(mockedFilename.getFilename()).thenReturn("mockedFileName");
    when(mockedFilename.getPath()).thenReturn("mockedPath");
    when(sportCategory.getUriSmallIcon()).thenReturn("smallIconsPath");
    when(sportCategory.getUriMediumIcon()).thenReturn("mediumIconsPath");
    when(sportCategory.getUriLargeIcon()).thenReturn("largeIconsPath");
    when(sportCategory.getIcon()).thenReturn(mockedFilename);
  }

  @Test
  public void attachAllSizesIconTest() {

    Optional<SportCategory> result =
        service.attachAllSizesIcon(
            sportCategory,
            "fileName",
            file,
            ImagePath.builder()
                .smallPath("smallIconsPath")
                .mediumPath("mediumIconsPath")
                .largePath("largeIconsPath")
                .smallSize(smallSize)
                .mediumSize(mediumSize)
                .largeSize(largeSize)
                .build());

    verify(imageService, times(3)).upload(eq(sportCategory.getBrand()), any(), any(), any(), any());
    assertEquals(sportCategory, result.orElse(null));

    result =
        service.attachAllSizesIcon(
            sportCategory,
            file,
            ImagePath.builder()
                .smallPath("smallIconsPath")
                .mediumPath("mediumIconsPath")
                .largePath("largeIconsPath")
                .smallSize(smallSize)
                .mediumSize(mediumSize)
                .largeSize(largeSize)
                .build());

    verify(imageService, times(3)).upload(eq(sportCategory.getBrand()), any(), any(), any());
    assertFalse(result.isPresent());
  }

  @Test
  public void removeAllSizesIconTest() {
    Optional<SportCategory> result = service.removeAllSizesIcon(sportCategory);

    verify(imageService, times(1))
        .removeImage(sportCategory.getBrand(), sportCategory.getUriSmallIcon());
    verify(imageService, times(1))
        .removeImage(sportCategory.getBrand(), sportCategory.getUriMediumIcon());
    verify(imageService, times(1))
        .removeImage(sportCategory.getBrand(), sportCategory.getUriLargeIcon());
    verify(imageService, times(1))
        .removeImage(
            sportCategory.getBrand(),
            Paths.get(mockedFilename.getPath(), mockedFilename.getFilename()).toString());
    assertEquals(sportCategory, result.orElse(null));
  }
}