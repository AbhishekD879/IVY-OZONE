package com.entain.oxygen.promosandbox.controller;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.entain.oxygen.promosandbox.dto.UserRankRequestDto;
import com.entain.oxygen.promosandbox.handler.PromoConfigMessageHandler;
import com.entain.oxygen.promosandbox.utils.AbstractControllerTest;
import com.entain.oxygen.promosandbox.utils.TestUtil;
import java.io.IOException;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;

@WebMvcTest({QAController.class})
class QAControllerTest extends AbstractControllerTest {

  @MockBean PromoConfigMessageHandler promoConfigMessageHandler;

  private static UserRankRequestDto request;

  @BeforeAll
  static void setup() throws IOException {
    request = TestUtil.deserializeWithJackson("/userRankApiRequest.json", UserRankRequestDto.class);
  }

  @Test
  void handleMessageTest() throws Exception {
    Mockito.doNothing().when(promoConfigMessageHandler).handleKafkaMessage(Mockito.any());
    mockMvc
        .perform(
            post("/promosandbox/api/publish-message")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(request)))
        .andExpect(status().is2xxSuccessful());
  }
}
