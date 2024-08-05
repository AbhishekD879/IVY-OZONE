package com.ladbrokescoral.oxygen.cms.configuration;

import static com.ladbrokescoral.oxygen.cms.api.constants.ConfigConstant.CS_POLICY;

import com.ladbrokescoral.oxygen.cms.api.service.PublicApiTokenFilter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpStatus;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.authentication.HttpStatusEntryPoint;
import org.springframework.web.filter.CorsFilter;

@Profile({"!UNIT", "SECURITY"})
@Configuration
@EnableWebSecurity
@Order(1)
@SuppressWarnings({"java:S1874", "java:S4502"})
public class SecuredPublicApiSecurityConfiguration extends WebSecurityConfigurerAdapter {

  @Value("${public.api.token}")
  private String expectedToken;

  @Value("${secured.public.api.path}")
  private String securedPublicApiPath;

  @Override
  protected void configure(HttpSecurity http) throws Exception {

    http.headers().contentSecurityPolicy(CS_POLICY);
    http.antMatcher(securedPublicApiPath + "/**")
        .addFilterAfter(new PublicApiTokenFilter(expectedToken), CorsFilter.class)
        .authorizeRequests()
        // secure all endpoints
        .anyRequest()
        .authenticated()
        .and()
        // always use 401 instead of 403.
        .exceptionHandling()
        .authenticationEntryPoint(new HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED))
        .and()
        // not to hold session information for users, as this is uneccesary in an API
        .sessionManagement()
        .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
        .and()
        .cors()
        .and()
        .csrf()
        .disable();
  }
}
