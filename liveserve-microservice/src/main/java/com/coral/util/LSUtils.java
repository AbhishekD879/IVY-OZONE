package com.coral.util;

import java.util.Arrays;
import java.util.Iterator;
import java.util.Properties;
import org.springframework.core.env.AbstractEnvironment;
import org.springframework.core.env.EnumerablePropertySource;
import org.springframework.core.env.Environment;

/** Created by ogavur on 4/21/17. */
public class LSUtils {

  private LSUtils() {
    throw new IllegalAccessError("Utility class");
  }

  public static Properties getProperties(Environment environment) {
    Properties properties = new Properties();
    for (Iterator<?> it = ((AbstractEnvironment) environment).getPropertySources().iterator();
        it.hasNext(); ) {
      Object propertySource = it.next();
      if (propertySource instanceof EnumerablePropertySource) {
        EnumerablePropertySource source = (EnumerablePropertySource) propertySource;
        Arrays.stream(source.getPropertyNames())
            .forEach(
                str -> {
                  if (!properties.containsKey(str)) {
                    properties.put(str, source.getProperty(str));
                  }
                });
      }
    }
    return properties;
  }
}
