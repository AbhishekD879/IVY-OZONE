package com.entain.oxygen.configuration;

import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.autoconfigure.endpoint.web.CorsEndpointProperties;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.context.support.AnnotationConfigContextLoader;
import org.springframework.web.reactive.config.CorsRegistry;

@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = WebFluxConfig.class, loader = AnnotationConfigContextLoader.class)
class WebFluxConfigTest {

  @MockBean private CorsEndpointProperties corsEndpointProperties;
  @Autowired private WebFluxConfig webFluxConfig;

  @Test
  void testCorsMappings() {
    CorsRegistry corsRegistry = new CorsRegistry();
    Mockito.doNothing().when(corsEndpointProperties).setAllowedOrigins(List.of("*"));
    Mockito.doNothing().when(corsEndpointProperties).setAllowedMethods(List.of("*"));
    Mockito.doNothing().when(corsEndpointProperties).setAllowedHeaders(List.of("*"));
    webFluxConfig.addCorsMappings(corsRegistry);
    Mockito.verify(corsEndpointProperties, Mockito.atLeast(1)).getAllowedOrigins();
    Mockito.verify(corsEndpointProperties, Mockito.atLeast(1)).getAllowedHeaders();
    Mockito.verify(corsEndpointProperties, Mockito.atLeast(1)).getAllowedMethods();
  }
}
