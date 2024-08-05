package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterLogo;
import com.ladbrokescoral.oxygen.cms.api.repository.FooterLogoRepository;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class FooterLogoServiceTest {

  @Mock private FooterLogoRepository repository;
  @Mock private ImageService imageService;
  @Mock private SvgEntityService<FooterLogo> svgEntityService;
  private String mediumMenusPath = "mediumMenusPath";
  private String originalMenusPath = "originalMenusPath";
  private String svgMenuPath = "svgMenuPath";
  FooterLogoService service;
  private FooterLogo footerLogo;
  @Mock MultipartFile file;
  @Mock MultipartFile errorFile;
  @Mock MultipartFile svgFile;
  @Mock Filename filename;

  @Before
  public void init() throws Exception {
    service =
        new FooterLogoService(
            repository,
            imageService,
            svgEntityService,
            mediumMenusPath,
            originalMenusPath,
            svgMenuPath);

    footerLogo = TestUtil.deserializeWithJackson("test/footer.json", FooterLogo.class);
    doReturn("filename").when(filename).getFilename();
    doReturn(Optional.of(filename))
        .when(imageService)
        .upload(footerLogo.getBrand(), file, mediumMenusPath, null);
    doReturn(Optional.of(filename))
        .when(imageService)
        .upload(footerLogo.getBrand(), file, originalMenusPath, null);
    doReturn(Optional.empty())
        .when(imageService)
        .upload(footerLogo.getBrand(), errorFile, originalMenusPath, null);
    doReturn(Optional.ofNullable(filename))
        .when(imageService)
        .upload(footerLogo.getBrand(), errorFile, mediumMenusPath, null);
  }

  @Test
  public void findByBrandTest() {
    String brand = "testBrand";
    doReturn(Collections.singletonList(footerLogo))
        .when(repository)
        .findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
    List<FooterLogo> footerLogos = service.findAllByBrandAndDisabled(brand);
    verify(repository, times(1)).findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
    assertTrue(footerLogos.contains(footerLogo));
  }

  @Test
  public void attachImageTest() {
    footerLogo.setUriMedium(null);
    footerLogo.setFilename(null);
    Optional<FooterLogo> footerLogoOpt = service.attachImage(footerLogo, file);
    assertTrue(footerLogoOpt.isPresent());
    assertNotNull(footerLogoOpt.get().getUriMedium());
    assertNotNull(footerLogoOpt.get().getFilename());
    footerLogoOpt = service.attachImage(footerLogo, errorFile);
    assertFalse(footerLogoOpt.isPresent());
  }

  @Test
  public void removeImageTest() {

    assertNotNull(footerLogo.getUriMedium());
    assertNotNull(footerLogo.getUriOriginal());
    String uriMedium = footerLogo.getUriMedium();
    String uriOrigin = footerLogo.getUriOriginal();

    Optional<FooterLogo> footerLogoOpt = service.removeImage(footerLogo);

    verify(imageService).removeImage(footerLogo.getBrand(), uriMedium);
    verify(imageService).removeImage(footerLogo.getBrand(), uriOrigin);
    assertNull(footerLogoOpt.get().getUriMedium());
    assertNull(footerLogoOpt.get().getUriOriginal());
  }

  @Test
  public void svgTest() {
    Optional<FooterLogo> footerLogoOpt = service.attachSvgImage(footerLogo, svgFile);
    verify(svgEntityService).attachSvgImage(footerLogo, svgFile, svgMenuPath);

    footerLogoOpt = service.removeSvgImage(footerLogo);
    verify(svgEntityService).removeSvgImage(footerLogo);
  }
}
