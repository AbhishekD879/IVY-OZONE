package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CouponStatsWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponStatsWidget;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponStatsWidgetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponStatsWidgetService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.Arrays;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {CouponStatsWidgetPublicApi.class, CouponStatsWidgetService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class CouponStatsWidgetPublicApiTest extends AbstractControllerTest {

  @MockBean CouponStatsWidgetRepository repository;
  @MockBean ImageService imageService;
  CouponStatsWidget entity;
  CouponStatsWidgetDto dto;
  ModelMapper mapper = new ModelMapper();

  @Before
  public void init() {
    dto = createDto();
    entity = mapper.map(dto, CouponStatsWidget.class);
    entity.setId("12121212121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
  }

  @Test
  public void testFindByBrand() throws Exception {

    given(repository.findByBrand("bma")).willReturn(Arrays.asList(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coupon-stats-widget/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testFindByBrandNotFound() throws Exception {
    given(repository.findByBrand("bma")).willReturn(null);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coupon-stats-widget/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().isNotFound());
  }

  private CouponStatsWidgetDto createDto() {
    CouponStatsWidgetDto couponStatsWidgetDto = new CouponStatsWidgetDto();
    couponStatsWidgetDto.setButtonText("OK,Thanks");
    couponStatsWidgetDto.setImageUrl("image.com");
    couponStatsWidgetDto.setIsEnable(true);
    couponStatsWidgetDto.setDisplayFrom(Instant.now());
    couponStatsWidgetDto.setDisplayTo(Instant.now());
    couponStatsWidgetDto.setBrand("bma");
    return couponStatsWidgetDto;
  }
}
