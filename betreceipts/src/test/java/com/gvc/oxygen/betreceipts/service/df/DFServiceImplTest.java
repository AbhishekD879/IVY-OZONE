package com.gvc.oxygen.betreceipts.service.df;

import com.coral.oxygen.df.api.DFClient;
import com.coral.oxygen.df.model.RaceEvent;
import com.gvc.oxygen.betreceipts.config.DFApiConfig;
import com.gvc.oxygen.betreceipts.dto.RaceDTO;
import com.gvc.oxygen.betreceipts.mapping.GenericMapper;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.modelmapper.ModelMapper;
import org.modelmapper.convention.MatchingStrategies;

@ExtendWith(MockitoExtension.class)
public class DFServiceImplTest extends BDDMockito implements WithAssertions {

  @Mock private DFClient dfClient;

  @Mock private DFApiConfig config;

  @Spy
  private GenericMapper<Map<Long, RaceEvent>, Map<Long, RaceDTO>> mapper =
      new GenericMapper<>(modelMapper());

  @InjectMocks private DFServiceImpl dfService;

  @Test
  public void testGetNextRaces() throws IOException {
    Optional<Map<Long, RaceDTO>> nextRaces = null;
    mockDataFabric();
    nextRaces = dfService.getNextRaces(21, Arrays.asList(1L, 2L));
    assertThat(nextRaces)
        .isNotNull()
        .isPresent()
        .get()
        .extracting(e -> e.get(1L).getDistance())
        .isEqualTo("123");
  }

  private void mockDataFabric() throws IOException {
    Map<Long, RaceEvent> races = new HashMap<>();
    races.put(1L, buildRaceEvent());
    races.put(3L, buildRaceEvent());
    when(config.api()).thenReturn(dfClient);
    when(dfClient.getRaceEvents(anyInt(), anyCollection())).thenReturn(Optional.of(races));
  }

  private RaceEvent buildRaceEvent() {
    RaceEvent raceEvent = new RaceEvent();
    raceEvent.setDistance("123");
    return raceEvent;
  }

  private ModelMapper modelMapper() {
    ModelMapper modelMapper = new ModelMapper();
    modelMapper.getConfiguration().setMatchingStrategy(MatchingStrategies.STRICT);
    return modelMapper;
  }
}
