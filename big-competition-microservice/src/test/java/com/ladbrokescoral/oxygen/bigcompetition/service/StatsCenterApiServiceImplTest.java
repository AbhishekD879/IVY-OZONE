package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.ladbrokescoral.oxygen.bigcompetition.dto.StatsResultTableReqParams;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.StatsCenterApiServiceCachable;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.StatsCenterApiServiceImpl;
import java.util.Map;
import org.apache.commons.lang3.reflect.FieldUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.util.Assert;

@RunWith(MockitoJUnitRunner.class)
public class StatsCenterApiServiceImplTest {
  public static final int REFRESH_RATE = 1000; // 1s
  public static final int CACHE_REFRESH_COUNT_AFTER_IT_THREAD_VALUE_UNUSED = 10;
  StatsCenterApiServiceImpl statsCenterApiService;
  @Mock StatsCenterApiServiceCachable statsCenterApiServiceCachable;

  @Before
  public void setUp() throws Exception {
    statsCenterApiService =
        new StatsCenterApiServiceImpl(
            statsCenterApiServiceCachable,
            REFRESH_RATE,
            CACHE_REFRESH_COUNT_AFTER_IT_THREAD_VALUE_UNUSED);
  }

  @Test
  public void testRefreshStatsResultTables() throws IllegalAccessException {
    Map<StatsResultTableReqParams, Long> regParams =
        (Map<StatsResultTableReqParams, Long>)
            FieldUtils.readField(statsCenterApiService, "regParams", true);
    Assert.isTrue(regParams.isEmpty(), "Map should be empty before test");

    // setup
    statsCenterApiService.getResultTables(42, 42, 42, 42);
    statsCenterApiService.getResultTables(42, 42, 42, 42);
    statsCenterApiService.getResultTables(13, 13, 13, 13);
    // validation
    Assert.isTrue(regParams.size() == 2, "There should be 2 obj with request params");

    // setup
    StatsResultTableReqParams statsResultTableReqParams =
        new StatsResultTableReqParams()
            .setSportId(42)
            .setAreaId(42)
            .setCompetitionId(42)
            .setSeasonId(42);
    Long oldEventTimeStamp =
        regParams.get(statsResultTableReqParams)
            - REFRESH_RATE * CACHE_REFRESH_COUNT_AFTER_IT_THREAD_VALUE_UNUSED
            - 1;
    regParams.put(statsResultTableReqParams, oldEventTimeStamp);
    // process
    statsCenterApiService.refreshStatsResultTables();
    // validation
    verify(statsCenterApiServiceCachable, times(1)).cachePutResultTables(13, 13, 13, 13);
  }
}
