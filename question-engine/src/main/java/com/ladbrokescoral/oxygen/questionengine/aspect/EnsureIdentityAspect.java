package com.ladbrokescoral.oxygen.questionengine.aspect;

import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import com.ladbrokescoral.oxygen.questionengine.exception.UnauthorizedException;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

import javax.servlet.http.HttpServletRequest;

@Component
@Aspect
@RequiredArgsConstructor
@ConditionalOnProperty(value = "application.security.disabled", havingValue = "false")
public class EnsureIdentityAspect {
  private static final String SECRET_HEADER_NAME = "QE-API-KEY";

  private final ApplicationProperties properties;
  private final HttpServletRequest request;

  @Before("within(com.ladbrokescoral.oxygen.questionengine.internal.*)")
  public void ensureIdentity(JoinPoint joinPoint) {
    if (!StringUtils.equals(request.getHeader(SECRET_HEADER_NAME), properties.getApiKey())) {
      throw new UnauthorizedException("Someone is trying to perform unauthorized action: " + joinPoint.getSignature().getName());
    }
  }
}
