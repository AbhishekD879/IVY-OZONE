package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.DataRetentionJobsRepository;
import com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.JobsRepository;
import com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.entity.DataRetentionJobs;
import com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.entity.Jobs;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class ArchivalRecordsPurgeTask {

  private final ScheduledTaskExecutor scheduledTaskExecutor;
  private final ArchivalRecordsPurgeService archivalRecordsPurgeService;

  @Value("${archival.removeExpired.afterDays}")
  private final int daysToPurgeArchival;

  private final JobsRepository jobsRepository;
  private final DataRetentionJobsRepository dataRetentionJobsRepository;

  public ArchivalRecordsPurgeTask(
      final ScheduledTaskExecutor scheduledTaskExecutor,
      @Value("${archival.removeExpired.afterDays}") final int daysToPurgeArchival,
      final ArchivalRecordsPurgeService archivalRecordsPurgeService,
      JobsRepository jobsRepository,
      DataRetentionJobsRepository dataRetentionJobsRepository) {

    this.scheduledTaskExecutor = scheduledTaskExecutor;
    this.daysToPurgeArchival = daysToPurgeArchival;
    this.archivalRecordsPurgeService = archivalRecordsPurgeService;
    this.jobsRepository = jobsRepository;
    this.dataRetentionJobsRepository = dataRetentionJobsRepository;
  }

  @Scheduled(cron = "${archival.removeExpired.cron}")
  public void uploadArchivalRecords() {
    scheduledTaskExecutor.execute(this::purgeRecordsByDate);
  }

  private void purgeRecordsByDate() {
    String jobStatus = "Completed";
    Instant startTime = Instant.now();
    try {
      Instant lastUpdateDate = getLatUpdatedDateByJobNameAndSatatus("BIExtract", "Completed");
      Instant purgeDate = lastUpdateDate.minus(daysToPurgeArchival, ChronoUnit.DAYS);
      log.info("purgeupdateDate {}", purgeDate);
      startTime = Instant.now();
      archivalRecordsPurgeService.deleteByArchivalDateBefore(purgeDate);
    } catch (Exception e) {
      jobStatus = "failed";
      log.error(ArchivalRecordsPurgeTask.class.getName(), e);
    } finally {

      Instant endTime = Instant.now();
      dataRetentionJobsRepository.save(
          DataRetentionJobs.builder()
              .endTimestamp(endTime)
              .jobName("ArchivalPurgeJob")
              .startTimestamp(startTime)
              .runSatus(jobStatus)
              .build());
    }
  }

  private Instant getLatUpdatedDateByJobNameAndSatatus(String jobName, String status) {
    Jobs job = jobsRepository.findFirstByJobNameAndJobStatusOrderByUpdatedDateDesc(jobName, status);
    return job.getUpdatedDate();
  }
}
