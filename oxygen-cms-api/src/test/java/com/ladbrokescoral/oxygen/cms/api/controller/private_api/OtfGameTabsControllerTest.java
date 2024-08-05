package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.OtfGameTabs;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.OtfGameTabsRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.OtfGameTabsService;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {BrandService.class, OtfGameTabsController.class, OtfGameTabsService.class})
@AutoConfigureMockMvc(addFilters = false)
class OtfGameTabsControllerTest extends AbstractControllerTest {

  @MockBean OtfGameTabsRepository otfGameTabsRepository;
  @MockBean BrandService brandService;
  @MockBean BrandRepository brandRepository;

  private OtfGameTabs entity;
  public static final String API_BASE_URL = "/v1/api/otf-tab-config";
  public static final String TABS_ID = "1";
  public static final String BRAND = "ladbrokes";

  @BeforeEach
  public void setUp() throws IOException {
    entity = createGameTabs();
    given(otfGameTabsRepository.save(any(OtfGameTabs.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(entity)).when(otfGameTabsRepository).findById(any(String.class));
  }

  @Test
  void createOtfGameTabsTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateOtfGameTabsTest() throws Exception {
    OtfGameTabs updateEntity = createGameTabs();
    updateEntity.setPreviousTabLabel("Updated Previous");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + TABS_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void findByBrandTest() throws Exception {
    List<OtfGameTabs> OtfGameTabsList = new ArrayList<>();
    OtfGameTabsList.add(entity);
    when(otfGameTabsRepository.findByBrand(any())).thenReturn(OtfGameTabsList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testFindByBrandWhenOtfGameTabsNotCreated() throws Exception {
    when(otfGameTabsRepository.findByBrand(any())).thenReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(new OtfGameTabs())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void deleteOtfGameTabsTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + TABS_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  private OtfGameTabs createGameTabs() {
    OtfGameTabs otfGameTabs = new OtfGameTabs();
    otfGameTabs.setBrand(BRAND);
    otfGameTabs.setCurrentTabLabel("Current");
    otfGameTabs.setPreviousTabLabel("Previous Results");
    return otfGameTabs;
  }
}
