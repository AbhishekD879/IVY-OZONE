package com.ladbrokescoral.oxygen.betpackmp.controller;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.BDDMockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

@ActiveProfiles("UNIT")
public abstract class AbstractControllerTest extends BDDMockito {

  @Autowired protected MockMvc mockMvc;

  @BeforeEach
  public void init() {}

  @AfterEach
  public void verify() {}
}
