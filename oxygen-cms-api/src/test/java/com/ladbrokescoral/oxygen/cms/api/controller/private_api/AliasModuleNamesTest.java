package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.repository.ExtraNavigationPointRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.NavigationPointRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportQuickLinkRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AliasModuleNamesService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import java.time.Duration;
import java.time.Instant;
import java.util.Collections;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.MockBeans;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

@WebMvcTest(value = {AliasModuleNames.class, AliasModuleNamesService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBeans(value = {@MockBean(BrandService.class)})
public class AliasModuleNamesTest extends AbstractControllerTest {

  @MockBean private SportQuickLinkRepository sportQuickLinkRepository;

  @MockBean private NavigationPointRepository superButtonRepository;

  @MockBean private ExtraNavigationPointRepository specialSuperButtonRepository;

  private SportQuickLink sportQuickLink;

  private NavigationPoint superButton;

  private ExtraNavigationPoint specialSuperButton;

  @Before
  public void init() {
    this.sportQuickLink = sportQuickLink("bma");
    this.superButton = superButton("bma");
    this.specialSuperButton = specialSuperButton("bma");
  }

  @Test
  public void testGetQLAndSB() throws Exception {
    given(this.sportQuickLinkRepository.findAllByBrandAndPageTypeIn(anyString(), any()))
        .willReturn(Collections.singletonList(sportQuickLink));
    given(this.superButtonRepository.findByBrand(anyString()))
        .willReturn(Collections.singletonList(superButton));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/alias-module-names/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(
            MockMvcResultMatchers.content()
                .json(
                    "{\"QL\":[{\"id\":\"11\",\"title\":\"CRC-QL\",\"addTag\":false}],\"SB\":[{\"id\":\"12\",\"title\":\"CRC-SB\",\"addTag\":false}]}"));
  }

  @Test
  public void testGetQlAndSBAndSSB() throws Exception {
    SportQuickLink sportQuickLink = this.sportQuickLink;
    sportQuickLink.setBrand("ladbrokes");
    NavigationPoint superButton = this.superButton;
    superButton.setBrand("ladbrokes");
    ExtraNavigationPoint specialSuperButton = this.specialSuperButton;
    specialSuperButton.setBrand("ladbrokes");
    given(this.sportQuickLinkRepository.findAllByBrandAndPageTypeIn(anyString(), any()))
        .willReturn(Collections.singletonList(sportQuickLink));
    given(this.superButtonRepository.findByBrand(anyString()))
        .willReturn(Collections.singletonList(superButton));
    given(this.specialSuperButtonRepository.findByBrand(anyString()))
        .willReturn(Collections.singletonList(specialSuperButton));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/alias-module-names/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(
            MockMvcResultMatchers.content()
                .json(
                    "{\"QL\":[{\"id\":\"11\",\"title\":\"CRC-QL\",\"addTag\":false}],\"SB\":[{\"id\":\"12\",\"title\":\"CRC-SB\",\"addTag\":false},{\"id\":\"13\",\"title\":\"CRC-SSB\",\"addTag\":false}]}"));
  }

  @Test
  public void testAliasModuleNamesForValidityOutOfDate() throws Exception {
    SportQuickLink ql = sportQuickLink("ladbrokes");
    ql.setValidityPeriodEnd(Instant.now());
    NavigationPoint sb = superButton("ladbrokes");
    sb.setValidityPeriodEnd(Instant.now());
    ExtraNavigationPoint ssB = specialSuperButton("ladbrokes");
    ssB.setValidityPeriodEnd(Instant.now());
    given(this.sportQuickLinkRepository.findAllByBrandAndPageTypeIn(anyString(), any()))
        .willReturn(Collections.singletonList(ql));
    given(this.superButtonRepository.findByBrand(anyString()))
        .willReturn(Collections.singletonList(sb));
    given(this.specialSuperButtonRepository.findByBrand(anyString()))
        .willReturn(Collections.singletonList(ssB));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/alias-module-names/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.content().json("{\"QL\":[],\"SB\":[]}"));
  }

  @Test
  public void testAliasNamesWithInactive() throws Exception {
    SportQuickLink ql = sportQuickLink("ladbrokes");
    ql.setDisabled(true);
    NavigationPoint sb = superButton("ladbrokes");
    sb.setEnabled(false);
    ExtraNavigationPoint ssB = specialSuperButton("ladbrokes");
    ssB.setEnabled(false);
    given(this.sportQuickLinkRepository.findAllByBrandAndPageTypeIn(anyString(), any()))
        .willReturn(Collections.singletonList(ql));
    given(this.superButtonRepository.findByBrand(anyString()))
        .willReturn(Collections.singletonList(sb));
    given(this.specialSuperButtonRepository.findByBrand(anyString()))
        .willReturn(Collections.singletonList(ssB));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/alias-module-names/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.content().json("{\"QL\":[],\"SB\":[]}"));
  }

  private SportQuickLink sportQuickLink(String brand) {
    SportQuickLink sportQuickLink = new SportQuickLink();
    sportQuickLink.setId("11");
    sportQuickLink.setTitle("CRC-QL");
    sportQuickLink.setBrand(brand);
    sportQuickLink.setDisabled(false);
    sportQuickLink.setValidityPeriodEnd(Instant.now().plus(Duration.ofDays(1)));
    return sportQuickLink;
  }

  private NavigationPoint superButton(String brand) {
    NavigationPoint superButton = new NavigationPoint();
    superButton.setId("12");
    superButton.setTitle("CRC-SB");
    superButton.setBrand(brand);
    superButton.setValidityPeriodEnd(Instant.now().plus(Duration.ofDays(1)));
    superButton.setEnabled(true);
    return superButton;
  }

  private ExtraNavigationPoint specialSuperButton(String brand) {
    ExtraNavigationPoint specialSuperButton = new ExtraNavigationPoint();
    specialSuperButton.setId("13");
    specialSuperButton.setTitle("CRC-SSB");
    specialSuperButton.setBrand(brand);
    specialSuperButton.setEnabled(true);
    specialSuperButton.setValidityPeriodEnd(Instant.now().plus(Duration.ofDays(1)));
    return specialSuperButton;
  }
}
