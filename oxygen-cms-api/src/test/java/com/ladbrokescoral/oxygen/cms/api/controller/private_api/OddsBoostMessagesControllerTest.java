package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OddsBoostMessageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostMessage;
import com.ladbrokescoral.oxygen.cms.api.repository.OddsBoostMessageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.OddsBoostMessageService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      OddsBoostMessagesController.class,
      OddsBoostMessageService.class,
      OddsBoostMessageRepository.class,
      ModelMapper.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class OddsBoostMessagesControllerTest extends AbstractControllerTest {
  @MockBean private OddsBoostMessageDto oddsBoostMessageDto;
  @MockBean private OddsBoostMessageRepository oddsBoostMessageRepository;
  @Autowired private OddsBoostMessageService oddsBoostMessageService;
  @MockBean private ModelMapper modelMapper;
  @MockBean private BrandService brandService;

  @Override
  @Before
  public void init() {
    oddsBoostMessageDto = createOddsBoostMessageDto();
    given(oddsBoostMessageRepository.save(any(OddsBoostMessage.class)))
        .will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testToCreateMyBet() throws Exception {
    when(oddsBoostMessageRepository.findOneByBrand(any())).thenReturn(Optional.empty());
    when(modelMapper.map(any(), any())).thenReturn(new OddsBoostMessage());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/odds-boost-messages")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOddsBoostMessageDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToCreateMyBet1() throws Exception {
    when(oddsBoostMessageRepository.findOneByBrand(any()))
        .thenReturn(Optional.of(new OddsBoostMessage()));
    when(modelMapper.map(any(), any())).thenReturn(new OddsBoostMessage());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/odds-boost-messages")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOddsBoostMessageDto())))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testToReadMyBet() throws Exception {
    when(oddsBoostMessageRepository.findOneByBrand(any())).thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/odds-boost-messages/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadMyBet1() throws Exception {
    when(oddsBoostMessageRepository.findOneByBrand(any()))
        .thenReturn(Optional.of(new OddsBoostMessage()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/odds-boost-messages/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateMyBet() throws Exception {
    when(oddsBoostMessageRepository.findById(any()))
        .thenReturn(Optional.of(new OddsBoostMessage()));
    when(modelMapper.map(any(), any())).thenReturn(new OddsBoostMessage());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/odds-boost-messages/6642ff2aa6151d2e76eca00b")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOddsBoostMessageDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteMyBet() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/odds-boost-messages/id")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  private OddsBoostMessageDto createOddsBoostMessageDto() {
    OddsBoostMessageDto entity = new OddsBoostMessageDto();
    entity.setSvgId("616e7a3c54409d7519879827");
    entity.setBrand("ladbrokes");
    return entity;
  }
}
