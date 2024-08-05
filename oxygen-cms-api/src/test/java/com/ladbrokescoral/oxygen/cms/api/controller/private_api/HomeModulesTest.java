package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl.SORT_BY_DISPLAY_ORDER_ASC;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.HomeModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.Visibility;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.EventHubService;
import com.ladbrokescoral.oxygen.cms.api.service.HomeModuleSiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import com.ladbrokescoral.oxygen.cms.util.WithMockCustomUser;
import java.time.Instant;
import java.util.Arrays;
import java.util.Optional;
import java.util.UUID;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({HomeModules.class, HomeModuleServiceImpl.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({
  BrandService.class,
  // ImageEntityService.class,
  // SvgEntityService.class,
  HomeModuleSiteServeService.class,
  SegmentService.class,
  EventHubService.class,
  HomeModuleArchivalRepository.class
})
@Import(ModelMapperConfig.class)
public class HomeModulesTest extends AbstractControllerTest {

  @MockBean private HomeModuleRepository homeModuleRepository;

  private HomeModule homeModule;

  @Before
  public void init() {
    homeModule = HomeModuleControllerTest.create(PageType.eventhub, "2");
    homeModule.setVisibility(createVisibility());
    given(homeModuleRepository.findById(any(String.class))).willReturn(Optional.of(homeModule));
    given(homeModuleRepository.save(any(HomeModule.class))).willReturn(homeModule);
    given(
            homeModuleRepository.findAllUniversalByBrandAndPageIdAndPageType(
                "bma", PageType.valueOf("sport"), "0", SORT_BY_DISPLAY_ORDER_ASC))
        .willReturn(Arrays.asList(homeModule));

    given(
            homeModuleRepository.findAllPublishToChannelAndSegmentNameAndIsActive(
                Instant.now(), "bma", Arrays.asList("segment1"), true, SORT_BY_DISPLAY_ORDER_ASC))
        .willReturn(Arrays.asList(homeModule));
  }

  @Test
  @WithMockCustomUser
  public void testOrderMenu() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/home-module/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testDeleteModule() throws Exception {
    homeModule = HomeModuleControllerTest.create(PageType.eventhub, "2");
    homeModule.setVisibility(createVisibility());
    homeModule.setId("1");
    given(homeModuleRepository.findById("1")).willReturn(Optional.of(homeModule), Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/home-module/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testReadByBrandAndPageTypeAndSegmentName() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/home-module/brand/bma/sport/0/segment/universal")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testReadByBrandAndSegmentName() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/home-module/brand/bma/segment/segment1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  private OrderDto createOrderDto() {
    OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("1", "2", "3"))
            .segmentName("segment1")
            .id(UUID.randomUUID().toString())
            .build();
    return orderDto;
  }

  private Visibility createVisibility() {
    Visibility visibility = new Visibility();
    visibility.setDisplayFrom(Instant.now());
    visibility.setDisplayTo(Instant.now().plusSeconds(60 * 60 * 24));
    visibility.setEnabled(true);
    return visibility;
  }
}
