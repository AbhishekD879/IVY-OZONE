package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.LottoBannerConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.dto.LottoConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LottoConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.LottoConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.LottoConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.*;
import java.util.*;
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

@WebMvcTest(value = {LottoConfigs.class, LottoConfigService.class, ModelMapper.class})
@RunWith(SpringRunner.class)
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
@MockBean(BrandService.class)
public class LottoConfigsTest extends AbstractControllerTest {
  @MockBean LottoConfigRepository repository;
  LottoConfig entity;
  LottoConfigDTO dto;
  ModelMapper mapper = new ModelMapper();

  @Before
  public void init() {
    dto = createDto();
    entity = mapper.map(dto, LottoConfig.class);
    entity.setId("1");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(repository.save(any())).thenReturn(entity);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
  }

  @Test
  public void testCreateLottoConfig() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/lotto-config")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateLottoConfigWhenIdExists() throws Exception {
    String id = "1110212913455091313";
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/lotto-config/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateLottoConfigWhenIdNotExists() throws Exception {
    String id = "118000004558668682";
    when(repository.findById(id)).thenReturn(Optional.empty());
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/lotto-config/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadById() throws Exception {
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/v1/api/lotto-config/233"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrderMenu() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/lotto-config/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateLottoBannerConfigSuccess() throws Exception {

    List<LottoConfig> lottoConfigs = new ArrayList<>();
    lottoConfigs.add(entity);

    LottoBannerConfigDTO lottoBannerConfigDTO =
        new LottoBannerConfigDTO(
            "globalbannerlinkurl", "banner text", lottoConfigs, Arrays.asList("1"), 2);

    when(repository.findByBrand("bma")).thenReturn(lottoConfigs);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/lotto-config/banner-link/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(lottoBannerConfigDTO)))
        .andExpect(status().is2xxSuccessful());
    verify(repository, times(1)).saveAll(any());
  }

  @Test
  public void testUpdateLottoBannerFails_WhenIdsofDiffSizes() throws Exception {

    List<LottoConfig> lottoConfigs = new ArrayList<>();
    lottoConfigs.add(entity);

    LottoBannerConfigDTO lottoBannerConfigDTO =
        new LottoBannerConfigDTO(
            "globalbannerlinkurl", "banner text", lottoConfigs, Arrays.asList("1", "2"), 2);

    when(repository.findByBrand("bma")).thenReturn(lottoConfigs);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/lotto-config/banner-link/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(lottoBannerConfigDTO)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateLottoBannerFails_WhenIdsNotMatch()
      throws Exception { // input ids and existing ids could not match

    List<LottoConfig> lottoConfigs = new ArrayList<>();
    lottoConfigs.add(entity);

    LottoBannerConfigDTO lottoBannerConfigDTO =
        new LottoBannerConfigDTO(
            "globalbannerlinkurl", "banner text", lottoConfigs, Arrays.asList("2"), 2);

    when(repository.findByBrand("bma")).thenReturn(lottoConfigs);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/lotto-config/banner-link/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(lottoBannerConfigDTO)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateLottoBannerFails_WhenNoRecordFound() throws Exception {

    List<LottoConfig> lottoConfigs = new ArrayList<>();
    lottoConfigs.add(entity);

    LottoBannerConfigDTO lottoBannerConfigDTO =
        new LottoBannerConfigDTO(
            "globalbannerlinkurl", "banner text", lottoConfigs, Arrays.asList("1"), 2);

    when(repository.findByBrand("bma")).thenReturn(null);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/lotto-config/banner-link/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(lottoBannerConfigDTO)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testFindByBrand() throws Exception {

    List<LottoConfig> lottoConfigs = new ArrayList<>();
    lottoConfigs.add(entity);
    when(repository.findByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(lottoConfigs);
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/v1/api/lotto-config/brand/bma"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testFindByBrandEmpty() throws Exception {

    List<LottoConfig> lottoConfigs = new ArrayList<>();

    when(repository.findByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(lottoConfigs);
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/v1/api/lotto-config/brand/bma"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void DeleteById() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.of(entity), Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/lotto-config/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static LottoConfigDTO createDto() {
    LottoConfigDTO lottoConfigDTO = new LottoConfigDTO();
    lottoConfigDTO.setBrand("bma");
    lottoConfigDTO.setSsMappingId("1132333");
    lottoConfigDTO.setLabel("label");
    lottoConfigDTO.setInfoMessage("info message");
    lottoConfigDTO.setNextLink("nextLinkUrl");
    lottoConfigDTO.setSortOrder(1.00);
    lottoConfigDTO.setBannerLink("bannerLinkUrl");
    lottoConfigDTO.setSvgId("Lotto config");
    lottoConfigDTO.setId("1");
    lottoConfigDTO.setMaxPayOut(78.78);
    return lottoConfigDTO;
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
}
