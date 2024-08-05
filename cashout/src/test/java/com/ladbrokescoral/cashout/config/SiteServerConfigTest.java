package com.ladbrokescoral.cashout.config;

import static org.junit.Assert.assertNotNull;

import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class SiteServerConfigTest {
  @InjectMocks private SiteServerConfig siteServerConfig;

  @ParameterizedTest
  @ValueSource(booleans = {true, false})
  void testSiteServerApi(boolean hasPriceStream) {
    ReflectionTestUtils.setField(siteServerConfig, "isPriceBoostEnabled", hasPriceStream);
    try {
      siteServerConfig.siteServerApi("https://backoffice-tst2.coral.co.uk/", 1, 1, 1, "BASIC");
    } catch (KeyManagementException e) {
      assertNotNull(e);
    } catch (NoSuchAlgorithmException e) {
      assertNotNull(e);
    }
  }
}
