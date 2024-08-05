package com.gvc.oxygen.betreceipts.config;

import io.undertow.server.HttpHandler;
import io.undertow.server.handlers.DisallowedMethodsHandler;
import io.undertow.util.HttpString;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.web.embedded.undertow.UndertowDeploymentInfoCustomizer;
import org.springframework.boot.web.embedded.undertow.UndertowServletWebServerFactory;
import org.springframework.boot.web.server.WebServerFactoryCustomizer;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class CustomContainer
    implements WebServerFactoryCustomizer<UndertowServletWebServerFactory> {

  @Override
  public void customize(UndertowServletWebServerFactory factory) {
    if (factory.getClass().isAssignableFrom(UndertowServletWebServerFactory.class)) {
      factory.addDeploymentInfoCustomizers(new ContextSecurityCustomizer());
    }
  }

  private static class ContextSecurityCustomizer implements UndertowDeploymentInfoCustomizer {

    @Override
    public void customize(io.undertow.servlet.api.DeploymentInfo deploymentInfo) {
      log.info("undertow customized");
      deploymentInfo.addInitialHandlerChainWrapper(
          (HttpHandler handler) -> {
            HttpString[] disallowedHttpMethods = {
              HttpString.tryFromString("TRACE"), HttpString.tryFromString("TRACK")
            };
            return new DisallowedMethodsHandler(handler, disallowedHttpMethods);
          });
    }
  }
}
