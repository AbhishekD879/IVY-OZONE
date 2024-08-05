package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.controller.public_api.SecretApi;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import java.io.IOException;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.web.filter.OncePerRequestFilter;

@RequiredArgsConstructor
public class PublicApiTokenFilter extends OncePerRequestFilter {

  private final String expectedToken;

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
      throws ServletException, IOException {

    String token = request.getHeader(SecretApi.REQUEST_HEADER_X_API_KEY_NAME);

    if (expectedToken.equals(token)) {

      // FIXME: need to create `System User` and use here as a Principal
      // it's ok to rework this filter and such approch as secured public api
      UserDetails user = User.builder().id("system").build();

      UsernamePasswordAuthenticationToken authentication =
          new UsernamePasswordAuthenticationToken(user, token, user.getAuthorities());

      authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
      SecurityContextHolder.getContext().setAuthentication(authentication);
    }

    filterChain.doFilter(request, response);
  }
}
