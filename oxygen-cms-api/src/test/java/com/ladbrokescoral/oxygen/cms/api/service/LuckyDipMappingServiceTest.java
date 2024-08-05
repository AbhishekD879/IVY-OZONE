package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipMapping;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.repository.LuckyDipMappingRepository;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(MockitoJUnitRunner.class)
public class LuckyDipMappingServiceTest {

  @Mock LuckyDipMappingRepository repository;

  @InjectMocks LuckyDipMappingService luckyDipMappingService;

  List<LuckyDipMapping> existingLuckyDipMappings;
  String brand;

  @Before
  public void setUp() throws Exception {
    brand = "bma";

    existingLuckyDipMappings =
        TestUtil.deserializeListWithJackson(
            "service/luckyDip/existingLuckyDipMappings.json", LuckyDipMapping.class);

    when(repository.findByBrandAndActiveTrueOrderBySortOrderAsc(any()))
        .thenReturn(existingLuckyDipMappings);
  }

  @Test(expected = BadRequestException.class)
  public void tstDuplicateCategoryId() throws IOException {
    LuckyDipMapping luckyDipMapping =
        TestUtil.deserializeWithJackson(
            "service/luckyDip/LdMappingWithDuplicateCategoryId.json", LuckyDipMapping.class);

    luckyDipMappingService.validateCategoryAndTypeIds(luckyDipMapping);
  }

  @Test(expected = BadRequestException.class)
  public void tstDuplicatedCurrentTypeIds() throws IOException {
    ReflectionTestUtils.setField(luckyDipMappingService, "enableTypeIdsValidation", true);
    LuckyDipMapping luckyDipMapping =
        TestUtil.deserializeWithJackson(
            "service/luckyDip/LdMappingWithDuplicateCurrentTypeIds.json", LuckyDipMapping.class);

    luckyDipMappingService.validateCategoryAndTypeIds(luckyDipMapping);
  }

  @Test(expected = InvocationTargetException.class)
  public void tstMaxTypeIdsLimitExceeds() throws Exception {
    Method method =
        LuckyDipMappingService.class.getDeclaredMethod(
            "validateTypeIdCount", LuckyDipMapping.class);
    method.setAccessible(true);
    LuckyDipMapping luckyDipMapping =
        TestUtil.deserializeWithJackson(
            "service/luckyDip/LdMappingWithMaxTypeIds.json", LuckyDipMapping.class);

    method.invoke(luckyDipMappingService, luckyDipMapping);
  }

  @Test(expected = BadRequestException.class)
  public void tstDuplicatedTypeIds() throws IOException {
    ReflectionTestUtils.setField(luckyDipMappingService, "enableTypeIdsValidation", true);
    LuckyDipMapping luckyDipMapping =
        TestUtil.deserializeWithJackson(
            "service/luckyDip/LdMappingWithDuplicateTypeIds.json", LuckyDipMapping.class);

    luckyDipMappingService.validateCategoryAndTypeIds(luckyDipMapping);
  }

  @Test
  public void tstCreateWithNoDuplicates() throws IOException {
    ReflectionTestUtils.setField(luckyDipMappingService, "enableTypeIdsValidation", true);
    LuckyDipMapping luckyDipMapping =
        TestUtil.deserializeWithJackson(
            "service/luckyDip/LdMappingWithNoDuplicates.json", LuckyDipMapping.class);

    Assert.assertNotNull(luckyDipMappingService);
    luckyDipMappingService.validateCategoryAndTypeIds(luckyDipMapping);
  }

  @Test
  public void tstLdMappingUpdate() throws IOException {
    LuckyDipMapping luckyDipMapping =
        TestUtil.deserializeWithJackson(
            "service/luckyDip/LDMappingUpdateEntity.json", LuckyDipMapping.class);

    Assert.assertNotNull(luckyDipMappingService);
    luckyDipMappingService.validateCategoryAndTypeIds(luckyDipMapping);
  }

  @Test
  public void tstLdMappingUpdateWithWrongId() throws IOException {
    LuckyDipMapping luckyDipMapping =
        TestUtil.deserializeWithJackson(
            "service/luckyDip/LDMappingUpdateEntity.json", LuckyDipMapping.class);
    luckyDipMapping.setId("1234");

    Assert.assertNotNull(luckyDipMappingService);
    luckyDipMappingService.validateCategoryAndTypeIds(luckyDipMapping);
  }

  @Test
  public void tstWhenActiveFlagFalse() throws IOException {
    LuckyDipMapping luckyDipMapping =
        TestUtil.deserializeWithJackson(
            "service/luckyDip/LdMappingWithDuplicateCategoryId.json", LuckyDipMapping.class);
    luckyDipMapping.setActive(false);

    Assert.assertNotNull(luckyDipMappingService);
    luckyDipMappingService.validateCategoryAndTypeIds(luckyDipMapping);
  }

  @Test
  public void tstGetAllLuckyDipMappingsByBrand() {
    List<LuckyDipMapping> allLuckyDipMappingsByBrand =
        luckyDipMappingService.getAllLuckyDipMappingsByBrand(brand);
    Assert.assertEquals(existingLuckyDipMappings, allLuckyDipMappingsByBrand);
  }
}
