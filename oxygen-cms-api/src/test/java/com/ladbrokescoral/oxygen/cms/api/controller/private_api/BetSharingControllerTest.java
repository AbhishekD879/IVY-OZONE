package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.BetSharingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetSharingEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.BetSharingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BetSharingService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {BetSharingController.class, BetSharingService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class BetSharingControllerTest extends AbstractControllerTest {

  @MockBean private BetSharingRepository repository;

  private BetSharingEntity betSharingEntity;
  private BetSharingDto betSharingDto;
  ModelMapper mapper = new ModelMapper();

  @Before
  public void setUp() throws Exception {
    betSharingDto =
        TestUtil.deserializeWithJackson(
            "controller/private_api/BetSharing/betSharing.json", BetSharingDto.class);
    betSharingEntity = mapper.map(betSharingDto, BetSharingEntity.class);
    when(repository.save(any())).thenReturn(betSharingEntity);
    when(repository.findById(any())).thenReturn(Optional.of(betSharingEntity));
  }

  @Test
  public void testCreateBetSharing() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-sharing")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betSharingDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateBetSharingWhenIdExists() throws Exception {
    String id = "62cd9ce3fa2d927e6d9c18ad";
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/bet-sharing/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betSharingDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateBetSharingWhenIdNotExists() throws Exception {
    String id = "118000004558668682";
    when(repository.findById(id)).thenReturn(Optional.empty());
    betSharingDto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/bet-sharing/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betSharingDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testDeleteById() throws Exception {
    String id = "62cd9ce3fa2d927e6d9c18ad";
    when(repository.findById(any())).thenReturn(Optional.of(betSharingEntity), Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-sharing/" + id)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetByBrand() throws Exception {
    when(repository.findByBrand(anyString())).thenReturn(Arrays.asList(betSharingEntity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-sharing/brand/coral")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetByBrandWhenEmpty() throws Exception {
    when(repository.findByBrand(anyString())).thenReturn(Arrays.asList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-sharing/brand/coral")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }
}
