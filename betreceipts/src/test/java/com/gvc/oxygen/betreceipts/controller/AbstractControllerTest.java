package com.gvc.oxygen.betreceipts.controller;

import com.gvc.oxygen.betreceipts.config.ModelMapperConfig;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.BDDMockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

@ActiveProfiles("UNIT")
@Import(ModelMapperConfig.class)
public abstract class AbstractControllerTest extends BDDMockito {

  @Autowired protected MockMvc mockMvc;

  @BeforeEach
  public void init() throws Exception {}

  @AfterEach
  public void verify() {}
}
