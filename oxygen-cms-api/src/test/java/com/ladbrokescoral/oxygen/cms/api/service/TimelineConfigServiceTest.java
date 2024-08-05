package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Config;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineConfigRepository;
import com.ladbrokescoral.oxygen.cms.kafka.TimelineKafkaPublisher;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class TimelineConfigServiceTest {

  @Mock private TimelineKafkaPublisher timelineKafkaPublisher;
  @Mock private TimelineConfigRepository repository;
  private TimelineConfigService service;

  Config config;

  public static final String BRAND = "ladbrokes";
  public static final String BMA = "bma";

  @Before
  public void setUp() {
    config = new Config();
    config.setBrand(BRAND);

    when(repository.findOneByBrand(eq(BRAND))).thenReturn(Optional.of(config));

    service = new TimelineConfigService(repository, timelineKafkaPublisher);
  }

  @Test
  public void testSave() {
    when(repository.existsByBrand(eq(BRAND))).thenReturn(false);

    service.save(config);

    verify(repository).save(config);
  }

  @Test
  public void testUpdateBMA() {
    Config newConfig = new Config();
    newConfig.setBrand(BMA);
    config.setBrand(BMA);
    service.update(config, newConfig);

    verify(repository).save(config);
  }

  @Test
  public void testUpdate() {
    Config newConfig = new Config();
    newConfig.setBrand(BRAND);

    service.update(config, newConfig);

    verify(repository).save(config);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testUpdateSetNewBrand() {
    Config newConfig = new Config();
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
