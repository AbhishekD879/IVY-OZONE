package com.coral.oxygen.middleware.featured.configuration;

import com.coral.oxygen.middleware.pojos.model.output.featured.CloudFlareFeatureModel;
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentedFeaturedModel;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.fasterxml.jackson.databind.ser.FilterProvider;
import com.fasterxml.jackson.databind.ser.impl.SimpleBeanPropertyFilter;
import com.fasterxml.jackson.databind.ser.impl.SimpleFilterProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ObjectMapperConfig {
  @Bean
  public ObjectMapper objectMapper() {
    ObjectMapper objectMapper = new ObjectMapper();
    objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
    objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    return objectMapper;
  }

  @Bean
  public ObjectWriter objectWriter() {
    ObjectMapper objectMapper = new ObjectMapper();
    objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
    objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

    objectMapper.addMixIn(Object.class, CloudFlareFeatureModel.class);
    objectMapper.addMixIn(Object.class, SegmentedFeaturedModel.class);

    String[] ignorableFieldNames = {
      "primaryMarkets", "segmentReferences", "moduleType", "featureStructureChanged", "moduleIds"
    };
    FilterProvider filters =
        new SimpleFilterProvider()
            .addFilter(
                "cloudFlareFeatureModel",
                SimpleBeanPropertyFilter.serializeAllExcept(ignorableFieldNames))
            .addFilter(
                "segmentedFeaturedModel",
                SimpleBeanPropertyFilter.serializeAllExcept(ignorableFieldNames));
    return objectMapper.writer(filters);
  }
}
