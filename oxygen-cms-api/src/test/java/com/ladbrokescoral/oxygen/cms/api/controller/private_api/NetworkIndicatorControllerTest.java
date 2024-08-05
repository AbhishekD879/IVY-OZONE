package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.NetworkIndicatorConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.NetworkIndicatorRepository;
import com.ladbrokescoral.oxygen.cms.api.service.NetworkIndicatorService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {NetworkIndicatorController.class, NetworkIndicatorService.class})
@AutoConfigureMockMvc(addFilters = false)
public class NetworkIndicatorControllerTest extends AbstractControllerTest {
  @MockBean private NetworkIndicatorRepository networkIndicatorRepository;
  @SpyBean private NetworkIndicatorService networkIndicatorService;

  @Before
  public void init() {
    NetworkIndicatorConfig entity = getEntity();
    doReturn(entity)
        .when(networkIndicatorService)
        .update(any(NetworkIndicatorConfig.class), any(NetworkIndicatorConfig.class));
    doReturn(entity).when(networkIndicatorService).save(any(NetworkIndicatorConfig.class));
    doReturn(Optional.of(entity)).when(networkIndicatorRepository).findOneByBrand("ladbrokes");
    given(networkIndicatorRepository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(networkIndicatorRepository.save(any(NetworkIndicatorConfig.class)))
        .will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testSaveEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/networkIndicator")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/networkIndicator/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/networkIndicator/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(getEntity())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/networkIndicator/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private NetworkIndicatorConfig getEntity() {
    NetworkIndicatorConfig NetworkConnectionIndicator = new NetworkIndicatorConfig();
    NetworkConnectionIndicator.setId("62d9591cc6f0e44f03603941");
    NetworkConnectionIndicator.setImageURL(
        "https: //scmedia.itsfogo.com/$-$/8abaa65e01f24df587aadff849e25915.jpg");
    NetworkConnectionIndicator.setNetworkIndicatorEnabled(true);
    NetworkConnectionIndicator.setPollingInterval(200);
    NetworkConnectionIndicator.setSlowTimeout(10);
    NetworkConnectionIndicator.setThresholdTime(300);
    return NetworkConnectionIndicator;
  }
}
