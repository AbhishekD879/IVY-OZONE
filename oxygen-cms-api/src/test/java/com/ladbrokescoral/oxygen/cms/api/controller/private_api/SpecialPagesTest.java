package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.EuroLoyal;
import com.ladbrokescoral.oxygen.cms.api.entity.TierInfo;
import com.ladbrokescoral.oxygen.cms.api.repository.SpecialPagesRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SpecialPagesService;
import com.ladbrokescoral.oxygen.cms.api.service.bpp.specialPages.SpecialPageDTO;
import com.ladbrokescoral.oxygen.cms.api.service.bpp.specialPages.SpecialPagesMaintenance;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      SpecialPages.class,
      SpecialPagesRepository.class,
      SpecialPagesService.class,
      SpecialPagesMaintenance.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class SpecialPagesTest extends AbstractControllerTest {

  private EuroLoyal euroLoyal;

  @MockBean SpecialPagesRepository specialPagesRepository;
  @MockBean SpecialPagesMaintenance specialPagesMaintenance;

  @Before
  public void init() {
    euroLoyal = createEuroLoyal();

    given(specialPagesRepository.save(any(EuroLoyal.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(specialPagesRepository.findByPageName(anyString())).willReturn(Optional.of(euroLoyal));
    given(specialPagesRepository.findById(anyString())).willReturn(Optional.of(euroLoyal));
    doNothing().when(specialPagesMaintenance).saveOrUpdateSpecialPage(any(SpecialPageDTO.class));
  }

  @Test
  public void testToCreateSpecialPage() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/special-pages/EuroLoyal")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(euroLoyal)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testToCreateFanzoneException() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/special-pages/EuroLoyal1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(euroLoyal)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToReadSpecialPage() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/special-pages/EuroLoyal")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateSpecialPage() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/special-pages/EuroLoyal")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(euroLoyal)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateException() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/special-pages/EuroLoyal1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(euroLoyal)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToDeleteSpecialPage() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/special-pages/EuroLoyal")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static EuroLoyal createEuroLoyal() {
    EuroLoyal entity = new EuroLoyal();
    entity.setId("60210e530aa8af135ab0f5bf");
    entity.setPageName("EuroLoyal");
    entity.setStartDate(Instant.now());
    entity.setEndDate(Instant.now().plus(Duration.ofDays(2)));

    List<TierInfo> tierInfoList = new ArrayList<TierInfo>();
    TierInfo tierInfo = new TierInfo();
    tierInfo.setTierName("Tier1");
    tierInfo.setOfferIdSeq(new ArrayList<String>(Arrays.asList("1", "2", "3")));
    tierInfo.setFreeBetPositionSequence(new ArrayList<Integer>(Arrays.asList(100, 101, 102)));
    tierInfoList.add(tierInfo);
    entity.setTierInfo(tierInfoList);

    entity.setHowItWorks("How it Works!");
    entity.setTermsAndConditions("Terms and Conditions");
    entity.setFullTermsURI("Full Terms!");
    return entity;
  }
}
