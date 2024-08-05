package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.TestUtil.deserializeWithJackson;
import static org.junit.Assert.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.InvalidPageNameException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.ApiCollectionConfigRepository;
import java.io.IOException;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class ApiCollectionConfigServiceTest extends BDDMockito {

  @InjectMocks private ApiCollectionConfigService apiCollectionConfigService;
  @Mock private ApiCollectionConfigRepository apiCollectionConfigRepository;
  @Mock CrudService<User> userServiceObj;
  private ApiCollectionConfig createApiCollectionConfig;

  @Before
  public void init() throws IOException {
    createApiCollectionConfig =
        deserializeWithJackson(
            "controller/private_api/apicollectionconfig/createApiCollectionConfig.json",
            ApiCollectionConfig.class);
    apiCollectionConfigService = new ApiCollectionConfigService(apiCollectionConfigRepository);
  }

  @Test
  public void testFindAllByBrand() {
    when(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .thenReturn(Optional.of(Arrays.asList(createApiCollectionConfig)));
    assertNotNull(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()));
  }

  @Test
  public void testFindByBrandAndColumn() {
    when(apiCollectionConfigRepository.findConfigMapByAndColumn(
            anyString(), anyString(), anyString()))
        .thenReturn(Optional.of(createApiCollectionConfig));
    assertNotNull(
        apiCollectionConfigService.findConfigMapByBrandAndColumn(
            anyString(), anyString(), anyString()));
  }

  @Test
  public void testFindByBrandAndColumnNotPresent() {
    when(apiCollectionConfigRepository.findConfigMapByAndColumn(
            anyString(), anyString(), anyString()))
        .thenReturn(Optional.empty());
    assertNotNull(
        apiCollectionConfigService.findConfigMapByBrandAndColumn(
            anyString(), anyString(), anyString()));
  }

  @Test
  public void testDeleteByBrandAndColumn() throws Exception {
    when(apiCollectionConfigRepository.findConfigMapByAndColumn(
            "ladbrokes", "id", "6284cf4860f795132aa9f05c"))
        .thenReturn(Optional.of(createApiCollectionConfig));
    apiCollectionConfigService.deleteByBrandAndColumn(
        "ladbrokes", "id", "6284cf4860f795132aa9f05c");
    assertNotNull(apiCollectionConfigService);
    verify(apiCollectionConfigRepository, atLeastOnce()).delete(createApiCollectionConfig);
  }

  @Test
  public void testDeleteAllByBrandPageName() {
    when(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .thenReturn(Optional.of(Arrays.asList(createApiCollectionConfig)));
    apiCollectionConfigService.deleteAllByBrand(anyString());
    assertNotNull(apiCollectionConfigService);
    verify(apiCollectionConfigRepository, atLeastOnce()).delete(createApiCollectionConfig);
  }

  @Test
  public void testDeleteAllConfigMapElse() throws Exception {
    boolean thrown = false;
    try {
      when(apiCollectionConfigService.findAllConfigMapByBrand(anyString()))
          .thenReturn(Optional.empty());
      apiCollectionConfigService.deleteAllByBrand(anyString());
    } catch (NotFoundException e) {
      thrown = true;
    }
    assertTrue(thrown);
  }

  @Test
  public void testToPopulateCreatorAndUpdater() throws Exception {
    Boolean isPresent = false;
    try {
      apiCollectionConfigService.populateCreatorAndUpdater(
          userServiceObj, createApiCollectionConfig);
      isPresent = true;
    } catch (InvalidPageNameException e) {
    }
    assertTrue(isPresent);
  }
}
