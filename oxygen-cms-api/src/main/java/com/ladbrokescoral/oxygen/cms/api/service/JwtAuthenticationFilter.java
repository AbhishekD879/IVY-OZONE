package com.ladbrokescoral.oxygen.cms.api.service;

import java.io.IOException;
import java.util.Optional;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.web.filter.OncePerRequestFilter;

@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

  private final AuthenticationService authenticationService;
  private final UserService userService;

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
      throws ServletException, IOException {

    try {
      Optional<String> token = retrieveToken(request);

      if (token.isPresent() && authenticationService.validateToken(token.get())) {

        String userId = authenticationService.retrieveSubject(token.get());
        UserDetails userDetails = userService.loadUserById(userId);

        UsernamePasswordAuthenticationToken authentication =
            new UsernamePasswordAuthenticationToken(
                userDetails, token.get(), userDetails.getAuthorities());

        authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
        SecurityContextHolder.getContext().setAuthentication(authentication);
      }

    } catch (Exception ex) {
      logger.error("Could not set user authentication in security context", ex);
    }

    filterChain.doFilter(request, response);
  }

  private Optional<String> retrieveToken(HttpServletRequest request) {

    // FIXME: hardcoded to fix issue with inccorect format from UI
    // added support for both:
    // * Authorization: Bearer <token>
    // * Authorization: <token>
    // Ticket BMA-57453:
    // * should be `Authorization: Bearer <token>` only
    return Optional.ofNullable(request.getHeader(HttpHeaders.AUTHORIZATION))
        // un-comment after BMA-57453 to avoid
        // `Invalid JWT token` for `Authorization: Basic`
        // .filter(h -> h.startsWith("Bearer "))
        .filter(h -> !h.startsWith("Basic ")) // remove after BMA-57453
        .map(h -> h.replace("Bearer ", ""));
  }
}
