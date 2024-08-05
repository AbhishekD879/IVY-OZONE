package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Dashboard;
import com.ladbrokescoral.oxygen.cms.api.repository.DashboardRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.OffsetLimitPageable;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class DashboardService extends AbstractService<Dashboard>
    implements PageableCrudService<Dashboard> {

  private final DashboardRepository dashboardRepository;
  private final Integer daysDuration;
  private ScheduledTaskExecutor scheduledTaskExecutor;

  @Autowired
  public DashboardService(
      DashboardRepository dashboardRepository,
      @Value("${dashboard.removeExpired.afterDays}") Integer daysDuration,
      ScheduledTaskExecutor scheduledTaskExecutor) {
    super(dashboardRepository);
    this.dashboardRepository = dashboardRepository;
    this.daysDuration = daysDuration;
    this.scheduledTaskExecutor = scheduledTaskExecutor;
  }

  @Override
  public List<Dashboard> findAll(int offset, int limit) {
    Page<Dashboard> dashboards =
        dashboardRepository.findAll(new OffsetLimitPageable(offset, limit));
    return dashboards.getContent();
  }

  @Scheduled(cron = "${dashboard.removeExpired.cron}")
  public void removeExpiredEntities() {
    scheduledTaskExecutor.execute(
        () ->
            dashboardRepository.removeDashboardsByCreatedAtBefore(
                Instant.now().minus(Duration.ofDays(daysDuration))));
  }

  public List<Dashboard> readByDate(LocalDate date) {
    Instant instant = date.atStartOfDay().toInstant(ZoneOffset.UTC);
    return dashboardRepository.findDashboardsByCreatedAt(instant, instant.plus(Duration.ofDays(1)));
  }
}
