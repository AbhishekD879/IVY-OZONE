package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.controller.public_api.CouponAndMarketSwitcherWidgetApi;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponAndMarketSwitcher;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponAndMarketSwitcherWidgetService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {CouponAndMarketSwitcherWidgetApi.class, CouponAndMarketSwitcherWidgetService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class CouponAndMarketSwitcherWidgetApiTest extends AbstractControllerTest {
  CouponAndMarketSwitcher entity;
  @MockBean CouponAndMarketSwitcherWidgetService service;
  ModelMapper mapper = new ModelMapper();

  @Before
  public void init() {
    entity = new CouponAndMarketSwitcher();
    entity.setButtonText("Ok,Thanks!");
    entity.setBrand("ladbrokes");
    entity.setIsEnable(true);
    entity.setImageUrl("file.svg");
    entity.setId("121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
  }

  @Test
  public void testFindByBrand() throws Exception {

    given(service.readByBrand(Mockito.anyString())).willReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/couponAndMarketSwitcherWidget/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }
}
