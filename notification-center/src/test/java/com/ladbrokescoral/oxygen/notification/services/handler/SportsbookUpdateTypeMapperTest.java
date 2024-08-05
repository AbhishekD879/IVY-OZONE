package com.ladbrokescoral.oxygen.notification.services.handler;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.*;

import com.google.gson.Gson;
import com.ladbrokescoral.oxyegn.test.utils.Utils;
import com.ladbrokescoral.oxygen.notification.services.ContentConverter;
import com.ladbrokescoral.oxygen.notification.utils.time.TimeProvider;
import java.io.IOException;
import java.util.List;
import org.joda.time.DateTime;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SportsbookUpdateTypeMapperTest {

  private SportsbookUpdateTypeMapper sportsbookUpdateTypeMapper;

  private String goingDownLateUpdate;
  private String goingDownUpdate;
  private String nonRunnerUpdate;
  private String raceOffUpdate;
  private String resultsUpdate;
  private String streamUpdate;

  @Mock private TimeProvider timeProvider;

  @Before
  public void setUp() throws IOException {
    sportsbookUpdateTypeMapper =
        new SportsbookUpdateTypeMapper(new ContentConverter(new Gson()), 15, timeProvider);

    Mockito.when(timeProvider.currentTime()).thenReturn(DateTime.parse("2019-03-29T14:30:00Z"));

    goingDownLateUpdate =
        Utils.fromResource(
            "sportsbook/going_down_late_update.json", this.getClass().getClassLoader());
    goingDownUpdate =
        Utils.fromResource("sportsbook/going_down_update.json", this.getClass().getClassLoader());
    nonRunnerUpdate =
        Utils.fromResource("sportsbook/non_runner_update.json", this.getClass().getClassLoader());
    raceOffUpdate =
        Utils.fromResource("sportsbook/race_off_update.json", this.getClass().getClassLoader());
    resultsUpdate =
        Utils.fromResource("sportsbook/results_update.json", this.getClass().getClassLoader());
    streamUpdate =
        Utils.fromResource(
            "sportsbook/stream_starting_update.json", this.getClass().getClassLoader());
  }

  @Test
  public void filterLateUpdates() {
    List<String> types = sportsbookUpdateTypeMapper.forMessage(goingDownLateUpdate);
    Assert.assertTrue(types.isEmpty());
  }

  @Test
  public void goingDownTest() {
    List<String> types = sportsbookUpdateTypeMapper.forMessage(goingDownUpdate);
    Assert.assertTrue(types.contains(GOING_DOWN.name()));
  }

  @Test
  public void nonRunnerTest() {
    List<String> types = sportsbookUpdateTypeMapper.forMessage(nonRunnerUpdate);
    Assert.assertTrue(types.contains(NON_RUNNER.name()));
  }

  @Test
  public void raceOffTest() {
    List<String> types = sportsbookUpdateTypeMapper.forMessage(raceOffUpdate);
    Assert.assertTrue(types.contains(RACE_OFF.name()));
  }

  @Test
  public void resultsTest() {
    List<String> types = sportsbookUpdateTypeMapper.forMessage(resultsUpdate);
    Assert.assertTrue(types.contains(RESULTS.name()));
  }

  @Test
  public void streamTest() {
    List<String> types = sportsbookUpdateTypeMapper.forMessage(streamUpdate);
    Assert.assertTrue(types.contains(STREAM_STARTING.name()));
  }
}
