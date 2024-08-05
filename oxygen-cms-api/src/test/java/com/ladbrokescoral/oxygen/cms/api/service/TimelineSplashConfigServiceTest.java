package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineSplashConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineSplashConfigRepository;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class TimelineSplashConfigServiceTest {
  private TimelineSplashConfigService service;
  @Mock TimelineSplashConfigRepository repository;

  TimelineSplashConfig config;

  public static final String BRAND = "ladbrokes";

  @Before
  public void setUp() {
    config = new TimelineSplashConfig();
    config.setBrand(BRAND);

    when(repository.findOneByBrand(eq(BRAND))).thenReturn(Optional.of(config));

    service = new TimelineSplashConfigService(repository);
  }

  @Test
  public void testSave() {
    when(repository.existsByBrand(eq(BRAND))).thenReturn(false);

    service.save(config);

    verify(repository).save(config);
  }

  @Test
  public void testUpdate() {
    TimelineSplashConfig newConfig = new TimelineSplashConfig();
    newConfig.setBrand(BRAND);

    service.update(config, newConfig);

    verify(repository).save(config);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testUpdateSetNewBrand() {
    TimelineSplashConfig newConfig = new TimelineSplashConfig();
    newConfig.setBrand(BRAND + "new");

    service.update(config, newConfig);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testRepeatingSaveCausesException() {
    when(repository.existsByBrand(eq(BRAND))).thenReturn(true);

    service.save(config);

    verify(repository).save(config);
  }

  @Test
  public void testFindOneByBrand() {
    service.findOneByBrand(BRAND);
    verify(repository).findOneByBrand(BRAND);
  }

  @Test
  public void testFindOptionalByBrand() {
    service.findOptionalByBrand(BRAND);
    verify(repository).findOneByBrand(BRAND);
  }
}
