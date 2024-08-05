package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.LottoConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.entity.LottoConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.LottoConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.LottoConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {LottoConfigApi.class, LottoConfigService.class, ModelMapper.class})
@RunWith(SpringRunner.class)
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
@MockBean(BrandService.class)
public class LottoConfigApiTest extends AbstractControllerTest {

  @MockBean LottoConfigRepository repository;
  LottoConfig entity;
  LottoConfigDTO dto;
  ModelMapper mapper = new ModelMapper();

  @Before
  public void init() {
    dto = createDto();
    entity = mapper.map(dto, LottoConfig.class);
    entity.setId("1212212121121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
  }

  @Test
  public void testFindByBrand() throws Exception {

    List<LottoConfig> lottoConfigs = new ArrayList<>();
    lottoConfigs.add(entity);
    when(repository.findByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(lottoConfigs);
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/cms/api/bma/lotto-config"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testFindByBrandFails_NoRecordsFound() throws Exception {

    when(repository.findByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.EMPTY_LIST);
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/cms/api/bma/lotto-config"))
        .andExpect(status().is4xxClientError());
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
    lottoConfigDTO.setId("1");
    lottoConfigDTO.setMaxPayOut(78.78);
    return lottoConfigDTO;
  }
}
