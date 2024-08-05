package com.coral.oxygen.middleware.featured.configuration;

import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;

public class PopularBetApiConfigurationTest {

  PopularBetApiConfiguration popularBetApiConfiguration;

  private String trendingBeturl = "test";

  @Before
  public void init() {
    popularBetApiConfiguration = new PopularBetApiConfiguration(trendingBeturl);
  }

  @Test
  public void popularBetApiTest() {

    Assertions.assertDoesNotThrow(() -> popularBetApiConfiguration.getPopularBetApi());
  }
}
