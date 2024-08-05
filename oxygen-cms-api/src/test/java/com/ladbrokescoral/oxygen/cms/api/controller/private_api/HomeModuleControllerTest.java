package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.HomeModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.dto.HomeModuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DataSelection;
import com.ladbrokescoral.oxygen.cms.api.entity.Device;
import com.ladbrokescoral.oxygen.cms.api.entity.EventsSelectionSetting;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SelectionType;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.EventHubService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentedModuleSerive;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.ResponseEntity;

@RunWith(MockitoJUnitRunner.class)
public class HomeModuleControllerTest extends BDDMockito {

  @Mock private HomeModuleRepository homeModuleRepository;
  @Mock private EventHubService hubService;
  @Mock private UserService userService;

  private HomeModules homeModuleController;
  @Spy private ModelMapper modelMapper;
  HomeModuleServiceImpl homemoduleService;
  @Mock private SegmentedModuleSerive segmentedModuleSerive;

  @Mock private HomeModuleArchivalRepository homeModuleArchivalRepository;
  @Mock SegmentService segmentService;
  @MockBean private SegmentArchivalRepository segmentArchivalRepository;

  @Before
  public void setUp() throws Exception {

    homeModuleController =
        new HomeModules(
            new HomeModuleServiceImpl(
                homeModuleRepository,
                homeModuleArchivalRepository,
                modelMapper,
                segmentService,
                hubService),
            null);

    homeModuleController.setUserService(userService);

    List<HomeModule> active =
        Arrays.asList(
            TestUtil.deserializeWithJackson(
                "controller/private_api/home_module_active_entities.json", HomeModule.class));
    List<HomeModule> inactive =
        Arrays.asList(
            TestUtil.deserializeWithJackson(
                "controller/private_api/home_module_inactive_entities.json", HomeModule.class));

    when(homeModuleRepository.findAllActive(any())).thenReturn(active);
    when(homeModuleRepository.findAllInactive(any())).thenReturn(inactive);
  }

  @Test
  public void testFindListByActiveStatus() {
    ResponseEntity result = homeModuleController.findAll(true);
    assertTrue(result.getStatusCode().is2xxSuccessful());
    List<HomeModuleDto> body = (List<HomeModuleDto>) result.getBody();
    verify(homeModuleRepository).findAllActive(any());
    assertEquals(new Long(1), body.get(0).getShowEventsForDays());
  }

  @Test
  public void testFindListByInactiveStatus() {
    ResponseEntity result = homeModuleController.findAll(false);
    assertTrue(result.getStatusCode().is2xxSuccessful());
    List<HomeModuleDto> body = (List<HomeModuleDto>) result.getBody();
    verify(homeModuleRepository).findAllInactive(any());
    assertEquals(new Long(1), body.get(0).getShowEventsForDays());
  }

  @Test
  public void testSave() {
    HomeModule module = create(PageType.sport, "0");
    when(homeModuleRepository.save(any(HomeModule.class))).thenReturn(module);
    ResponseEntity result = homeModuleController.create(module);
    assertTrue(result.getStatusCode().is2xxSuccessful());
  }

  @Test
  public void testSaveAutoRefreshModule() {
    HomeModule module = create(PageType.sport, "0");
    module.getEventsSelectionSettings().setAutoRefresh(true);
    when(homeModuleRepository.save(any(HomeModule.class))).thenReturn(module);
    ResponseEntity result = homeModuleController.create(module);
    assertTrue(result.getStatusCode().is2xxSuccessful());
  }

  @Test(expected = IllegalArgumentException.class)
  public void testFailedToSaveAutoRefreshEventModule() {
    HomeModule module = create(PageType.sport, "0");
    module.getEventsSelectionSettings().setAutoRefresh(true);
    module.getDataSelection().setSelectionType(SelectionType.EVENT.getValue());
    homeModuleController.create(module);
  }

  @Test
  public void testSaveMultipleIdsRaceModule() {
    HomeModule module = create(PageType.sport, "0");
    module.getEventsSelectionSettings().setAutoRefresh(true);
    module.setDataSelection(new DataSelection(SelectionType.RACE_TYPE_ID.getValue(), "445,332"));
    when(homeModuleRepository.save(any(HomeModule.class))).thenReturn(module);
    ResponseEntity result = homeModuleController.create(module);
    assertTrue(result.getStatusCode().is2xxSuccessful());
  }

  @Test(expected = IllegalArgumentException.class)
  public void testFailedToSaveMultipleSelectionIdsModule() {
    HomeModule module = create(PageType.sport, "0");
    module.getEventsSelectionSettings().setAutoRefresh(true);
    module.setDataSelection(new DataSelection(SelectionType.CATEGORY.getValue(), "445,332"));
    homeModuleController.create(module);
  }

  public static HomeModule create(PageType pageType, String pageId) {
    HomeModule module = new HomeModule();
    module.setPageType(pageType);
    module.setPageId(pageId);
    module.setCreatedBy("test");
    Map<String, Device> publishedDevices = new HashMap<String, Device>();
    publishedDevices.put("111", new Device());
    module.setPublishedDevices(publishedDevices);
    module.setPublishToChannels(new ArrayList<>(publishedDevices.keySet()));
    module.setDataSelection(new DataSelection(SelectionType.TYPE.getValue(), "123"));
    module.setEventsSelectionSettings(new EventsSelectionSetting());
    return module;
  }

  @Test(expected = IllegalArgumentException.class)
  public void testSaveLinkedToEventHubNoBrand() {
    HomeModule module = new HomeModule();
    module.setPageType(PageType.eventhub);
    homeModuleController.create(module);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testSaveLinkedToSportNoBrand() {
    HomeModule module = new HomeModule();
    module.setPageType(PageType.sport);
    module.setPageId("2");
    homeModuleController.create(module);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testSaveLinkedToEventHubMultiBrand() {
    HomeModule module = new HomeModule();
    module.setPageType(PageType.eventhub);
    module.setPageId("2");
    Map<String, Device> publishedDevices = new HashMap<String, Device>();
    publishedDevices.put("111", new Device());
    publishedDevices.put("222", new Device());
    module.setPublishedDevices(publishedDevices);
    homeModuleController.create(module);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testSaveLinkedToInvalidEventHub() {
    HomeModule module = new HomeModule();
    module.setPageType(PageType.eventhub);
    module.setPageId("2");
    Map<String, Device> publishedDevices = new HashMap<String, Device>();
    publishedDevices.put("111", new Device());
    module.setPublishedDevices(publishedDevices);
    module.setDataSelection(new DataSelection(SelectionType.EVENT.getValue(), "123"));
    homeModuleController.create(module);
  }

  @Test
  public void testSaveLinkedToValidEventHub() {
    HomeModule module = create(PageType.eventhub, "2");

    when(hubService.existByBrandAndIndexNumber("111", 2)).thenReturn(Boolean.TRUE);
    when(homeModuleRepository.save(any(HomeModule.class))).thenReturn(module);
    homeModuleController.create(module);

    verify(hubService, times(1)).existByBrandAndIndexNumber("111", 2);
    verify(homeModuleRepository, times(1)).save(any(HomeModule.class));
  }
}
