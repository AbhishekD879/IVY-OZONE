package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYConfigurationEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.RGYConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.RGYConfigUploadService;
import com.ladbrokescoral.oxygen.cms.api.service.RGYModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {RGYConfigController.class, RGYConfigService.class})
@AutoConfigureMockMvc(addFilters = false)
public class RGYConfigControllerTest extends AbstractControllerTest {

  @MockBean private RGYConfigRepository rgyConfigRepository;
  @MockBean private RGYModuleService rgyModuleService;
  @MockBean private RGYModuleRepository rgyModuleRepository;
  @MockBean private RGYConfigUploadService rgyConfigUploadService;
  @MockBean private DeliveryNetworkService deliveryNetworkService;

  @SpyBean private RGYConfigService rgyConfigService;

  @Before
  public void init() {
    RGYConfigurationEntity entity = getRGYConfigurationEntity();
    List<RGYConfigurationEntity> entities = new ArrayList<>();
    entities.add(entity);
    doReturn(entity)
        .when(rgyConfigService)
        .update(any(RGYConfigurationEntity.class), any(RGYConfigurationEntity.class));
    doReturn(entity).when(rgyConfigService).save(any(RGYConfigurationEntity.class));
    doReturn(entities).when(rgyConfigRepository).findByBrand("ladbrokes");
    given(rgyConfigRepository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(rgyConfigRepository.save(any(RGYConfigurationEntity.class)))
        .will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testSaveEntity() throws Exception {
    RGYConfigurationEntity rgyConfigurationEntity = getRGYConfigurationEntity();
    rgyConfigurationEntity.getModuleIds().add("promo12131");
    when(rgyConfigService.findByBrandAndReasonCodeAndRiskLevelCode("ladbrokes", 3, 4))
        .thenReturn(rgyConfigurationEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/rgyConfig")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRGYConfigurationEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testSaveEntityUpdate() throws Exception {
    RGYConfigurationEntity rgyConfigurationEntity = new RGYConfigurationEntity();
    rgyConfigurationEntity.setId("abcd1234");
    rgyConfigurationEntity.setBrand("ladbrokes");
    rgyConfigurationEntity.setBonusSuppression(true);
    rgyConfigurationEntity.setReasonDesc("");
    rgyConfigurationEntity.setReasonCode(3);
    rgyConfigurationEntity.setRiskLevelCode(4);
    rgyConfigurationEntity.setRiskLevelDesc("");
    List<String> moduleIds = new ArrayList<>();
    moduleIds.add("dfadfsdfdsfererer");
    rgyConfigurationEntity.setModuleIds(moduleIds);
    when(rgyConfigService.findByBrandAndReasonCodeAndRiskLevelCode("ladbrokes", 3, 4))
        .thenReturn(rgyConfigurationEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/rgyConfig")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRGYConfigurationEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testSaveEntityEmpty() throws Exception {
    when(rgyConfigService.findByBrandAndReasonCodeAndRiskLevelCode("ladbrokes", 3, 4))
        .thenReturn(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/rgyConfig")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRGYConfigurationEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/rgyConfig/abcd1234")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRGYConfigurationEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/rgyConfig/abcd1234")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRGYConfigurationEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/rgyConfig/ladbrokes/abcd1234")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRGYConfigurationEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/rgyConfig/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private RGYConfigurationEntity getRGYConfigurationEntity() {
    RGYConfigurationEntity rgyConfigurationEntity = new RGYConfigurationEntity();
    rgyConfigurationEntity.setId("abcd1234");
    rgyConfigurationEntity.setBrand("ladbrokes");
    rgyConfigurationEntity.setBonusSuppression(true);
    rgyConfigurationEntity.setReasonDesc("");
    rgyConfigurationEntity.setReasonCode(3);
    rgyConfigurationEntity.setRiskLevelCode(4);
    rgyConfigurationEntity.setRiskLevelDesc("");
    List<String> moduleIds = new ArrayList<>();
    moduleIds.add("fiveaside211212");
    rgyConfigurationEntity.setModuleIds(moduleIds);
    return rgyConfigurationEntity;
  }
}
