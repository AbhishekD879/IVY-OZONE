package com.gvc.oxygen.betreceipts;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.BDDMockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Profile;
import org.springframework.test.web.servlet.MockMvc;

@Profile("UNIT")
@TestConfiguration
@AutoConfigureMockMvc
public class SpringBootTestConfiguration extends BDDMockito {

  @Autowired protected MockMvc mockMvc;

  @BeforeEach
  public void init() throws Exception {}

  @AfterEach
  public void verify() {}
}
