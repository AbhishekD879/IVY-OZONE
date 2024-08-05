package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.*;
import com.ladbrokescoral.oxygen.cms.api.service.impl.CacheImageServiceImpl;
import java.util.Optional;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class SvgMigrationServiceTest {

  @Mock private SvgMigrationRepository repository;
  private SvgImageService svgImageService;
  @Mock private SvgBackupRepository svgBackupRepository;
  @Mock private SvgImageRepository svgImageRepository;
  @Mock private SportCategoryRepository sportCategoryRepository;
  @Mock private FooterMenuRepository footerMenuRepository;
  @Mock private SportRepository sportRepository;
  @Mock private SportQuickLinkRepository sportQuickLinkRepository;
  @Mock private HighlightCarouselRepository highlightCarouselRepository;
  @Mock private SurfaceBetRepository surfaceBetRepository;
  @Mock private RightMenuRepository rightMenuRepository;
  @Mock private ConnectMenuRepository connectMenuRepository;
  @Mock private OddsBoostConfigurationRepository oddsBoostConfigurationRepository;
  @Mock private FooterLogoRepository footerLogoRepository;
  @Mock private VirtualSportRepository virtualSportRepository;

  private SvgMigrationService svgMigrationService;

  private ImageService imageService;

  @Mock private SvgImageParser svgImageParser;

  private SvgEntityService svgEntityService;

  @Mock private BrandCacheServiceProvider brandCacheServiceProvider;

  private SvgMigration entity;

  @Before
  public void init() {
    imageService = new CacheImageServiceImpl(brandCacheServiceProvider);
    svgEntityService = new SvgEntityService(imageService, svgImageParser);
    svgImageService =
        new SvgImageService(svgImageRepository, svgEntityService, "images/svg", svgImageParser);
    svgMigrationService =
        new SvgMigrationService(
            repository,
            svgImageService,
            svgBackupRepository,
            svgImageRepository,
            sportCategoryRepository,
            footerMenuRepository,
            sportRepository,
            sportQuickLinkRepository,
            highlightCarouselRepository,
            surfaceBetRepository,
            rightMenuRepository,
            connectMenuRepository,
            oddsBoostConfigurationRepository,
            footerLogoRepository,
            virtualSportRepository);
    String id = "67";
    entity = createEntity(id);
    when(repository.save(any())).thenReturn(entity);
    when(svgImageParser.parse(anyString(), any(MultipartFile.class), anyString()))
        .thenReturn(Optional.of(createSvg(id)));
    when(svgImageRepository.save(any(SvgImage.class))).thenReturn(createSvgImage("989398"));
  }

  private Svg createSvg(String id) {
    Svg svg = new Svg();
    svg.setSvg("svg");
    svg.setId(id);
    svg.setValue("value");
    svg.setPath("mockedpath");
    return svg;
  }

  @Test
  public void testGetBytes() throws Exception {
    CountDownLatch latch = new CountDownLatch(1);
    svgMigrationService.process(entity);
    latch.await(10, TimeUnit.SECONDS);
    verify(repository, atLeastOnce()).save(any());
  }

  private SvgImage createSvgImage(String id) {
    SvgImage image = new SvgImage();
    image.setBrand("bma");
    image.setSvgId(id);
    image.setSvg("svg");
    image.setSprite("sprite");
    image.setSvgFilename(createSvgFilenames());
    return image;
  }

  private SvgFilename createSvgFilenames() {

    SvgFilename filename = new SvgFilename();
    filename.setFiletype("svg");
    filename.setOriginalname("ogname.svg");
    filename.setPath("files/images");
    filename.setSize(1999);
    filename.setFilename("filename");
    return filename;
  }

  private SvgMigration createEntity(String id) {
    SvgMigration entity = new SvgMigration();
    entity.setBrand("bma");
    entity.setStatus("SCHEDULED");
    entity.setMessages("messages");
    entity.setId(id);
    return entity;
  }
}
