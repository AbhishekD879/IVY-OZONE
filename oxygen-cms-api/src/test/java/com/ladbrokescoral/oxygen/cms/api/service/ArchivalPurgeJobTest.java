package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.FooterMenuArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.HighlightCarouselArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.HomeModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.ModuleRibbonTabArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.NavigationPointArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportCategoryArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportQuickLinkArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SurfaceBetArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.DataRetentionJobsRepository;
import com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.JobsRepository;
import com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.entity.Jobs;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import java.time.Instant;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class ArchivalPurgeJobTest {

  private ArchivalRecordsPurgeTask archivalRecordsPurgeTask;
  private Integer daysDuration = 7;
  @Mock private ScheduledTaskExecutor scheduledTaskExecutorMock;

  private ArchivalRecordsPurgeService archivalRecordsPurgeService;
  @Mock private JobsRepository jobsRepository;
  @Mock private DataRetentionJobsRepository dataRetentionJobsRepository;

  @Mock private SurfaceBetArchivalRepository surfaceBetArchivalRepository;
  @Mock private HighlightCarouselArchiveRepository highlightCarouselArchiveRepository;
  @Mock private HomeModuleArchivalRepository homeModuleArchivalRepository;
  @Mock private FooterMenuArchivalRepository footerMenuArchivalRepository;
  @Mock private NavigationPointArchivalRepository navigationPointArchivalRepository;
  @Mock private SportQuickLinkArchivalRepository sportQuickLinkArchivalRepository;
  @Mock private ModuleRibbonTabArchiveRepository moduleRibbonTabArchiveRepository;
  @Mock private SegmentArchivalRepository segmentArchivalRepository;
  @Mock private SportCategoryArchivalRepository sportCategoryArchivalRepository;
  @Mock private SportModuleArchivalRepository sportModuleArchivalRepository;

  @Before
  public void setUp() {
    archivalRecordsPurgeService =
        new ArchivalRecordsPurgeService(
            surfaceBetArchivalRepository,
            highlightCarouselArchiveRepository,
            homeModuleArchivalRepository,
            footerMenuArchivalRepository,
            navigationPointArchivalRepository,
            sportQuickLinkArchivalRepository,
            moduleRibbonTabArchiveRepository,
            segmentArchivalRepository,
            sportCategoryArchivalRepository,
            sportModuleArchivalRepository);
    archivalRecordsPurgeTask =
        new ArchivalRecordsPurgeTask(
            scheduledTaskExecutorMock,
            daysDuration,
            archivalRecordsPurgeService,
            jobsRepository,
            dataRetentionJobsRepository);

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
  public void testRemoveExpiredEntities() {

    when(jobsRepository.findFirstByJobNameAndJobStatusOrderByUpdatedDateDesc(
            "BIExtract", "Completed"))
        .thenReturn(getJobEntity());
    archivalRecordsPurgeTask.uploadArchivalRecords();
    verify(jobsRepository, times(1))
        .findFirstByJobNameAndJobStatusOrderByUpdatedDateDesc(any(), any());
  }

  @Test
  public void testRemoveExpiredEntities_Exception() {
    when(jobsRepository.findFirstByJobNameAndJobStatusOrderByUpdatedDateDesc(
            "BIExtract", "Completed"))
        .thenReturn(null);
    archivalRecordsPurgeTask.uploadArchivalRecords();
    verify(jobsRepository, times(1))
        .findFirstByJobNameAndJobStatusOrderByUpdatedDateDesc(any(), any());
  }

  private Jobs getJobEntity() {
    Jobs j = new Jobs();
    j.setUpdatedDate(Instant.now());
    j.setInsertedDate(Instant.now());
    j.setJobName("BIExtract");
    j.setJobStatus("Completed");
    return j;
  }
}
