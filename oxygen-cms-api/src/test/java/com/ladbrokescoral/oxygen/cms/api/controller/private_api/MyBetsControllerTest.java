package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.MyBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.MyBetsRepository;
import com.ladbrokescoral.oxygen.cms.api.service.MyBetsService;
import java.util.Arrays;
import java.util.Collections;
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
      MyBetsController.class,
      MyBetsService.class,
      MyBetsRepository.class,
      ModelMapper.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class MyBetsControllerTest extends AbstractControllerTest {
  @MockBean private MyBetDto myBetDto;
  @MockBean private MyBetsRepository myBetsRepository;
  @Autowired private MyBetsService myBetsService;
  @MockBean private ModelMapper modelMapper;

  @Before
  public void init() {
    myBetDto = createMyBetDto();
    given(myBetsRepository.save(any(MyBet.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testToCreateMyBet() throws Exception {
    when(modelMapper.map(any(), any())).thenReturn(new MyBet());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/my-bets/open-bets")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createMyBetDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadMyBet() throws Exception {
    when(myBetsRepository.findByBrand(any())).thenReturn(Collections.EMPTY_LIST);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/my-bets/open-bets")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadMyBet1() throws Exception {
    when(myBetsRepository.findByBrand(any())).thenReturn(Arrays.asList(new MyBet()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/my-bets/open-bets")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateMyBet() throws Exception {
    when(myBetsRepository.findById(any())).thenReturn(Optional.of(new MyBet()));
    when(modelMapper.map(any(), any())).thenReturn(new MyBet());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(
                    "/v1/api/ladbrokes/my-bets/open-bets/616e7a3c54409d7519879827")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createMyBetDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteMyBet() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(
                    "/v1/api/ladbrokes/my-bets/open-bets/616e7a3c54409d7519879827")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  private MyBetDto createMyBetDto() {
    MyBetDto entity = new MyBetDto();
    entity.setId("616e7a3c54409d7519879827");
    entity.setBrand("ladbrokes");
    return entity;
  }
}
