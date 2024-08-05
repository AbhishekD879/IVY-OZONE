package com.entain.oxygen.configuration;

import com.entain.oxygen.bpp.BppConfigLightProps;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@TestPropertySource("classpath:bpp-light.properties")
@EnableConfigurationProperties(BppConfigLightProps.class)
class BppConfigLightPropsTest {

  @Autowired private BppConfigLightProps bppConfigLightProps;

  @Test
  void testBppLightProps() {

    Assertions.assertNotNull(bppConfigLightProps);
    Assertions.assertEquals(0, bppConfigLightProps.getRetryNumber());
    Assertions.assertEquals(2000, bppConfigLightProps.getConnectTimeout());
    Assertions.assertEquals(1000, bppConfigLightProps.getReadTimeout());
    Assertions.assertEquals(2000, bppConfigLightProps.getPoolSize());
    Assertions.assertEquals(50, bppConfigLightProps.getThreads());
    Assertions.assertEquals(false, bppConfigLightProps.isKeepAlive());
    Assertions.assertEquals(1000, bppConfigLightProps.getWriteTimeout());
    Assertions.assertEquals(0, bppConfigLightProps.getRetryTimeout());
  }
}
