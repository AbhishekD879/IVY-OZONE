package com.egalacoral.spark.timeform.configuration;

import com.egalacoral.spark.timeform.api.TimeFormAPI;
import com.egalacoral.spark.timeform.api.TimeFormService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by llegkyy on 09.08.16. */
@Configuration
public class TimeformLoginConfiguration {

  @Value("${timeform.api.login}")
  private String username;

  @Value("${timeform.api.password}")
  private String password;

  @Bean
  public TimeFormService getTimeFormService(TimeFormAPI timeFormAPI) {
    TimeFormService timeFormService = timeFormAPI.login(username, password);
    return timeFormService;
  }
}
