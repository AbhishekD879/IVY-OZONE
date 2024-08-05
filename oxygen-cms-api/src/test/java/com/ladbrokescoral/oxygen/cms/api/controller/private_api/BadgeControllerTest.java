package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Badge;
import com.ladbrokescoral.oxygen.cms.api.repository.BadgeRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BadgeService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
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

@WebMvcTest(value = {BadgeController.class, BadgeService.class})
@AutoConfigureMockMvc(addFilters = false)
class BadgeControllerTest extends AbstractControllerTest {

  @MockBean BadgeRepository badgeRepository;
  @MockBean BrandService brandService;
  @MockBean BrandRepository brandRepository;

  private Badge entity;
  private Badge updateBadgeEntity;

  public static final String API_BASE_URL = "/v1/api/badge";
  public static final String BADGE_ID = "1";
  public static final String BRAND = "ladbrokes";

  @BeforeEach
  public void setUp() throws IOException {
    entity =
        TestUtil.deserializeWithJackson("controller/private_api/createBadge.json", Badge.class);
    updateBadgeEntity =
        TestUtil.deserializeWithJackson("controller/private_api/updateBadge.json", Badge.class);
    given(badgeRepository.save(any(Badge.class))).will(AdditionalAnswers.returnsFirstArg());
    doReturn(Optional.of(entity)).when(badgeRepository).findById(any(String.class));
  }

  @Test
  void createBadgeTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(API_BASE_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void updateBadgeTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(API_BASE_URL + "/" + BADGE_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateBadgeEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void findByBrandTest() throws Exception {
    List<Badge> badgeList = new ArrayList<>();
    badgeList.add(entity);
    when(badgeRepository.findByBrand(any())).thenReturn(badgeList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void testFindByBrandWhenBadgeNotCreated() throws Exception {
    when(badgeRepository.findByBrand(any())).thenReturn(new ArrayList<>());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(API_BASE_URL + "/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(new Badge())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  void deleteBadgeTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete(API_BASE_URL + "/" + BADGE_ID)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }
}
