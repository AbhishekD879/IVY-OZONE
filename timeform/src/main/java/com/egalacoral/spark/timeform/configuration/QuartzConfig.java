package com.egalacoral.spark.timeform.configuration;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.quartz.SchedulerFactoryBean;

@Configuration
public class QuartzConfig {

  @Autowired private ApplicationContext applicationContext;

  @Bean
  public SchedulerFactoryBean quartzScheduler() {
    SchedulerFactoryBean quartzScheduler = new SchedulerFactoryBean();
    // custom job factory of spring with DI support for @Autowired
    AutowiringSpringBeanJobFactory jobFactory = new AutowiringSpringBeanJobFactory();
    jobFactory.setApplicationContext(applicationContext);
    quartzScheduler.setJobFactory(jobFactory);
    return quartzScheduler;
  }
}
