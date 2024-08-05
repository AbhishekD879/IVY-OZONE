package com.ladbrokescoral.oxygen.cms.configuration;

import static com.ladbrokescoral.oxygen.cms.api.constants.ConfigConstant.CS_POLICY;

import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.JwtAuthenticationFilter;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.authentication.HttpStatusEntryPoint;
import org.springframework.web.filter.CorsFilter;

@Profile({"!UNIT", "SECURITY"})
@Configuration
@EnableWebSecurity
@SuppressWarnings("java:S1874")
public class SecurityConfig {

  // FXIME: rework global config properties usage. remove duplicates in code.
  public static final String SECURED_PUBLIC_API_PATH = "/cms/api/secured";
  public static final String PRIVATE_API_PATH = "/v1/api";
  public static final String PUBLIC_API_PATH = "/cms/api";

  @Bean
  public PasswordEncoder passwordEncoder() {
    // FIXME: SEC: don't use BCryptPasswordEncoder directly
    // use PasswordEncoderFactories and "{bcrypt}encodedPassword"
    return new BCryptPasswordEncoder();
  }

  @Configuration
  @Order(2)
  public static class PrivateApiSecurityConfiguration extends WebSecurityConfigurerAdapter {

    @Autowired private AuthenticationService authenticationService;
    @Autowired private UserService userService;

    @Override
    protected void configure(HttpSecurity http) throws Exception {

      http.headers().contentSecurityPolicy(CS_POLICY);

      http.antMatcher(PRIVATE_API_PATH + "/**")
          .addFilterAfter(
              new JwtAuthenticationFilter(authenticationService, userService), CorsFilter.class)
          .authorizeRequests()
          // allow some private api
          .antMatchers(HttpMethod.GET, PRIVATE_API_PATH + "/timeline/sse")
          .permitAll()
          .antMatchers(HttpMethod.POST, PRIVATE_API_PATH + "/login", PRIVATE_API_PATH + "/token")
          .permitAll()
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

  /** Allow Actuator endpoints for non-prod enviroments */
  @Profile({"PRD0", "TST0", "HLV0", "HLV1", "UNIT"})
  @Configuration
  @Order(3)
  public static class PublicSecurityConfiguration extends WebSecurityConfigurerAdapter {

    @Value("${management.endpoints.web.base-path}")
    private String actuatorPath;

    @Value("${management.endpoints.web.path-mapping.health}")
    private String healthPath;

    @Value("${management.endpoints.web.path-mapping.info}")
    private String infoPath;

    @Override
    protected void configure(HttpSecurity http) throws Exception {

      http.headers().contentSecurityPolicy(CS_POLICY);

      http.authorizeRequests()
          // allow health / info
          .antMatchers(healthPath, infoPath, actuatorPath + healthPath, actuatorPath + infoPath)
          .permitAll()
          // allow all public api
          .antMatchers(PUBLIC_API_PATH + "/**")
          .permitAll()
          // secure all endpoints
          .anyRequest()
          .authenticated()
          .and()
          // not to hold session information for users, as this is uneccesary in an API
          .sessionManagement()
          .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
          .and()
          .httpBasic()
          .and()
          .cors()
          .and()
          .csrf()
          .disable();
    }
  }
}
