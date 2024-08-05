package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import java.util.Optional;
import org.springframework.http.HttpHeaders;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

public interface FreeRideService {

  String SECRET = "SECRET";

  String USER_NAME = "USER_NAME";

  default String getUserName() {
    return Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
        .filter(Authentication::isAuthenticated)
        .map(Authentication::getPrincipal)
        .map(User.class::cast)
        .map(User::getUsername)
        .orElse("");
  }

  default void addHeaderFields(
      HttpHeaders headers, String brand, String bmaKeyValue, String ladsKeyValue) {
    headers.set(SECRET, Brand.BMA.equalsIgnoreCase(brand) ? bmaKeyValue : ladsKeyValue);
    headers.set(USER_NAME, getUserName());
  }
}
