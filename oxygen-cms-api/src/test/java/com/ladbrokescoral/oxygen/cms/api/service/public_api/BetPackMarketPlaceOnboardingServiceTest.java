package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.*;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackOnboarding;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.OnboardingImage;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackMarketplaceOnboardingRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceOnboardingService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.data.mongodb.core.MongoTemplate;

@RunWith(MockitoJUnitRunner.class)
public class BetPackMarketPlaceOnboardingServiceTest {
  @Mock private CustomMongoRepository<BetPackOnboarding> mongoRepository;

  private BetPackMarketPlacePublicOnboardingService service;

  @Mock private BetPackMarketplaceOnboardingRepository repository;

  @Mock private ImageService imageService;

  @Mock private MongoTemplate mongoTemplate;

  @Mock private ModelMapper modelMapper;

  @Before
  public void init() {

    BetPackMarketPlaceOnboardingService betPackMarketPlaceOnboardingService =
        new BetPackMarketPlaceOnboardingService(
            repository, imageService, modelMapper, "image/path/betPackOnboarding");

    service = new BetPackMarketPlacePublicOnboardingService(betPackMarketPlaceOnboardingService);
  }

  @Test
  public void testFindUninitializedEntityByBrand() {
    // arrange
    String brand = "coral";

    /// BetPackBanner entity = new BetPackBanner();
    BetPackOnboarding entity = new BetPackOnboarding();
    when(repository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<BetPackOnboarding> onboardingList = service.getBpmpOnboardingByBrand(brand);

    assertNotNull(onboardingList);
    assertEquals(1, onboardingList.size());
    BetPackOnboarding betPackOnboarding = onboardingList.iterator().next();

    // arrange
    assertNull(betPackOnboarding.getBrand());
    assertNull(betPackOnboarding.getIsActive());
    assertNull(betPackOnboarding.getCreatedByUserName());
    assertNull(betPackOnboarding.getUpdatedByUserName());
    assertNull(betPackOnboarding.getImages());
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "coral";
    Filename onbFilename = new Filename();

    BetPackOnboarding entity = new BetPackOnboarding();
    List<OnboardingImage> onboardingImages = new ArrayList<>();
    OnboardingImage onboardingImage = new OnboardingImage();
    onboardingImage.setImageType("PNG");
    onboardingImage.setNextCTAButtonLabel("NEXT");
    onboardingImage.setOnboardImageDetails(onbFilename);
    onboardingImages.add(onboardingImage);

    entity.setBrand("bma");
    entity.setIsActive(true);
    entity.setCreatedByUserName("temp");
    entity.setUpdatedByUserName("temp");
    entity.setImages(onboardingImages);

    when(repository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(entity));

    // acthandler = {InvocationNotifierHandler@3974}
    List<BetPackOnboarding> onboardingList = service.getBpmpOnboardingByBrand(brand);

    // arrange
    assertNotNull(onboardingList);
    assertEquals(1, onboardingList.size());
    BetPackOnboarding betPackOnboarding = onboardingList.iterator().next();

    assertEquals(entity.getBrand(), betPackOnboarding.getBrand());
    assertEquals(entity.getImages(), betPackOnboarding.getImages());
    assertEquals(entity.getUpdatedByUserName(), betPackOnboarding.getUpdatedByUserName());
    assertEquals(entity.getCreatedByUserName(), betPackOnboarding.getCreatedByUserName());
    assertEquals(entity.getIsActive(), betPackOnboarding.getIsActive());
  }
}
