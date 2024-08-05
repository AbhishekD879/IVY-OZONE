package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackLabel;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerLabelRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceLabelService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.util.Collections;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BetPackMarketPlacePublicLabelServiceTest {

  @Mock private CustomMongoRepository<BetPackLabel> mongoRepository;
  @Mock private BetPackEnablerLabelRepository betPackEnablerLabelRepository;
  private BetPackMarketPlacePublicLabelService service;
  @Mock private ImageService imageService;

  @Before
  public void init() {
    BetPackMarketPlaceLabelService betPackMarketPlaceLabelService =
        new BetPackMarketPlaceLabelService(
            imageService, "image/path/betPackLabel", betPackEnablerLabelRepository);
    service = new BetPackMarketPlacePublicLabelService(betPackMarketPlaceLabelService);
  }

  @Test
  public void testFindUninitializedEntityByBrand() {
    // arrange
    String brand = "bma";

    BetPackLabel entity = new BetPackLabel();
    when(betPackEnablerLabelRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<BetPackLabel> list = service.getBetPackLabelByBrand(brand);

    // arrange
    assertEquals(1, list.size());
    BetPackLabel label = list.iterator().next();
    assertNull(label.getBrand());
    assertNull(label.getGoToBettingLabel());
    assertNull(label.getEndedLabel());
    assertNull(label.getDepositMessage());
    assertNull(label.getBetPackReview());
    assertNull(label.getErrorMessage());
    assertNull(label.getGoBettingURL());
    assertNull(label.getSoldOutLabel());
    assertNull(label.getMaxOnePurchasedLabel());
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "connect";

    BetPackLabel entity = new BetPackLabel();
    entity.setBrand("connect");
    entity.setBetPackReview("betPackReview");
    entity.setUseByLabel("useByLabel");
    entity.setDepositMessage("depositMessage");
    entity.setGoBettingURL("goBettingURL");
    entity.setMaxPurchasedLabel("maxPurchasedLabel");
    entity.setErrorTitle("errorTitle");

    when(betPackEnablerLabelRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(entity));

    // act
    List<BetPackLabel> list = service.getBetPackLabelByBrand(brand);

    // arrange
    assertEquals(1, list.size());
    BetPackLabel label = list.iterator().next();
    assertEquals(entity.getBrand(), label.getBrand());
    assertEquals(entity.getBetPackReview(), label.getBetPackReview());
    assertEquals(entity.getUseByLabel(), label.getUseByLabel());
    assertEquals(entity.getDepositMessage(), label.getDepositMessage());
    assertEquals(entity.getGoBettingURL(), label.getGoBettingURL());
    assertEquals(entity.getMaxPurchasedLabel(), label.getMaxPurchasedLabel());
    assertEquals(entity.getErrorTitle(), label.getErrorTitle());
  }

  @Test
  public void testFindUninitializedEntityByLabel() {

    BetPackLabel entity = new BetPackLabel();
    when(betPackEnablerLabelRepository.findAll()).thenReturn(Collections.singletonList(entity));

    // act
    List<BetPackLabel> list = service.getAllBetPackLabel();

    // arrange
    assertEquals(1, list.size());
    BetPackLabel label = list.iterator().next();
    assertNull(label.getBrand());
    assertNull(label.getGoToBettingLabel());
    assertNull(label.getEndedLabel());
    assertNull(label.getDepositMessage());
    assertNull(label.getBetPackReview());
    assertNull(label.getErrorMessage());
    assertNull(label.getGoBettingURL());
    assertNull(label.getSoldOutLabel());
    assertNull(label.getMaxOnePurchasedLabel());
  }

  @Test
  public void testFindByLabel() {

    BetPackLabel entity = new BetPackLabel();
    entity.setBrand("connect");
    entity.setBetPackReview("betPackReview");
    entity.setUseByLabel("useByLabel");
    entity.setDepositMessage("depositMessage");
    entity.setGoBettingURL("goBettingURL");
    entity.setMaxPurchasedLabel("maxPurchasedLabel");
    entity.setErrorTitle("errorTitle");

    when(betPackEnablerLabelRepository.findAll()).thenReturn(Collections.singletonList(entity));

    // act
    List<BetPackLabel> list = service.getAllBetPackLabel();

    // arrange
    assertEquals(1, list.size());
    BetPackLabel label = list.iterator().next();
    assertEquals(entity.getBrand(), label.getBrand());
    assertEquals(entity.getBetPackReview(), label.getBetPackReview());
    assertEquals(entity.getUseByLabel(), label.getUseByLabel());
    assertEquals(entity.getDepositMessage(), label.getDepositMessage());
    assertEquals(entity.getGoBettingURL(), label.getGoBettingURL());
    assertEquals(entity.getMaxPurchasedLabel(), label.getMaxPurchasedLabel());
    assertEquals(entity.getErrorTitle(), label.getErrorTitle());
  }
}
