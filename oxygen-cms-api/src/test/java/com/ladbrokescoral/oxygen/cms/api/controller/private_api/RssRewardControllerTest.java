package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.RssRewardDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.RssReward;
import com.ladbrokescoral.oxygen.cms.api.repository.RssRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.RssRewardService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      RssRewardController.class,
      RssRewardService.class,
      ModelMapper.class,
      RssReward.class,
      RssRepository.class
    })
@Import(ModelMapperConfig.class)
@MockBean(BrandService.class)
@AutoConfigureMockMvc(addFilters = false)
public class RssRewardControllerTest extends AbstractControllerTest {
  RssRewardDto rssRewardDto;
  @Mock RssRewardService rssRewardService;
  ModelMapper mapper = new ModelMapper();
  RssReward entity;
  @MockBean RssRepository repository;

  @Before
  public void init() {
    rssRewardDto = getRssRewardDto();
    entity = mapper.map(rssRewardDto, RssReward.class);
    entity.setId("1");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(repository.save(any())).thenReturn(entity);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    when(repository.findOneByBrand(any())).thenReturn(Optional.of(entity));
  }

  @Test
  public void createTest() throws Exception {
    when(repository.save(any(RssReward.class))).thenReturn(entity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/rss-rewards")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRssRewardDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getById() throws Exception {
    when(repository.findOneByBrand(anyString())).thenReturn(Optional.of(getRssReward()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/rss-rewards/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdate() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/rss-rewards/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRssRewardDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/rss-rewards/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRssRewardDto())))
        .andExpect(status().is2xxSuccessful());
  }

  private static RssRewardDto getRssRewardDto() {
    RssRewardDto getRssReward = new RssRewardDto();
    getRssReward.setEnabled(true);
    getRssReward.setBrand("1");
    getRssReward.setCoins(20);
    getRssReward.setProduct("Notes");
    getRssReward.setSitecoreTemplateId("entry point icon");
    getRssReward.setSource("System");
    getRssReward.setSubSource("System");
    return getRssReward;
  }

  private static RssReward getRssReward() {
    RssReward getRssReward = new RssReward();
    getRssReward.setEnabled(true);
    getRssReward.setBrand("1");
    getRssReward.setCoins(20);
    getRssReward.setProduct("Notes");
    getRssReward.setSitecoreTemplateId("entry point icon");
    getRssReward.setSource("System");
    getRssReward.setSubSource("System");
    return getRssReward;
  }
}
