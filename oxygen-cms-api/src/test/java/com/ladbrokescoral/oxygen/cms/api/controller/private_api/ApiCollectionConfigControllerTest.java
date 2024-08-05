package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static com.ladbrokescoral.oxygen.cms.api.TestUtil.deserializeWithJackson;
import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertEquals;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.ApiCollectionConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.ConfigMapKeyDuplicationException;
import com.ladbrokescoral.oxygen.cms.api.repository.ApiCollectionConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ApiCollectionConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.assertj.core.api.Assertions;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      ApiCollectionConfigRepository.class,
      ApiCollectionConfigController.class,
      ApiCollectionConfigService.class,
      UserService.class,
      User.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class ApiCollectionConfigControllerTest extends AbstractControllerTest {

  private ApiCollectionConfig createApiCollectionConfig;
  private ApiCollectionConfig updateApiCollectionConfig;
  private ApiCollectionConfigDto createApiCollectionConfigDto;

  @MockBean private ApiCollectionConfigRepository apiCollectionConfigRepository;
  @Autowired private ApiCollectionConfigService apiCollectionConfigService;
  public static final String API_BASE_URL = "/v1/api/api-collection-config";

  @Before
  public void init() throws IOException {
    createApiCollectionConfig =
        deserializeWithJackson(
            "controller/private_api/apicollectionconfig/createApiCollectionConfig.json",
            ApiCollectionConfig.class);

    updateApiCollectionConfig =
        deserializeWithJackson(
            "controller/private_api/apicollectionconfig/updateApiCollectionConfig.json",
            ApiCollectionConfig.class);

    createApiCollectionConfigDto =
        deserializeWithJackson(
            "controller/private_api/apicollectionconfig/createApiCollectionConfigDto.json",
            ApiCollectionConfigDto.class);
    given(apiCollectionConfigRepository.save(any(ApiCollectionConfig.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(
            apiCollectionConfigRepository.findConfigMapByAndColumn(
                anyString(), anyString(), anyString()))
        .willReturn(Optional.of(createApiCollectionConfig));
    given(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(createApiCollectionConfig)));
  }

  @Test
  public void testToCreateConfigMap() throws Exception {
    given(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createApiCollectionConfig)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToCreateConfigMapWithException() throws Exception {
    given(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(createApiCollectionConfig)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createApiCollectionConfigDto)))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testToUpdateConfigMap() throws Exception {
    List<ApiCollectionConfig> configMapList = new ArrayList<ApiCollectionConfig>();
    configMapList.add(createApiCollectionConfig);
    configMapList.get(0).setId("11");
    configMapList.get(0).setKey("/v1/api");
    ApiCollectionConfig apiCollectionConfig1 = updateApiCollectionConfig;
    configMapList.add(apiCollectionConfig1);
    given(
            apiCollectionConfigRepository.findConfigMapByAndColumn(
                anyString(), anyString(), anyString()))
        .willReturn(Optional.of(createApiCollectionConfig));
    given(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .willReturn(Optional.of(configMapList));
    given(apiCollectionConfigService.findOne(anyString()))
        .willReturn(Optional.of(createApiCollectionConfig));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/bma/id/101")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createApiCollectionConfigDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testConfigMapKeyUpperCase() {
    ApiCollectionConfig collectionConfig = new ApiCollectionConfig();
    collectionConfig.setBrand("bma");
    collectionConfig.setKey("api");
    when(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .thenReturn(Optional.of(Arrays.asList(collectionConfig)));
    Assertions.assertThatExceptionOfType(ConfigMapKeyDuplicationException.class)
        .isThrownBy(() -> apiCollectionConfigService.validateConfigMapByKey(collectionConfig));
  }

  @Test
  public void testConfigMapKeyNotUpperCase() {
    ApiCollectionConfig collectionConfig = new ApiCollectionConfig();
    collectionConfig.setBrand("bma");
    collectionConfig.setKey("APPI");
    String key = "API";
    when(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .thenReturn(Optional.of(Arrays.asList(createApiCollectionConfig)));
    apiCollectionConfigService.validateConfigMapByKey(collectionConfig);
  }

  @Test
  public void testToReadConfigMapByID() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/bma/id/100")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadAllConfigMap() throws Exception {
    given(apiCollectionConfigRepository.findAllConfigMapByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(createApiCollectionConfig)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteAllConfigMapEntry() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getConfigMap() {
    doReturn(Optional.ofNullable(createApiCollectionConfig))
        .when(apiCollectionConfigRepository)
        .findConfigMapByAndColumn(
            createApiCollectionConfig.getBrand(), "id", createApiCollectionConfig.getId());
    Optional<ApiCollectionConfig> apiCollectionConfig1 =
        Optional.ofNullable(
            apiCollectionConfigService.findConfigMapByBrandAndColumn(
                createApiCollectionConfig.getBrand(), "id", createApiCollectionConfig.getId()));
    verify(apiCollectionConfigRepository, times(1))
        .findConfigMapByAndColumn(
            createApiCollectionConfig.getBrand(), "id", createApiCollectionConfig.getId());

    assertEquals(createApiCollectionConfig, apiCollectionConfig1.get());
    assertTrue(apiCollectionConfig1.isPresent());
  }

  @Test
  public void testToDeleteConfigMap() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/bma/id/101")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
