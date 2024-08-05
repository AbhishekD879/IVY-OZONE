package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static com.ladbrokescoral.oxygen.cms.api.controller.ApiConstants.PRIVATE_API;
import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.HomeModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.entity.DataSelection;
import com.ladbrokescoral.oxygen.cms.api.entity.EventsSelectionSetting;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.Visibility;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.EventHubService;
import com.ladbrokescoral.oxygen.cms.api.service.HomeModuleSiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.temporal.ChronoUnit;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.data.domain.Sort;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

@RunWith(SpringRunner.class)
@WebMvcTest({
  HomeModules.class,
  AuthenticationService.class,
  HomeModuleServiceImpl.class,
  SegmentService.class
})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({
  HomeModuleArchivalRepository.class,
  UserService.class,
  SegmentService.class,
  EventHubService.class
})
@Import(ModelMapperConfig.class)
public class HomeModuleControllerIntegrationTest {

  @Autowired private MockMvc mockMvc;

  @MockBean private HomeModuleSiteServeService homeModuleSiteServeService;
  @MockBean private HomeModuleRepository homeModuleRepository;
  @MockBean private SegmentArchivalRepository segmentArchivalRepository;

  // Test if Spring boot serialize Date with format yyyy-MM-ddTHH:mm:ssZ
  @Test
  public void testFindAllWithCorrectDateFormat() throws Exception {
    HomeModule homeModule = createHomeModule();

    given(homeModuleRepository.findAllActive(Mockito.any(Instant.class)))
        .willReturn(Arrays.asList(homeModule));

    mockMvc
        .perform(get(PRIVATE_API + "/home-module"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(1)))
        .andExpect(jsonPath("$[0].visibility.displayTo", is("2017-01-05T10:00:00Z")));
  }

  @Test
  public void testCreateHomeModule() throws Exception {
    HomeModule homeModule = createValidHomeModule();

    given(homeModuleRepository.save(Mockito.any(HomeModule.class))).willReturn(homeModule);

    mockMvc
        .perform(
            post(PRIVATE_API + "/home-module")
                .content(TestUtil.convertObjectToJsonBytes(homeModule))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testFindHomeModule() throws Exception {
    HomeModule homeModule = createValidHomeModule();

    given(homeModuleRepository.findById(Mockito.any(String.class)))
        .willReturn(Optional.of(homeModule));

    mockMvc.perform(get(PRIVATE_API + "/home-module/123")).andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testFindHomeModuleNotFound() throws Exception {
    // HomeModule homeModule = createValidHomeModule();

    Mockito.when(homeModuleRepository.findById(Mockito.any(String.class)))
        .thenReturn(Optional.empty());

    mockMvc.perform(get(PRIVATE_API + "/home-module/123")).andExpect(status().is4xxClientError());
  }

  @Test
  public void testFindAllByBrand() throws Exception {
    HomeModule homeModule = createHomeModule();

    given(
            homeModuleRepository.findAllActiveAndPublishToChannel(
                Mockito.any(Instant.class), Mockito.any(String.class), Mockito.any(Sort.class)))
        .willReturn(Arrays.asList(homeModule));

    mockMvc
        .perform(get(PRIVATE_API + "/home-module/brand/bma"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(1)))
        .andExpect(jsonPath("$[0].visibility.displayTo", is("2017-01-05T10:00:00Z")));
  }

  @Test
  public void testFindAllByBrandInActive() throws Exception {
    HomeModule homeModule = createHomeModule();

    given(
            homeModuleRepository.findAllInactiveAndPublishToChannel(
                Mockito.any(Instant.class), Mockito.any(String.class), Mockito.any(Sort.class)))
        .willReturn(Arrays.asList(homeModule));

    mockMvc
        .perform(get(PRIVATE_API + "/home-module/brand/bma?active=false"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(1)))
        .andExpect(jsonPath("$[0].visibility.displayTo", is("2017-01-05T10:00:00Z")));
  }

  @Test
  public void testFindAllByBrandAndPageType() throws Exception {
    HomeModule homeModule = createHomeModule();

    given(
            homeModuleRepository.findAll(
                Mockito.any(String.class),
                Mockito.any(PageType.class),
                Mockito.any(String.class),
                Mockito.any(Sort.class)))
        .willReturn(Arrays.asList(homeModule));

    mockMvc
        .perform(get(PRIVATE_API + "/home-module/brand/bma/sport/123"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(1)))
        .andExpect(jsonPath("$[0].visibility.displayTo", is("2017-01-05T10:00:00Z")));
  }

  @Test
  public void testUpdateHomeModule() throws Exception {
    HomeModule homeModule = createValidHomeModule();
    homeModule.setId("1");

    Mockito.when(homeModuleRepository.findById(Mockito.any(String.class)))
        .thenReturn(Optional.of(homeModule));
    given(homeModuleRepository.save(Mockito.any(HomeModule.class))).willReturn(homeModule);

    mockMvc
        .perform(
            put(PRIVATE_API + "/home-module/123")
                .content(TestUtil.convertObjectToJsonBytes(homeModule))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteHomeModule() throws Exception {
    HomeModule homeModule = createValidHomeModule();

    Mockito.when(homeModuleRepository.findById(Mockito.any(String.class)))
        .thenReturn(Optional.of(homeModule));

    mockMvc.perform(delete(PRIVATE_API + "/home-module/123")).andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteHomeModuleNotFind() throws Exception {
    mockMvc
        .perform(delete(PRIVATE_API + "/home-module/123"))
        .andExpect(status().is4xxClientError());
  }

  private HomeModule createHomeModule() {
    HomeModule homeModule = new HomeModule();
    Visibility visibility = getVisibility();
    homeModule.setVisibility(visibility);
    return homeModule;
  }

  private HomeModule createValidHomeModule() {
    HomeModule homeModule = createHomeModule();
    homeModule.setDataSelection(getDataSelection());
    EventsSelectionSetting settings = new EventsSelectionSetting();
    settings.setFrom(Instant.now().minus(1, ChronoUnit.DAYS));
    settings.setTo(Instant.now());
    homeModule.setEventsSelectionSettings(settings);
    homeModule.setTitle("homeModule");
    homeModule.setPublishToChannels(Arrays.asList("mobile"));
    homeModule.setId("id");
    return homeModule;
  }

  private DataSelection getDataSelection() {
    DataSelection dataSelection = new DataSelection();
    dataSelection.setSelectionId("12345");
    dataSelection.setSelectionType("SGL");
    return dataSelection;
  }

  private Visibility getVisibility() {
    Visibility visibility = new Visibility();

    visibility.setDisplayTo(
        LocalDateTime.of(2017, 01, 05, 10, 00, 00, 000).toInstant(ZoneOffset.UTC));
    visibility.setDisplayFrom(
        LocalDateTime.of(2016, 01, 05, 10, 00, 00, 000).toInstant(ZoneOffset.UTC));
    return visibility;
  }
}
