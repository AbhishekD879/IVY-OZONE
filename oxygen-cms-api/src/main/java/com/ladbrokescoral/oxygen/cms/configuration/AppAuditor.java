package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.entity.User;
import java.util.Optional;
import org.springframework.data.domain.AuditorAware;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
public class AppAuditor implements AuditorAware<String> {

  @Override
  public Optional<String> getCurrentAuditor() {

    Authentication authentication = SecurityContextHolder.getContext().getAuthentication();

    // FIXME: field @CreatedBy in #AbstractEntity should be #User not #String
    return Optional.ofNullable(authentication)
        .filter(Authentication::isAuthenticated)
        .map(Authentication::getPrincipal)
        .filter(User.class::isInstance)
        .map(User.class::cast)
        .map(User::getId);
  }
}
