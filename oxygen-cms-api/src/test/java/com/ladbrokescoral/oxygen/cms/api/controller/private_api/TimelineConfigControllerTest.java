package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Config;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineConfigService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      TimelineConfigController.class,
      TimelineConfigService.class,
      TimelineConfigRepository.class
    })
@MockBean({KafkaTemplate.class, TimelineConfigService.class})
@AutoConfigureMockMvc(addFilters = false)
public class TimelineConfigControllerTest extends AbstractControllerTest {

  public static final String CONFIG_ID = "98789987";
  public static final String BRAND = "ladbrokes";

  private Config config;

  // FIXME: mock repository, not service under test
  @SpyBean private TimelineConfigService configService;
  @MockBean private TimelineConfigRepository repository;

  @Before
  public void init() {
    config = new Config();
    config.setId(CONFIG_ID);
    config.setBrand(BRAND);
    config.setPageUrls("/sample");
    config.setCreatedBy("Test");

    doReturn(config).when(configService).update(any(Config.class), any(Config.class));
    doReturn(config).when(configService).save(any(Config.class));
    doReturn(config).when(configService).prepareModelBeforeSave(any(Config.class));
    doReturn(Optional.of(config)).when(configService).findOne(any(String.class));
    doReturn(Optional.of(config)).when(repository).findOneByBrand(BRAND);
  }

  @Test
  public void testCreateConfig() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/timeline/system-config")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(config)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetConfigForBrand() throws Exception {
    Mockito.when(configService.findOneByBrand(BRAND)).thenReturn(config);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/timeline/system-config/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateConfig() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/timeline/system-config/" + CONFIG_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(config)))
        .andExpect(status().is2xxSuccessful());
  }
}
