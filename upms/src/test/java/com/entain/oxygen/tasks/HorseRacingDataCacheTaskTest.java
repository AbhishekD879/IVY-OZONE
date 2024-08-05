package com.entain.oxygen.tasks;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import com.entain.oxygen.service.siteserver.SiteServerService;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class HorseRacingDataCacheTaskTest {

  @Mock private SiteServerService siteServerService;
  @Mock private CacheManager cacheManager;

  private MasterSlaveExecutor masterSlaveExecutor;

  HorseRacingDataCacheTask horseRacingDataCacheTask;

  class MasterSlaveExecutorImpl implements MasterSlaveExecutor {

    @Override
    public void executeIfMaster(Runnable runnable, Runnable runnable1) {

      runnable.run();
      runnable1.run();
    }
  }

  @Test
  void runJobShouldPutDataIntoCache1() {
    masterSlaveExecutor = new MasterSlaveExecutorImpl();
    horseRacingDataCacheTask =
        new HorseRacingDataCacheTask(siteServerService, cacheManager, masterSlaveExecutor);
    ReflectionTestUtils.setField(horseRacingDataCacheTask, "uKIECache", "uk_ie_ss_horse");
    Cache cacheMock = mock(Cache.class);
    when(cacheManager.getCache("uk_ie_ss_horse")).thenReturn(cacheMock);
    masterSlaveExecutor.executeIfMaster(
        () -> horseRacingDataCacheTask.runJob(), () -> horseRacingDataCacheTask.slaveAction());
    verify(cacheMock, times(1)).put(any(), any());
  }

  @Test
  void runJobShouldHandleException() {
    Cache cacheMock = mock(Cache.class);

    masterSlaveExecutor = new MasterSlaveExecutorImpl();
    horseRacingDataCacheTask =
        new HorseRacingDataCacheTask(siteServerService, cacheManager, masterSlaveExecutor);
    ReflectionTestUtils.setField(horseRacingDataCacheTask, "uKIECache", "uk_ie_ss_horse");
    when(cacheManager.getCache("uk_ie_ss_horse")).thenReturn(null);
    masterSlaveExecutor.executeIfMaster(
        () -> horseRacingDataCacheTask.runJob(), () -> horseRacingDataCacheTask.slaveAction());
    verify(cacheMock, times(0)).put(any(), any());
  }
}
