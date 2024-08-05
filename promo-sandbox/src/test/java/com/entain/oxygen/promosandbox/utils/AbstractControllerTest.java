package com.entain.oxygen.promosandbox.utils;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.BDDMockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.MockMvc;

public abstract class AbstractControllerTest extends BDDMockito {

  @Autowired protected MockMvc mockMvc;

  @BeforeEach
  public void init() throws Exception {}

  @AfterEach
  public void verify() {}
}
