package com.coral.oxygen.middleware.featured.configuration;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import com.coral.oxygen.middleware.common.configuration.GsonConfiguration;
import com.coral.oxygen.middleware.common.configuration.OkHttpClientCreator;
import com.coral.oxygen.middleware.common.service.SportsConfig;
import com.coral.oxygen.middleware.common.utils.OrdinalToNumberConverter;
import com.coral.oxygen.middleware.featured.configuration.AemMetaConsumerConfig.SportsCategoriesLookup;
import com.coral.oxygen.middleware.featured.configuration.AemMetaConsumerConfigTest.Oxygen;
import com.coral.oxygen.middleware.featured.consumer.sportpage.AemCarouselsProcessor;
import java.util.Map;
import lombok.Data;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Profile;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@EnableConfigurationProperties
@Import(AemMetaConsumerConfig.class)
@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(
    classes = {
      SportsConfig.class,
      GsonConfiguration.class,
      OrdinalToNumberConverter.class,
      OkHttpClientCreator.class,
      Oxygen.class
    })
public class AemMetaConsumerConfigTest {

  @Profile("AEM")
  @ConfigurationProperties(prefix = "oxygen")
  @Configuration
  @Data
  public static class Oxygen {

    public SportsCategoriesLookup[] sportsCategoriesLookup;
  }

  @Autowired public Oxygen oxygen;

  @Autowired AemCarouselsProcessor aemCarouselsProcessor;

  @Test
  public void getSportsCategoriesDict() {
    Map<String, String> dict = aemCarouselsProcessor.getSportsCategoriesDict();
    for (SportsCategoriesLookup lookup : oxygen.sportsCategoriesLookup) {
      final String catId = lookup.categoryId;
      for (String synonym : lookup.getSynonyms()) {
        assertTrue(dict.containsKey(synonym));
        assertEquals(catId, dict.get(synonym));
      }
    }
    assertFalse(dict.isEmpty());
  }
}
