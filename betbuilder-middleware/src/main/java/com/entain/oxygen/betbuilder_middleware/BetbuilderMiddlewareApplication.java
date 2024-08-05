package com.entain.oxygen.betbuilder_middleware;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.thymeleaf.ThymeleafAutoConfiguration;
import org.springframework.boot.autoconfigure.web.servlet.MultipartAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication(
    exclude = {MultipartAutoConfiguration.class, ThymeleafAutoConfiguration.class})
@EnableScheduling
@ComponentScan({"com.entain.oxygen.betbuilder_middleware", "com.ladbrokescoral.lib.*"})
@OpenAPIDefinition(
    info =
        @Info(
            title = "Bet Builder Middleware",
            version = "1.0",
            description = "Bet Build Middleware APIs for all sports v1.0"))
public class BetbuilderMiddlewareApplication {
  public static void main(String[] args) {
    SpringApplication.run(BetbuilderMiddlewareApplication.class, args);
  }
}
