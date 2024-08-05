package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.NetworkIndicatorConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.NetworkIndicatorRepository;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {NetworkIndicatorService.class})
class NetworkIndicatorServiceTest {
  @MockBean private NetworkIndicatorRepository networkIndicatorRepository;
  @InjectMocks private NetworkIndicatorService networkIndicatorService;

  @BeforeEach
  public void setup() throws IOException, URISyntaxException {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testReadOneByBrand() {
    when(networkIndicatorRepository.findOneByBrand(Mockito.any()))
        .thenReturn(Optional.of(getEntity()));
    ResponseEntity<NetworkIndicatorConfig> networkindicatorConfig =
        networkIndicatorService.readOneByBrand(Mockito.any());
    assertEquals("62d9591cc6f0e44f03603941", networkindicatorConfig.getBody().getId());
    assertEquals(10, networkindicatorConfig.getBody().getSlowTimeout());
  }

  @Test
  void testReadOneByBrand_empty() {
    when(networkIndicatorRepository.findOneByBrand(Mockito.any())).thenReturn(Optional.empty());
    ResponseEntity<NetworkIndicatorConfig> networkindicatorConfig =
        networkIndicatorService.readOneByBrand(Mockito.any());
    assertEquals(null, networkindicatorConfig.getBody());
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
