package com.oxygen.publisher.sportsfeatured.service;

import static org.junit.Assert.assertFalse;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import java.util.concurrent.atomic.AtomicBoolean;
import org.junit.Before;
import org.junit.Test;

public class SportsPageIdRegistrationTest {

  private SportIdFilter sportIdFilter;
  private SportsCachedData sportsCachedData;
  private FeaturedService featuredService;

  private SportsPageIdRegistration sportsPageIdRegistration;

  @Before
  public void init() {
    sportIdFilter = mock(SportIdFilter.class);
    sportsCachedData = mock(SportsCachedData.class);
    featuredService = mock(FeaturedService.class);
    sportsPageIdRegistration =
        new SportsPageIdRegistration(mock(FeaturedService.class), sportIdFilter, sportsCachedData);
  }

  @Test
  public void testTheStart() {
    when(sportIdFilter.isSupportedPageType(anyString())).thenReturn(Boolean.TRUE);
    sportsPageIdRegistration.start();

    assertFalse(sportsCachedData.isEmpty());
  }

  @Test
  public void evict() {

    AtomicBoolean isOnService = new AtomicBoolean();
    isOnService.set(false);
    sportsPageIdRegistration.evict();
    assertFalse(isOnService.get());

    boolean healthy = sportsPageIdRegistration.isHealthy();
    assertFalse(healthy);

    sportsPageIdRegistration.onFail(new RuntimeException("failed on runtime"));
    assertFalse(isOnService.get());
  }
}
