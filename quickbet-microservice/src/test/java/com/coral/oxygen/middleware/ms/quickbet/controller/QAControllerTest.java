package com.coral.oxygen.middleware.ms.quickbet.controller;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.coral.oxygen.middleware.ms.quickbet.connector.SessionManager;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.impl.SessionStorage;
import java.util.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@ExtendWith(SpringExtension.class)
@WebMvcTest(value = {QAController.class})
@AutoConfigureMockMvc(addFilters = false)
class QAControllerTest {
  @Autowired private MockMvc mockMvc;
  @MockBean private SessionStorage<SessionDto> sessionStorage;
  @MockBean private SessionManager sessionManager;
  List<SessionDto> dto = new ArrayList<SessionDto>();
  Map<UUID, SessionDto> map = new HashMap<UUID, SessionDto>();

  @Test
  void testSessionCheck() throws Exception {
    Mockito.when(sessionStorage.findAll()).thenReturn(dto);
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/qa/sessions").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testattachedSessions() throws Exception {
    Mockito.when(sessionManager.getAllAttachedSessions()).thenReturn(map);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/qa/attachedSessions")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
