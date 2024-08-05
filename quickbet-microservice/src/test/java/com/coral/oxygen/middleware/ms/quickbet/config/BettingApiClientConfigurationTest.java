package com.coral.oxygen.middleware.ms.quickbet.config;

import com.coral.oxygen.middleware.ms.quickbet.configuration.BettingApiClientConfiguration;
import com.entain.oxygen.bettingapi.service.BettingService;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.mock.mockito.MockBean;

class BettingApiClientConfigurationTest {

  @MockBean private BettingApiClientConfiguration bettingApiClientConfiguration;

  @BeforeEach
  public void init() {

    bettingApiClientConfiguration = new BettingApiClientConfiguration();
  }

  @Test
  void testBettingService() {
    BettingService bettingService = null;
    bettingService =
        bettingApiClientConfiguration.bettingService("https://localhost:3000", 5000, 5000);
    Assertions.assertNotNull(bettingService);
  }
}
