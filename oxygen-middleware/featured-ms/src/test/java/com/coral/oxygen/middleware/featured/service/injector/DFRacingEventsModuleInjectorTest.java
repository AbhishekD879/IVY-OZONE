package com.coral.oxygen.middleware.featured.service.injector;

import com.coral.oxygen.df.api.DFService;
import com.coral.oxygen.middleware.common.mappers.DFGreyhoundRacingOutcomeMapper;
import com.coral.oxygen.middleware.common.mappers.DFHorseRacingOutcomeMapper;
import com.coral.oxygen.middleware.common.mappers.DFRacingEventDataMapper;
import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.pojos.model.cms.Module;
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent;
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContentItem;
import com.coral.oxygen.middleware.pojos.model.df.Horse;
import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import com.coral.oxygen.middleware.pojos.model.df.Runner;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Optional;
import java.util.UUID;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(MockitoJUnitRunner.class)
public class DFRacingEventsModuleInjectorTest {

  private static final int HORSE_RACE_CATEGORY_ID = 21;

  private static final int GREYHOUND_CATEGORY_ID = 19;

  @Mock DFService dfService;
  private DFHorseRacingOutcomeMapper horseMapper =
      new DFHorseRacingOutcomeMapper(HORSE_RACE_CATEGORY_ID);
  private DFGreyhoundRacingOutcomeMapper grayHoundMapper =
      new DFGreyhoundRacingOutcomeMapper(GREYHOUND_CATEGORY_ID);
  private DFRacingEventDataMapper dfRacingEventDataMapper = new DFRacingEventDataMapper();

  @Test
  public void injectData() {
    DFRacingEventsModuleInjector injector =
        new DFRacingEventsModuleInjector(
            dfService, horseMapper, grayHoundMapper, dfRacingEventDataMapper);

    ModularContentItem item = new ModularContentItem();
    item.setRacingEventsIds(Arrays.asList(4567L, 456L));
    ModularContent modularContent = new ModularContent(Arrays.asList(item));
    ArrayList<EventsModuleData> items = new ArrayList<>();
    EventsModuleData data1 = getEventsModuleData("21", 456L, 1);
    EventsModuleData data2 = getEventsModuleData("19", 4567L, 1);
    EventsModuleData data3 = getEventsModuleData("21", 14567L, 1);
    EventsModuleData data4 = getEventsModuleData("21", 404L, null);
    EventsModuleData data5 = getEventsModuleData(null, 4040L, 1);
    items.add(data1);
    items.add(data2);
    items.add(data3);
    items.add(data4);
    items.add(data5);
    ArrayList<Module> modules = new ArrayList<>();
    Module module = new Module();
    module.setData(items);
    modules.add(module);
    item.setModules(modules);

    HashMap<Long, RaceEvent> dogs = getGreyhoundEvents();
    Mockito.when(dfService.getRaceEvents(Mockito.eq(19), Mockito.any()))
        .thenReturn(Optional.of(dogs));

    HashMap<Long, RaceEvent> value = getHorseEvents();
    Mockito.when(dfService.getRaceEvents(Mockito.eq(21), Mockito.any()))
        .thenReturn(Optional.of(value));

    injector.injectData(items, new IdsCollector(modularContent, item));

    Assert.assertEquals("100", data1.getRacingFormEvent().getDistance());
    Assert.assertEquals(
        "m", data2.getMarkets().get(0).getOutcomes().get(0).getRacingFormOutcome().getGenderCode());
  }

  private HashMap<Long, RaceEvent> getHorseEvents() {
    HashMap<Long, RaceEvent> value = new HashMap<>();
    addHorseRaceEvent(value, 456L);
    addHorseRaceEvent(value, 404L);
    return value;
  }

  private HashMap<Long, RaceEvent> getGreyhoundEvents() {
    HashMap<Long, RaceEvent> value = new HashMap<>();
    getGreyhoundEvents(value, 4567L);
    getGreyhoundEvents(value, 404L);
    return value;
  }

  private void addHorseRaceEvent(HashMap<Long, RaceEvent> value, long id) {
    RaceEvent value1 = new RaceEvent();
    value1.setGoingCode("going1");
    value1.setDistance("100m");
    value1.setYards(100);
    ArrayList<Horse> horses = new ArrayList<>();
    Horse horse1 = getHorse(1, "15");
    Horse horse2 = getHorse(2, "15");
    horses.add(horse1);
    horses.add(horse2);
    value1.setHorses(horses);
    value.put(id, value1);
  }

  private void getGreyhoundEvents(HashMap<Long, RaceEvent> value, long id) {
    RaceEvent value1 = new RaceEvent();
    ArrayList<Runner> horses = new ArrayList<>();
    Runner horse1 = getRunner(1, "m");
    Runner horse2 = getRunner(2, "f");
    horses.add(horse1);
    horses.add(horse2);
    value1.setRunners(horses);
    value.put(id, value1);
  }

  private Horse getHorse(int saddle, String weight) {
    Horse e = new Horse();
    e.setSaddle(saddle);
    e.setWeight(weight);
    return e;
  }

  private Runner getRunner(int saddle, String sex) {
    Runner e = new Runner();
    e.setTrap(saddle);
    e.setDogSex(sex);
    return e;
  }

  private EventsModuleData getEventsModuleData(String categoryId, long id, Integer runnerNumber) {
    EventsModuleData data = new EventsModuleData();
    ReflectionTestUtils.setField(data, "marketId", id);
    data.setId(id);
    data.setCategoryId(categoryId);
    ArrayList<OutputMarket> markets = new ArrayList<>();
    OutputMarket outputMarket = new OutputMarket();
    outputMarket.setId(UUID.randomUUID().toString());
    ArrayList<OutputOutcome> outcomes = new ArrayList<>();
    OutputOutcome e = getOutputOutcome(runnerNumber);
    outcomes.add(e);
    outputMarket.setOutcomes(outcomes);
    markets.add(outputMarket);
    data.setMarkets(markets);
    return data;
  }

  private OutputOutcome getOutputOutcome(Integer runnerNumber) {
    OutputOutcome e = new OutputOutcome();
    e.setRunnerNumber(runnerNumber);
    if (runnerNumber == null) {
      runnerNumber = -1;
    }
    e.setId(String.valueOf(runnerNumber));
    e.setName("runner" + runnerNumber);

    return e;
  }
}
