package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyCollection;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyZeroInteractions;

import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DataSelection;
import com.ladbrokescoral.oxygen.cms.api.entity.Device;
import com.ladbrokescoral.oxygen.cms.api.entity.EventsSelectionSetting;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModuleData;
import com.ladbrokescoral.oxygen.cms.api.entity.SelectionType;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleAutoUpdateScheduler;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class HomeModuleAutoUpdateSchedulerTest {
  @Mock private HomeModuleRepository repository;
  @Mock private HomeModuleSiteServeService homeModuleSiteServeService;
  private HomeModuleAutoUpdateScheduler homeModuleAutoUpdateScheduler;
  private Integer daysDuration = 7;
  @Mock private ScheduledTaskExecutor scheduledTaskExecutorMock;
  @Captor private ArgumentCaptor<List<HomeModule>> homeModulesCaptor;

  @Before
  public void setUp() {
    homeModuleAutoUpdateScheduler =
        new HomeModuleAutoUpdateScheduler(
            homeModuleSiteServeService, repository, daysDuration, scheduledTaskExecutorMock);

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
    homeModuleAutoUpdateScheduler.removeExpiredEntities();
    verify(repository, times(1)).removeHomeModulesByVisibilityDisplayToBefore(any());
  }

  @Test
  public void testSSNotCalledWhenNoEntitiesToAutoUpdate() {
    doReturn(Collections.emptyList())
        .when(repository)
        .findWithAutoRefreshAndSelectionTypeIn(any(), any());

    homeModuleAutoUpdateScheduler.refreshModulesEvents();
    verifyZeroInteractions(homeModuleSiteServeService);
  }

  @Test
  public void testAutoUpdateNoEvents() {
    String brand = "bma";
    SelectionType type = SelectionType.RACE_TYPE_ID;
    String selectionId = "12345";
    List<HomeModule> homeModules =
        Collections.singletonList(createHomeModule(brand, type, selectionId));
    doReturn(homeModules).when(repository).findWithAutoRefreshAndSelectionTypeIn(any(), any());
    doReturn(Collections.emptyList())
        .when(homeModuleSiteServeService)
        .loadEventsFromSiteServe(eq(brand), eq(type), eq(selectionId), any(), any());

    homeModuleAutoUpdateScheduler.refreshModulesEvents();
    verify(homeModuleSiteServeService)
        .loadEventsFromSiteServe(eq(brand), eq(type), eq(selectionId), any(), any());
    verify(repository, never()).saveAll(anyCollection());
  }

  @Test
  public void testAutoUpdateAddNewEvents() {
    String brand = "bma";
    SelectionType type = SelectionType.RACE_TYPE_ID;
    String selectionId = "12345";
    HomeModule homeModule = createHomeModule(brand, type, selectionId);
    homeModule.setData(
        new ArrayList<>(
            Arrays.asList(
                createHomeModuleData("1"), createHomeModuleData("2"), createHomeModuleData("3"))));
    List<HomeModule> homeModules = Collections.singletonList(homeModule);
    doReturn(homeModules).when(repository).findWithAutoRefreshAndSelectionTypeIn(any(), any());
    doReturn(Arrays.asList(createSiteServeEventDto("3"), createSiteServeEventDto("4")))
        .when(homeModuleSiteServeService)
        .loadEventsFromSiteServe(eq(brand), eq(type), eq(selectionId), any(), any());

    homeModuleAutoUpdateScheduler.refreshModulesEvents();

    verify(repository).saveAll(homeModulesCaptor.capture());
    List<HomeModule> savedModules = homeModulesCaptor.getValue();
    assertEquals(1, savedModules.size());
    List<HomeModuleData> savedData = savedModules.get(0).getData();
    assertEquals(2, savedData.size());
    assertTrue(savedData.stream().allMatch(e -> "3".equals(e.getId()) || "4".equals(e.getId())));
  }

  private HomeModule createHomeModule(String brand, SelectionType type, String selectionId) {
    HomeModule homeModule = new HomeModule();
    homeModule.setPublishToChannels(Collections.singletonList(brand));
    homeModule.setPublishedDevices(Collections.singletonMap(brand, new Device()));
    homeModule.setDataSelection(new DataSelection(type.getValue(), selectionId));
    EventsSelectionSetting eventsSelectionSettings = new EventsSelectionSetting();
    eventsSelectionSettings.setAutoRefresh(true);
    eventsSelectionSettings.setTo(Instant.now());
    eventsSelectionSettings.setTo(Instant.now());
    homeModule.setEventsSelectionSettings(eventsSelectionSettings);
    return homeModule;
  }

  private HomeModuleData createHomeModuleData(String id) {
    HomeModuleData data = new HomeModuleData();
    data.setId(id);
    return data;
  }

  private SiteServeEventDto createSiteServeEventDto(String id) {
    SiteServeEventDto event = new SiteServeEventDto();
    event.setId(id);
    return event;
  }
}
