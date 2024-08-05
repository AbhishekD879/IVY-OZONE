package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.ArcMasterDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcMasterData;
import com.ladbrokescoral.oxygen.cms.api.repository.ArcMasterRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ArcMasterService;
import java.io.IOException;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      ArcMasterController.class,
      ArcMasterData.class,
      ArcMasterService.class,
      ArcMasterRepository.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class ArcMasterControllerTest extends AbstractControllerTest {

  private ArcMasterData arcMasterData;
  private ArcMasterDataDto arcMasterDataDto;

  @MockBean ArcMasterService arcMasterService;

  @Before
  public void init() throws IOException {
    arcMasterData = createArcMasterDataList().get(0);
    arcMasterDataDto = createArcMasterDataDtoList().get(0);
  }

  @Test
  public void testToCreateArcMasterData() throws Exception {
    given(arcMasterService.createMasterData(any(ArcMasterData.class)))
        .willReturn(new ResponseEntity<>(arcMasterData, HttpStatus.CREATED));
    given(arcMasterService.getMasterDataByLineItem(anyString())).willReturn(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/arc-master-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(arcMasterDataDto)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testToCreateArcMasterDataWithConflict() throws Exception {
    given(arcMasterService.getMasterDataByLineItem(anyString())).willReturn(arcMasterData);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/arc-master-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(arcMasterDataDto)))
        .andExpect(status().isConflict());
  }

  @Test
  public void testToReadArcMasterData() throws Exception {
    given(arcMasterService.getAllMetadata()).willReturn(createArcMasterDataList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/arc-master-data")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(3)))
        .andExpect(jsonPath("$[0].masterLineName", is("modelRiskLevel")))
        .andExpect(jsonPath("$[0].values", hasSize(4)))
        .andExpect(jsonPath("$[1].masterLineName", is("reasonCodes")))
        .andExpect(jsonPath("$[1].values", hasSize(17)))
        .andExpect(jsonPath("$[2].masterLineName", is("sportActions")))
        .andExpect(jsonPath("$[2].values", hasSize(4)));
  }

  @Test
  public void testToReadArcMasterDataByLineItem() throws Exception {
    given(arcMasterService.getMasterDataByLineItem(anyString())).willReturn(arcMasterData);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/arc-master-data/modelRiskLevel")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.masterLineName", is("modelRiskLevel")))
        .andExpect(jsonPath("$.values.size()", is(4)));
  }

  @Test
  public void testToUpdateArcMasterDataByLineItem() throws Exception {
    given(arcMasterService.getMasterDataByLineItem(anyString())).willReturn(arcMasterData);
    given(arcMasterService.update(any(), any())).willReturn(arcMasterData);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/arc-master-data/modelRiskLevel")
                .contentType(MediaType.APPLICATION_JSON)
                .characterEncoding("UTF-8")
                .content(TestUtil.convertObjectToJsonBytes(arcMasterDataDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateArcMasterDataByLineItemNotFound() throws Exception {
    given(arcMasterService.getMasterDataByLineItem(anyString())).willReturn(null);
    given(arcMasterService.update(any(), any())).willReturn(arcMasterData);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/arc-master-data/modelRiskLevel")
                .contentType(MediaType.APPLICATION_JSON)
                .characterEncoding("UTF-8")
                .content(TestUtil.convertObjectToJsonBytes(arcMasterDataDto)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToUpdateArcMasterDataByLineItemThrowException() throws Exception {
    given(arcMasterService.getMasterDataByLineItem(anyString())).willReturn(arcMasterData);
    given(arcMasterService.update(any(), any())).willThrow(IllegalArgumentException.class);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/arc-master-data/modelRiskLevel")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(arcMasterDataDto)))
        .andExpect(status().isConflict());
  }

  private List<ArcMasterDataDto> createArcMasterDataDtoList() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    List<ArcMasterDataDto> masterDataList =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/private_api/arcMasterData.json"),
            new TypeReference<List<ArcMasterDataDto>>() {});
    return masterDataList;
  }

  private List<ArcMasterData> createArcMasterDataList() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    List<ArcMasterData> masterDataList =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/private_api/arcMasterData.json"),
            new TypeReference<List<ArcMasterData>>() {});
    return masterDataList;
  }
}
