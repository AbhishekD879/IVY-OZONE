package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.RssRewardDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.RssReward;
import com.ladbrokescoral.oxygen.cms.api.mapping.RssRewardMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.RssRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.RssRewardService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.RssRewardPublicService;
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
      RssRewardPublicApi.class,
      RssRewardService.class,
      RssRewardPublicService.class,
      ModelMapper.class,
      RssRewardMapper.class,
      RssReward.class,
      RssRepository.class
    })
@Import(ModelMapperConfig.class)
@MockBean(BrandService.class)
@AutoConfigureMockMvc(addFilters = false)
public class RssRewardPublicApiTest extends AbstractControllerTest {
  RssRewardDto rssRewardDto;
  @Mock RssRewardService rssRewardService;
  @Mock RssRewardPublicService RssRewardPublicService;
  ModelMapper mapper = new ModelMapper();
  RssReward entity;
  @MockBean RssRepository repository;

  @Before
  public void init() {
    rssRewardDto = getRssRewardDto();
    RssRewardMapper.INSTANCE.toEntity(rssRewardDto);
    entity = mapper.map(rssRewardDto, RssReward.class);
    entity.setId("1");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(repository.save(any())).thenReturn(entity);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    when(repository.findOneByBrand(any())).thenReturn(Optional.of(entity));
  }

  @Test
  public void testUpdate() throws Exception {
    when(repository.findOneByBrand(anyString())).thenReturn(Optional.of(getRssReward()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/ce/rssrewards")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRssRewardDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCommunicationType() throws Exception {
    when(repository.findOneByBrand(anyString()))
        .thenReturn(Optional.of(getEmptyCommunicationType()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/ce/rssrewards")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRssRewardDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testemptyUpdate() throws Exception {
    when(repository.findOneByBrand(anyString())).thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/ce/rssrewards")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRssRewardDto())))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testNonActive() throws Exception {
    when(repository.findOneByBrand(anyString()))
        .thenReturn(Optional.of(getRssReward().setEnabled(false)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/ce/rssrewards")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getRssRewardDtoNonEnabled())))
        .andExpect(status().is4xxClientError());
  }

  private static RssRewardDto getRssRewardDtoNonEnabled() {
    RssRewardDto getRssReward = new RssRewardDto();
    getRssReward.setEnabled(false);
    getRssReward.setBrand("1");
    getRssReward.setCoins(20);
    getRssReward.setProduct("Notes");

    getRssReward.setSitecoreTemplateId("entry point icon 3");
    getRssReward.setSource("System");
    getRssReward.setSubSource("System");
    return getRssReward;
  }

  private static RssRewardDto getRssRewardDto() {
    RssRewardDto getRssReward = new RssRewardDto();
    getRssReward.setEnabled(true);
    getRssReward.setBrand("1");
    getRssReward.setCoins(20);
    getRssReward.setProduct("Notes");

    getRssReward.setSitecoreTemplateId("entry point icon 2");
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

    getRssReward.setSitecoreTemplateId("entry point icon 1");
    getRssReward.setSource("System");
    getRssReward.setSubSource("System");
    return getRssReward;
  }

  private static RssReward getEmptyCommunicationType() {
    RssReward getRssReward = new RssReward();
    getRssReward.setEnabled(true);
    getRssReward.setBrand("1");
    getRssReward.setCoins(20);
    getRssReward.setProduct("Notes");
    getRssReward.setSource("System");
    getRssReward.setSubSource("System");
    return getRssReward;
  }
}
