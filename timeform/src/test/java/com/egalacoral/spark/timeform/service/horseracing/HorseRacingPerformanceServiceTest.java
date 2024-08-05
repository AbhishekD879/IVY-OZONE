package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.model.horseracing.HRPerformance;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.Arrays;
import java.util.Collection;
import java.util.Map;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class HorseRacingPerformanceServiceTest {

  @Mock private Storage instance;

  @Test
  public void testGetPerfomance() {
    HorseRacingPerformanceService service = new HorseRacingPerformanceService(instance);
    Collection<Object> list = Arrays.asList(perfomance(1), perfomance(2));
    Map<Object, Object> map = Mockito.mock(Map.class);
    Mockito.when(instance.getMap(Mockito.anyObject())).thenReturn(map);
    Mockito.when(map.values()).thenReturn(list);

    Optional<HRPerformance> optional = service.getPerfomance("md:1:1:hr1");
    Assert.assertTrue(optional.isPresent());
  }

  protected HRPerformance perfomance(int courseId) {
    HRPerformance hrPerformance = new HRPerformance();
    hrPerformance.setMeetingDate("md");
    hrPerformance.setCourseId(courseId);
    hrPerformance.setHorseCode("hr1");
    hrPerformance.setRaceNumber(1);
    return hrPerformance;
  }
}
