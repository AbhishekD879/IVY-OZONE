package com.oxygen.publisher.sportsfeatured.service;

import static org.junit.Assert.assertNotNull;

import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry;
import com.oxygen.publisher.sportsfeatured.configuration.FeaturedServiceConfiguration;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest
public class FeaturedServiceConfigurationTest {

  @Autowired private FeaturedServiceConfiguration featuredServiceConfiguration;

  @Autowired private SportsServiceRegistry medianServiceRegistry;

  @Test
  public void testSportsCachedData() {

    final SportsCachedData cachedData = featuredServiceConfiguration.sportsCachedData(22, 15);

    assertNotNull(cachedData);
  }

  @Test
  public void testSportsPageIdRegistration() {

    assertNotNull(medianServiceRegistry);
    medianServiceRegistry.load();
    SportsPageIdRegistration sportsPageIdRegistration =
        medianServiceRegistry.getSportsPageIdRegistration();
    assertNotNull(sportsPageIdRegistration);
  }
}
