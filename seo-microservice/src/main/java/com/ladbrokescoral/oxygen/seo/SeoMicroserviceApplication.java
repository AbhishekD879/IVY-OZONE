package com.ladbrokescoral.oxygen.seo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jmx.JmxAutoConfiguration;
import org.springframework.boot.autoconfigure.web.servlet.MultipartAutoConfiguration;
import reactor.tools.agent.ReactorDebugAgent;

@SpringBootApplication(
    exclude = {
      MultipartAutoConfiguration.class,
      JmxAutoConfiguration.class,
    })
public class SeoMicroserviceApplication {

  public static void main(String[] args) {
    // debug hook to get more error details
    ReactorDebugAgent.init();
    SpringApplication.run(SeoMicroserviceApplication.class, args);
  }
}
