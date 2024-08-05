package com.coral.oxygen.middleware.util;

import java.util.Iterator;
import java.util.Properties;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.springframework.core.env.AbstractEnvironment;
import org.springframework.core.env.EnumerablePropertySource;
import org.springframework.core.env.Environment;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class PropertyUtils {

  public static Properties getProperties(Environment environment) {
    Properties properties = new Properties();
    for (Iterator<?> it = ((AbstractEnvironment) environment).getPropertySources().iterator();
        it.hasNext(); ) {
      Object propertySource = it.next();
      if (propertySource instanceof EnumerablePropertySource) {
        EnumerablePropertySource source = (EnumerablePropertySource) propertySource;
        String[] strings = source.getPropertyNames();
        for (String string : strings) {
          if (!properties.containsKey(string)) {
            properties.put(string, source.getProperty(string));
          }
        }
      }
    }
    return properties;
  }
}
