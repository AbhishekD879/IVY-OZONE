package com.ladbrokescoral.oxygen.cms.configuration;

import static org.junit.Assert.assertNotNull;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {SiteServerApiConfiguration.class})
class SiteServerApiConfigurationTest {
  @Autowired private SiteServerApiConfiguration siteServerApiConfiguration;

  @Test
  void testSiteServ() {
    siteServerApiConfiguration.siteServerAPI("https://ss-tst2.coral.co.uk/");
    ReflectionTestUtils.setField(siteServerApiConfiguration, "isPriceBoostEnabled", true);
    SiteServerApi siteServerAPI =
        siteServerApiConfiguration.siteServerAPI("https://ss-tst2.coral.co.uk/");
    assertNotNull(siteServerAPI);
  }
}
