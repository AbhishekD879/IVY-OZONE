package com.ladbrokescoral.oxygen.cms.api.controller;

import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.configuration.AppAuditor;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;

class AppAuditorTest {

  private AppAuditor appAuditor;

  @BeforeEach
  public void setUp() {
    appAuditor = new AppAuditor();
  }

  @Test
  void testGetCurrentAuditor_WithValidAuthentication() {
    Authentication authentication = Mockito.mock(Authentication.class);
    User user = new User();
    user.setId("testUserId");
    Mockito.when(authentication.isAuthenticated()).thenReturn(true);
    Mockito.when(authentication.getPrincipal()).thenReturn(user);
    SecurityContext securityContext = Mockito.mock(SecurityContext.class);
    Mockito.when(securityContext.getAuthentication()).thenReturn(authentication);
    SecurityContextHolder.setContext(securityContext);
    Assertions.assertNotNull(appAuditor.getCurrentAuditor());
  }

  @Test
  void testGetCurrentAuditor_WithNoAuthentication() {
    SecurityContextHolder.clearContext();
    Assertions.assertNotNull(appAuditor.getCurrentAuditor());
  }
}
