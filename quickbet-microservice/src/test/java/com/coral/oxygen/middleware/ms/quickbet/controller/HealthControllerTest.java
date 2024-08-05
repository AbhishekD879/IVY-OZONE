package com.coral.oxygen.middleware.ms.quickbet.controller;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {HealthController.class})
@AutoConfigureMockMvc(addFilters = false)
class HealthControllerTest {
  @Autowired private MockMvc mockMvc;

  @Test
  void testHealthCheck() throws Exception {
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/health").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
