package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Promotions.PromotionIdNotUniqueException;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Promotions.PromotionKeyNotUniqueException;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import java.io.*;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class PromotionsControllerTest extends BDDMockito {

  @Rule public ExpectedException exceptionRule = ExpectedException.none();

  // Controler Mocks
  @Mock private PromotionService service; // FIXME: don't mock service, mock repository
  @Mock private WysiwygService wysiwygService;
  @Mock private PromotionSectionService sectionService;
  @Mock private PromoLeaderboardValidationService promoLeaderboardValidationService;
  // Global Mocks
  @Mock private UserService userService;

  // Test Mocks
  @Mock private MultipartFile file;

  @InjectMocks private Promotions controller;

  @Before
  public void initTest() {}

  @Test(expected = PromotionIdNotUniqueException.class)
  public void createWhenPromotionIdIsDuplicateThenThrowException() throws Exception {

    final Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    doReturn(Optional.ofNullable(promotion))
        .when(service)
        .findByBrandAndPromotionId(anyString(), anyString());

    controller.create(promotion);

    verify(service, times(1)).findByBrandAndPromotionId("bma", "124");
    verify(service, times(0)).save(any(Promotion.class));
  }

  @Test
  public void testCreatePromotionWithDuplicatePromoKey() throws Exception {

    exceptionRule.expect(PromotionKeyNotUniqueException.class);

    final Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    Assert.assertNotNull(promotion);

    doReturn(Optional.empty()).when(service).findByBrandAndPromotionId(anyString(), anyString());
    doReturn(Optional.of(promotion)).when(service).findByBrandAndPromoKey(anyString(), anyString());

    controller.create(promotion);

    verify(service, times(1)).findByBrandAndPromoKey(promotion.getBrand(), promotion.getPromoKey());
    verify(service, times(0)).save(any(Promotion.class));
  }

  @Test
  public void testCreatePromotionWithLbr() throws Exception {
    Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    promotion.setNavigationGroupId("NG1");
    when(service.save((Promotion) any())).thenReturn(promotion);

    controller.create(promotion);
    verify(service, times(0)).save(any(Promotion.class));
  }

  @Test
  public void testCreatePromotionWithoutNavGroup() throws Exception {
    Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    when(service.save((Promotion) any())).thenReturn(promotion);
    controller.create(promotion);
    verify(service, times(0)).save(any(Promotion.class));
  }

  @Test
  public void testCreatePromotionWithNavGroupEmpty() throws Exception {
    Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    promotion.setNavigationGroupId("");
    when(service.save((Promotion) any())).thenReturn(promotion);
    controller.create(promotion);
    verify(service, times(0)).save(any(Promotion.class));
  }

  @Test
  public void testUpdatePromotionWithNewNavG() throws Exception {
    Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    promotion.setNavigationGroupId("NG1");
    when(service.findOne(any())).thenReturn(Optional.of(promotion));

    Promotion promotion1 =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard1.json", Promotion.class);
    promotion1.setNavigationGroupId("NG2");
    when(service.update(any(), any())).thenReturn(promotion1);
    controller.update(promotion1.getId(), promotion1);
    Assert.assertNotNull(promotion);
  }

  @Test
  public void testUpdatePromotionWithExistingNavGNull() throws Exception {
    Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    when(service.findOne(any())).thenReturn(Optional.of(promotion));

    Promotion promotion1 =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard1.json", Promotion.class);
    promotion1.setNavigationGroupId("NG2");
    when(service.update(any(), any())).thenReturn(promotion1);
    controller.update(promotion.getId(), promotion1);
    Assert.assertNotNull(promotion);
  }

  @Test
  public void testUpdatePromotionWhenNavGSame() throws Exception {
    Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    promotion.setNavigationGroupId("NG1");
    when(service.findOne(any())).thenReturn(Optional.of(promotion));

    Promotion promotion1 =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard1.json", Promotion.class);
    promotion1.setNavigationGroupId("NG1");
    when(service.update(any(), any())).thenReturn(promotion1);
    controller.update(promotion.getId(), promotion1);
    Assert.assertNotNull(promotion);
  }

  @Test
  public void testUpdatePromotionWithNewNavGNull() throws Exception {
    Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    when(service.findOne(any())).thenReturn(Optional.of(promotion));

    Promotion promotion1 =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard1.json", Promotion.class);
    when(service.update(any(), any())).thenReturn(promotion1);
    controller.update(promotion.getId(), promotion1);
    Assert.assertNotNull(promotion);
  }

  @Test
  public void testUpdatePromotionWithNewNavGEmpty() throws Exception {
    Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    when(service.findOne(any())).thenReturn(Optional.of(promotion));

    Promotion promotion1 =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard1.json", Promotion.class);
    promotion1.setNavigationGroupId("");
    when(service.update(any(), any())).thenReturn(promotion1);
    controller.update(promotion1.getId(), promotion1);
    Assert.assertNotNull(promotion);
  }

  @Test
  public void updateWhenPromotionIdIsDuplicateThenThrowException() throws Exception {

    exceptionRule.expect(PromotionIdNotUniqueException.class);

    final Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    doReturn(Optional.of(new Promotion()))
        .when(service)
        .findByBrandAndPromotionId(anyString(), anyString());

    controller.update(promotion.getId(), promotion);
  }

  @Test
  public void testUpdatePromotionWithDuplicatePromoKey() throws Exception {

    exceptionRule.expect(PromotionKeyNotUniqueException.class);

    final Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    Assert.assertNotNull(promotion);

    doReturn(Optional.empty()).when(service).findByBrandAndPromotionId(anyString(), anyString());
    doReturn(Optional.of(new Promotion()))
        .when(service)
        .findByBrandAndPromoKey(anyString(), anyString());

    controller.update(promotion.getId(), promotion);
  }

  @Test
  public void updateWhenPromotionIdIsChangedOnNull() throws Exception {

    final Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/whenPromotionIdsIsNull.json", Promotion.class);

    doReturn(
            Optional.ofNullable(
                TestUtil.deserializeWithJackson(
                    "controller/private_api/promotions/standard.json", Promotion.class)))
        .when(service)
        .findOne(anyString());

    doReturn(promotion).when(service).update(any(), any());
    doReturn(Optional.of(new User())).when(userService).findOne(any());
    doReturn(Optional.empty()).when(service).findByBrandAndPromoKey(anyString(), anyString());
    doNothing().when(sectionService).deletePromotionIdInSections("bma", "124");

    controller.update(promotion.getId(), promotion);

    verify(sectionService, times(1)).deletePromotionIdInSections(anyString(), anyString());
  }

  @Test
  public void delete() throws Exception {

    final Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    doReturn(Optional.ofNullable(promotion)).when(service).findOne(anyString());

    doReturn(Optional.ofNullable(promotion)).when(service).removeImage(any());
    doReturn(promotion).when(service).save(any(Promotion.class));

    doNothing().when(service).delete(anyString());

    doNothing().when(sectionService).deletePromotionIdInSections("bma", "124");

    controller.delete("1");

    verify(sectionService, times(1)).deletePromotionIdInSections(anyString(), anyString());
  }

  @Test
  public void updateWhenPromotionIdIsChangedOnNew() throws Exception {

    final Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard1.json", Promotion.class);
    doReturn(Optional.empty()).when(service).findByBrandAndPromotionId(anyString(), anyString());
    doReturn(
            Optional.ofNullable(
                TestUtil.deserializeWithJackson(
                    "controller/private_api/promotions/standard.json", Promotion.class)))
        .when(service)
        .findOne(anyString());

    doReturn(promotion).when(service).update(any(), any());
    doReturn(Optional.of(new User())).when(userService).findOne(any());
    doReturn(Optional.empty()).when(service).findByBrandAndPromoKey(anyString(), anyString());

    doNothing().when(sectionService).updatePromotionIdInSections("bma", "124", "125");

    controller.update(promotion.getId(), promotion);

    verify(sectionService, times(1)).updatePromotionIdInSections("bma", "124", "125");
  }

  @Test
  public void testUploadTableCSVFile() throws IOException {
    ClassLoader classloader = Thread.currentThread().getContextClassLoader();
    InputStream inputStream =
        classloader.getResourceAsStream(
            "com/ladbrokescoral/oxygen/cms/api/controller/private_api/promotions/PromotionsTableUpload.csv");
    MultipartFile file = new MockMultipartFile("PromotionsTableUpload.csv", inputStream);

    ResponseEntity<List<Map<String, String>>> response = controller.uploadTableCSVFile(file);

    Assert.assertTrue(response.getStatusCode().is2xxSuccessful());
  }

  @Test
  public void readall() throws Exception {
    final Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    doReturn(Arrays.asList(promotion)).when(service).findAllSorted();
    controller.readAll();
    verify(service, times(1)).findAllSorted();
  }

  @Test
  public void readall1() throws Exception {

    final Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    doReturn(Optional.of(promotion)).when(service).findOne(anyString());
    controller.read(promotion.getId());
    verify(service, times(1)).findOne(anyString());
  }

  @Test
  public void readByBrand() throws Exception {
    final Promotion promotion =
        TestUtil.deserializeWithJackson(
            "controller/private_api/promotions/standard.json", Promotion.class);
    doReturn(Arrays.asList(promotion)).when(service).findByBrand(anyString());
    controller.readByBrand(promotion.getId());
    verify(service, times(1)).findByBrand(anyString());
  }
}
