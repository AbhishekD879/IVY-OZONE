package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Badge;
import com.ladbrokescoral.oxygen.cms.api.repository.BadgeRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BadgeService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BadgePublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({OneTwoFreeBadgeApi.class, BadgePublicService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class OneTwoFreeBadgeApiTest extends AbstractControllerTest {

  @MockBean BadgeService badgeService;
  @MockBean BadgeRepository badgeRepository;

  private List<Badge> badgeList;

  @BeforeEach
  public void setUp() throws Exception {
    Badge entity = new Badge();
    entity.setBrand("bma");
    badgeList = new ArrayList<>();
    badgeList.add(entity);
    given(badgeRepository.findByBrand(any())).willReturn(badgeList);
  }

  @Test
  void findAllByBrandTest() throws Exception {
    given(badgeService.findByBrand(any())).willReturn(badgeList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/one-two-free/badge")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
