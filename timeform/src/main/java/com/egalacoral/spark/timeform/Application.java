package com.egalacoral.spark.timeform;

import static org.springframework.boot.SpringApplication.run;

import com.egalacoral.spark.timeform.util.PropertyUtils;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import javax.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.core.env.Environment;
import org.springframework.scheduling.annotation.EnableScheduling;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@SpringBootApplication
@EnableCaching
@EnableScheduling
@EnableSwagger2
@EnableAspectJAutoProxy(proxyTargetClass = true)
@EnableAutoConfiguration
/**
 * Main class for timeform application.
 *
 * @author Vitalij Havryk
 */
public class Application {

  private static final Logger LOGGER = LoggerFactory.getLogger(Application.class);

  @Autowired private Environment environment;

  public static void main(String[] args) {
    ConfigurableApplicationContext run = run(Application.class, args);
  }

  @PostConstruct
  public void init() {
    Properties properties = PropertyUtils.getProperties(environment);
    Set<Map.Entry<Object, Object>> set = properties.entrySet();
    LOGGER.info("Application properties :");
    for (Map.Entry<Object, Object> object : set) {
      LOGGER.info("Application Property {}={}", object.getKey(), object.getValue());
    }
  }
}
