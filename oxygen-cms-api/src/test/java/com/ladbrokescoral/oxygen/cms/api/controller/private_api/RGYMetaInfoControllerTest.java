package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYMetaInfoEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYMetaInfoRepository;
import com.ladbrokescoral.oxygen.cms.api.service.RGYMetaInfoService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {RGYMetaInfoController.class, RGYMetaInfoService.class})
@AutoConfigureMockMvc(addFilters = false)
public class RGYMetaInfoControllerTest extends AbstractControllerTest {

  @MockBean private RGYMetaInfoRepository rgyMetaInfoRepository;

  @SpyBean private RGYMetaInfoService rgyMetaInfoService;

  @Before
  public void init() {
    RGYMetaInfoEntity entity = getMetaInfo();
    doReturn(Optional.of(entity))
        .when(rgyMetaInfoService)
        .update(any(RGYMetaInfoEntity.class), any(RGYMetaInfoEntity.class));

    given(rgyMetaInfoRepository.findOneByBrand(any(String.class))).willReturn(Optional.of(entity));
  }

  @Test
  public void testGetRgyMetaInfo() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/rgy-mtaInfo/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getMetaInfo())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateRgyFlag() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/rgy-mtaInfo/ladbrokes/true")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getMetaInfo())))
        .andExpect(status().is2xxSuccessful());
  }

  private RGYMetaInfoEntity getMetaInfo() {
    RGYMetaInfoEntity rgyMetaInfoEntity = new RGYMetaInfoEntity();
    rgyMetaInfoEntity.setBrand("ladbrokes");
    return rgyMetaInfoEntity;
  }
}
