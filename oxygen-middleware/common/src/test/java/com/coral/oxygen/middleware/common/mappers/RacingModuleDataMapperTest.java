package com.coral.oxygen.middleware.common.mappers;

import static org.mockito.Mockito.*;

import com.egalacoral.spark.siteserver.model.*;
import com.oxygen.middleware.common.utils.TestUtils;
import java.util.ArrayList;
import java.util.List;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = {RacingModuleDataMapper.class})
@AutoConfigureMockMvc(addFilters = false)
@MockitoSettings(strictness = Strictness.LENIENT)
public class RacingModuleDataMapperTest {

  // @MockBean Event event;
  // @MockBean Market market;

  @Test
  public void mapEmpty() {
    RacingModuleDataMapper mapper = new RacingModuleDataMapper();
    Event d = new Event();
    mapper.mapInternationalToteData(d, new String(), new String());
    Assert.assertNull(d.getAwayTeamExtIds());
  }

  @Test
  public void mapEmpty1() {
    RacingModuleDataMapper mapper = new RacingModuleDataMapper();
    Event d = new Event();
    mapper.mapVirtualCarouselData(d);
    Assert.assertNull(d.getAwayTeamExtIds());
  }

  @Test
  public void mapEmpty2() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId.json", Event.class);
    RacingModuleDataMapper mapper = new RacingModuleDataMapper();
    List<String> poolTypes = new ArrayList<>();
    mapper.mapRacingEventData(events.get(0), poolTypes);
    Assert.assertNotNull(events.get(0).getName());
  }

  @Test
  public void mapRacingReferenceEachWayTerms() {
    List<Event> events =
        TestUtils.deserializeListWithJackson(
            "event_with_reference_eachway_terms.json", Event.class);
    RacingModuleDataMapper mapper = new RacingModuleDataMapper();
    List<String> poolTypes = new ArrayList<>();
    mapper.mapRacingEventData(events.get(0), poolTypes);
    Assert.assertNotNull(events.get(0).getName());
  }
}
