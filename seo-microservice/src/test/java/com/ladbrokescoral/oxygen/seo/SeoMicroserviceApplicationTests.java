package com.ladbrokescoral.oxygen.seo;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class SeoMicroserviceApplicationTests {

  @Test
  void contextLoads() {
    SeoMicroserviceApplication.main(new String[] {});
    Assertions.assertNotNull(SeoMicroserviceApplication.class);
  }
}
