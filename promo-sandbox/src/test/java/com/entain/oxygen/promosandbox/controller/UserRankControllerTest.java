package com.entain.oxygen.promosandbox.controller;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.entain.oxygen.promosandbox.dto.UserRankRequestDto;
import com.entain.oxygen.promosandbox.dto.UserRankResponseDto;
import com.entain.oxygen.promosandbox.service.UserRankService;
import com.entain.oxygen.promosandbox.utils.AbstractControllerTest;
import com.entain.oxygen.promosandbox.utils.TestUtil;
import java.io.IOException;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;

@WebMvcTest({UserRankController.class})
class UserRankControllerTest extends AbstractControllerTest {

  @MockBean UserRankService userRankService;

  private static UserRankRequestDto userRankRequest;

  @BeforeAll
  static void setup() throws IOException {
    userRankRequest =
        TestUtil.deserializeWithJackson("/userRankApiRequest.json", UserRankRequestDto.class);
  }

  @Test
  void fetchUserRankDetailsTest() throws Exception {
    when(userRankService.fetchUserRankDetails(Mockito.any(), any()))
        .thenReturn(new UserRankResponseDto());
    mockMvc
        .perform(
            post("/promosandbox/api/user-rank")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "123444")
                .content(TestUtil.convertObjectToJsonBytes(userRankRequest)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void fetchUserRankDetails400Test() throws Exception {
    when(userRankService.fetchUserRankDetails(Mockito.any(), any()))
        .thenReturn(new UserRankResponseDto());
    mockMvc
        .perform(
            post("/promosandbox/api/user-rank")
                .contentType(MediaType.APPLICATION_JSON)
                .header("token", "123444")
                .content(TestUtil.convertObjectToJsonBytes(new UserRankRequestDto())))
        .andExpect(status().is4xxClientError());
  }

  @Test
  void fetchUserRankDetails404Test() throws Exception {
    when(userRankService.fetchUserRankDetails(Mockito.any(), any()))
        .thenReturn(new UserRankResponseDto());
    mockMvc
        .perform(
            post("/promosandbox/api/userRank2")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(new UserRankRequestDto())))
        .andExpect(status().is4xxClientError());
  }
}
