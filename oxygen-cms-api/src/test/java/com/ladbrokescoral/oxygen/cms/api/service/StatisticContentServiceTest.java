package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.StatisticContent;
import com.ladbrokescoral.oxygen.cms.api.repository.StatisticContentRepository;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.time.Instant;
import java.util.Collections;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class StatisticContentServiceTest {

  private StatisticContentService service;

  @Mock private StatisticContentRepository repository;

  @Mock private SiteServeApiProvider siteServeApiProvider;

  @Mock private ScheduledTaskExecutor executor;

  private StatisticContent entity;

  @Before
  public void init() {
    Mockito.doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[0];
              task.run();
              return null;
            })
        .when(executor)
        .execute(Mockito.any(Runnable.class));

    entity = new StatisticContent();
    entity.setTitle("Man Vs Liv");
    entity.setStartTime(Instant.now());
    entity.setEndTime(Instant.now());
    this.service = new StatisticContentService(repository, siteServeApiProvider, executor, 1);
  }

  @Test
  public void testNotRemoveExpiredEntities() {
    Mockito.doReturn(Collections.singletonList(entity)).when(repository).findAll();
    this.service.removeExpiredEntities();
    Mockito.verify(repository, Mockito.atLeast(1)).findAll();
  }

  @Test
  public void testRemoveExpiredEntities() {
    StatisticContent content = this.entity;
    content.setStartTime(Instant.parse("2023-01-08T05:44:27.865Z"));
    content.setEndTime(Instant.parse("2023-01-08T05:50:27.865Z"));
    Mockito.doReturn(Collections.singletonList(content)).when(repository).findAll();
    this.service.removeExpiredEntities();
    Mockito.verify(repository, Mockito.atLeast(1)).findAll();
  }
}
