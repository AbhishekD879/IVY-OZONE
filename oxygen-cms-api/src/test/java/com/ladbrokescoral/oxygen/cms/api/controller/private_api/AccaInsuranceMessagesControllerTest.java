package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.AccaInsuranceMessageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.AccaInsuranceMessage;
import com.ladbrokescoral.oxygen.cms.api.repository.AccaInsuranceMessageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AccaInsuranceMessageService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
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
      AccaInsuranceMessagesController.class,
      AccaInsuranceMessageService.class,
      AccaInsuranceMessageRepository.class,
      ModelMapper.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class AccaInsuranceMessagesControllerTest extends AbstractControllerTest {
  @MockBean private AccaInsuranceMessageDto accaInsuranceMessageDto;
  @MockBean private AccaInsuranceMessageRepository accaInsuranceMessageRepository;
  @Autowired private AccaInsuranceMessageService accaInsuranceMessageService;
  @MockBean private ModelMapper modelMapper;
  @MockBean private BrandService brandService;

  @Override
  @Before
  public void init() {
    accaInsuranceMessageDto = createAccaInsuranceMessageDto();
    given(accaInsuranceMessageRepository.save(any(AccaInsuranceMessage.class)))
        .will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testToCreateMyBet() throws Exception {
    when(accaInsuranceMessageRepository.findOneByBrand(any())).thenReturn(Optional.empty());
    when(modelMapper.map(any(), any())).thenReturn(new AccaInsuranceMessage());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/acca-insurance-messages")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createAccaInsuranceMessageDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToCreateMyBet1() throws Exception {
    when(accaInsuranceMessageRepository.findOneByBrand(any()))
        .thenReturn(Optional.of(new AccaInsuranceMessage()));
    when(modelMapper.map(any(), any())).thenReturn(new AccaInsuranceMessage());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/acca-insurance-messages")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createAccaInsuranceMessageDto())))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testToReadMyBet() throws Exception {
    when(accaInsuranceMessageRepository.findOneByBrand(any())).thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/acca-insurance-messages/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadMyBet1() throws Exception {
    when(accaInsuranceMessageRepository.findOneByBrand(any()))
        .thenReturn(Optional.of(new AccaInsuranceMessage()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/acca-insurance-messages/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateMyBet() throws Exception {
    when(accaInsuranceMessageRepository.findById(any()))
        .thenReturn(Optional.of(new AccaInsuranceMessage()));
    when(modelMapper.map(any(), any())).thenReturn(new AccaInsuranceMessage());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/acca-insurance-messages/6642ff2aa6151d2e76eca00b")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createAccaInsuranceMessageDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteMyBet() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/acca-insurance-messages/id")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  private AccaInsuranceMessageDto createAccaInsuranceMessageDto() {
    AccaInsuranceMessageDto entity = new AccaInsuranceMessageDto();
    entity.setSvgId("616e7a3c54409d7519879827");
    entity.setBrand("ladbrokes");
    return entity;
  }
}
