package com.ladbrokescoral.oxygen.notification.configs;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

  @Value("${swagger.basicAuth.user}")
  private String user;

  @Value("${swagger.basicAuth.pass}")
  private String password;

  @Value("${spring.profiles.active}")
  private String activeProfile;

  @Bean
  public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(10);
  }

  @Override
  protected void configure(HttpSecurity http) throws Exception {

    HttpSecurity httpSecurity = http.sessionManagement().and().csrf().disable();
    /*
     * make sure
     * spring.resources.add-mappings=false
     * is set for all ENVs except DEV
     */
    if (activeProfile.contains("DEV")) {
      httpSecurity
          .authorizeRequests()
          .antMatchers("/swagger.yaml")
          .authenticated()
          .antMatchers("/definitions/**")
          .authenticated()
          .antMatchers("/index.html")
          .authenticated()
          .and()
          .httpBasic()
          .and()
          .headers()
          .contentSecurityPolicy("script-src 'self'");
    } else {
      httpSecurity.authorizeRequests().anyRequest().permitAll();
    }
  }

  @Override
  public void configure(AuthenticationManagerBuilder authenticationManager) throws Exception {
    authenticationManager
        .inMemoryAuthentication()
        .withUser(user)
        .password(passwordEncoder().encode(password))
        .roles("SWAGGER")
        .authorities("SWAGGER");
  }
}
