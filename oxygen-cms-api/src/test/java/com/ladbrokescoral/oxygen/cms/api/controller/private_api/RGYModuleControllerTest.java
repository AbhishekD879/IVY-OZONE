package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.RGYConfigUploadService;
import com.ladbrokescoral.oxygen.cms.api.service.RGYModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.ArrayList;
import java.util.Collections;
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

@WebMvcTest(value = {RGYModuleController.class, RGYModuleService.class})
@AutoConfigureMockMvc(addFilters = false)
public class RGYModuleControllerTest extends AbstractControllerTest {
  @MockBean private RGYModuleRepository rgyModuleRepository;
  @MockBean private RGYConfigUploadService rgyConfigUploadService;

  @MockBean private DeliveryNetworkService deliveryNetworkService;
  @SpyBean private RGYModuleService rgyModuleService;

  @Before
  public void init() {
    RGYModuleEntity entity = getRGYModuleEntity();
    List<RGYModuleEntity> entities = new ArrayList<>();
    entities.add(entity);
    doReturn(entity)
        .when(rgyModuleService)
        .update(any(RGYModuleEntity.class), any(RGYModuleEntity.class));
    doReturn(entity).when(rgyModuleService).save(any(RGYModuleEntity.class));
    doReturn(entities).when(rgyModuleRepository).findByBrand("ladbrokes");
    given(rgyModuleRepository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(rgyModuleRepository.save(any(RGYModuleEntity.class)))
        .will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testSaveEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/rgyModule")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRGYModuleEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/rgyModule/adfdsf212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRGYModuleEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/rgyModule/adfdsf212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRGYModuleEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/rgyModule/ladbrokes/adfdsf212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRGYModuleEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/rgyModule/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private RGYModuleEntity getRGYModuleEntity() {
    RGYModuleEntity rgyModuleEntity = new RGYModuleEntity();
    rgyModuleEntity.setId("adfdsf212121");
    rgyModuleEntity.setBrand("ladbrokes");
    rgyModuleEntity.setModuleName("Promotions");
    rgyModuleEntity.setSubModuleEnabled(true);
    rgyModuleEntity.setAliasModules(
        Collections.singletonList(aliasModuleNamesDto("FIVEASIDE", "11")));
    return rgyModuleEntity;
  }

  private AliasModuleNamesDto aliasModuleNamesDto(String title, String id) {
    AliasModuleNamesDto aliasModuleNamesDto = new AliasModuleNamesDto();
    aliasModuleNamesDto.setId(id);
    aliasModuleNamesDto.setTitle(title);
    return aliasModuleNamesDto;
  }
}
