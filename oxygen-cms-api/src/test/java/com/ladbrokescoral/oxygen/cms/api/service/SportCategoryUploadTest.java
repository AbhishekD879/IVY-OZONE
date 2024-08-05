package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportCategoryArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;

@RunWith(MockitoJUnitRunner.class)
public class SportCategoryUploadTest {

  private SportCategoryArchivalUploadTask sportCategoryArchivalUploadTask;
  @Mock private ScheduledTaskExecutor scheduledTaskExecutorMock;
  @Mock private SportCategoryArchivalRepository sportCategoryArchivalRepository;
  @Mock private SportCategoryRepository sportCategoryRepository;

  @Before
  public void setUp() {

    sportCategoryArchivalUploadTask =
        new SportCategoryArchivalUploadTask(
            scheduledTaskExecutorMock,
            sportCategoryArchivalRepository,
            sportCategoryRepository,
            new ModelMapper());

    doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[0];
              task.run();
              return null;
            })
        .when(scheduledTaskExecutorMock)
        .execute(any(Runnable.class));
  }

  @Test
  public void testSportQuickLinkWithNullArchival() {

    when(sportCategoryRepository.findAll()).thenReturn(getAllSportQuickLink(null, null));

    sportCategoryArchivalUploadTask.uploadArchivalRecords();

    verify(sportCategoryRepository, times(1)).saveAll(any());
    verify(sportCategoryArchivalRepository, times(1)).saveAll(any());
  }

  @Test
  public void testSportQuickLinkWithOneArchival() {

    when(sportCategoryRepository.findAll()).thenReturn(getAllSportQuickLink("21212121", null));

    sportCategoryArchivalUploadTask.uploadArchivalRecords();

    verify(sportCategoryRepository, times(1)).saveAll(any());
    verify(sportCategoryArchivalRepository, times(1)).saveAll(any());
  }

  @Test
  public void testSportQuickLinkWithArchival() {

    when(sportCategoryRepository.findAll())
        .thenReturn(getAllSportQuickLink("21212121", "21212121"));

    sportCategoryArchivalUploadTask.uploadArchivalRecords();

    verify(sportCategoryRepository, times(0)).saveAll(any());
    verify(sportCategoryArchivalRepository, times(1)).saveAll(any());
  }

  @Test
  public void testSportQuickLinkWithArchivalException() {
    when(sportCategoryRepository.findAll())
        .thenReturn(getAllSportQuickLink("21212121", "21212121"));
    sportCategoryArchivalUploadTask =
        new SportCategoryArchivalUploadTask(
            scheduledTaskExecutorMock, null, sportCategoryRepository, new ModelMapper());
    sportCategoryArchivalUploadTask.uploadArchivalRecords();

    verify(sportCategoryRepository, times(0)).saveAll(any());
    verify(sportCategoryArchivalRepository, times(0)).saveAll(any());
  }

  @Test
  public void testSportQuickLinkWithArchivalwithooutException() {
    when(sportCategoryRepository.findAll()).thenReturn(new ArrayList<>());
    sportCategoryArchivalUploadTask =
        new SportCategoryArchivalUploadTask(
            scheduledTaskExecutorMock, null, sportCategoryRepository, new ModelMapper());
    sportCategoryArchivalUploadTask.uploadArchivalRecords();

    verify(sportCategoryRepository, times(0)).saveAll(any());
    verify(sportCategoryArchivalRepository, times(0)).saveAll(any());
  }

  private List<SportCategory> getAllSportQuickLink(String archival1, String archival2) {
    List<SportCategory> categories = new ArrayList<>();
    SportCategory cat = new SportCategory();
    cat.setArchivalId(archival1);
    cat.setUpdatedAt(Instant.now());
    SportCategory cat2 = new SportCategory();
    cat2.setArchivalId(archival2);
    cat2.setUpdatedAt(Instant.now().minus(3, ChronoUnit.DAYS));

    categories.add(cat);
    categories.add(cat2);
    return categories;
  }
}
