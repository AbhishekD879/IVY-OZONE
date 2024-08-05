package com.gvc.oxygen.betreceipts;

import com.gvc.oxygen.betreceipts.repository.BetRepository;
import com.gvc.oxygen.betreceipts.repository.EventRepository;
import com.gvc.oxygen.betreceipts.repository.MetaEventRepository;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

@ActiveProfiles("UNIT")
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
public class BetReceiptsTest {

  @Autowired private MockMvc mockMvc;

  @MockBean private BetRepository repository;

  @MockBean private EventRepository eventRepository;

  @MockBean private MetaEventRepository metaEventRepository;

  @Test
  public void testApp() throws Exception {
    mockMvc
        .perform(MockMvcRequestBuilders.get("/actuator/health"))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.status", Matchers.equalTo("UP")));
  }
}
