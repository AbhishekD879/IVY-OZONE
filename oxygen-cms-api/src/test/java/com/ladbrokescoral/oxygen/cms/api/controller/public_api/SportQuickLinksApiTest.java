package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyObject;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Users;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportQuickLinkExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.SportModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportQuickLinkPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StaticBlockPublicService;
import java.util.Arrays;
import java.util.Optional;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Users.class,
      AuthenticationService.class,
      SportQuickLinksApi.class,
      SportQuickLinkPublicService.class,
      SportQuickLinksApi.class,
      SportQuickLinkExtendedRepository.class,
      SportModuleService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class SportQuickLinksApiTest {

  @MockBean private SportQuickLinkExtendedRepository extendedRepository;
  @MockBean private UserService userServiceMock;
  @MockBean StaticBlockPublicService staticBlockService;
  @MockBean SportModuleService sportModuleService;
  @Autowired private MockMvc mockMvc;
  @MockBean SegmentRepository segmentRepository;

  @Before
  public void init() {
    given(extendedRepository.findAll(anyString())).willReturn(Arrays.asList(new SportQuickLink()));
    given(extendedRepository.findAll(anyString(), anyInt()))
        .willReturn(Arrays.asList(new SportQuickLink()));
    given(sportModuleService.findOne(anyString(), anyObject(), anyString(), anyObject()))
        .willReturn(Optional.empty());
  }

  @Test
  public void testGetAllByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("destination")));
  }

  @Test
  public void testGetAllByBrandDisabledGlobally() throws Exception {
    SportModule sportModule = new SportModule();
    sportModule.setDisabled(true);
    given(sportModuleService.findOne(anyString(), anyObject(), anyString(), anyObject()))
        .willReturn(Optional.of(sportModule));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("[]")));
  }

  @Test
  public void testGetAllByBrandEnabledGlobally() throws Exception {
    SportModule sportModule = new SportModule();
    sportModule.setDisabled(false);
    given(sportModuleService.findOne(anyString(), anyObject(), anyString(), anyObject()))
        .willReturn(Optional.of(sportModule));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("destination")));
  }

  @Test
  public void testGetAllByBrandEnabledGloballyForUniversal() throws Exception {
    SportModule sportModule = new SportModule();
    sportModule.setDisabled(false);
    given(sportModuleService.findOne(anyString(), anyObject(), anyString(), anyObject()))
        .willReturn(Optional.of(sportModule));
    given(segmentRepository.findByBrand("bma"))
        .willReturn(
            Arrays.asList(Segment.builder().segmentName(SegmentConstants.UNIVERSAL).build()));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("destination")));
  }

  @Test
  public void testGetAllByBrandAndSportId() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/sport-quick-link/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetAllByBrandAndSportDisabledGlobally() throws Exception {
    SportModule sportModule = new SportModule();
    sportModule.setDisabled(true);
    given(sportModuleService.findOne(anyString(), anyObject(), anyString(), anyObject()))
        .willReturn(Optional.of(sportModule));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/sport-quick-link/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("[]")));
  }

  @Test
  public void testGetAllByBrandAndSportEnabledGlobally() throws Exception {
    SportModule sportModule = new SportModule();
    sportModule.setDisabled(false);
    given(sportModuleService.findOne(anyString(), anyObject(), anyString(), anyObject()))
        .willReturn(Optional.of(sportModule));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/sport-quick-link/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(content().string(Matchers.containsString("destination")));
  }
}
