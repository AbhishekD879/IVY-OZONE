package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineSplashConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineSplashConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineSplashConfigService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {TimelineSplashConfigController.class, TimelineSplashConfigService.class})
@AutoConfigureMockMvc(addFilters = false)
public class TimelineSplashControllerTest extends AbstractControllerTest {

  public static final String CONFIG_ID = "98789987";
  public static final String BRAND = "ladbrokes";

  private TimelineSplashConfig config;

  // FIXME: mock repository, not service under test
  @SpyBean private TimelineSplashConfigService configService;
  @MockBean private TimelineSplashConfigRepository repository;

  @Before
  public void init() {
    config = new TimelineSplashConfig();
    config.setId(CONFIG_ID);
    config.setBrand(BRAND);

    doReturn(config)
        .when(configService)
        .update(any(TimelineSplashConfig.class), any(TimelineSplashConfig.class));
    doReturn(config).when(configService).save(any(TimelineSplashConfig.class));
    doReturn(Optional.of(config)).when(configService).findOne(any(String.class));
    doReturn(Optional.of(config)).when(repository).findOneByBrand(BRAND);
  }

  @Test
  public void testCreateConfig() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/timeline/splash-config")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(config)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetConfigForBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/timeline/splash-config/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateConfig() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/timeline/splash-config/" + CONFIG_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(config)))
        .andExpect(status().is2xxSuccessful());
  }
}
