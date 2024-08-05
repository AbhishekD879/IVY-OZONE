package com.ladbrokescoral.oxygen.cms.api.entity;

import static java.time.format.DateTimeFormatter.ISO_DATE_TIME;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableMap;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.ObjectUtils;

@Slf4j
@Getter
@RequiredArgsConstructor(access = AccessLevel.PRIVATE)
public enum SystemConfigPropertyType {
  INPUT("input"),
  INPUT_WITH_MULTISELECT("input with multiselect"),
  IMAGE("image"),
  SVG("svg"),
  CHECKBOX("checkbox"),
  NUMBER("number"),
  TIMERANGE("timerange"),
  DATERANGE("daterange") {
    @Override
    public Object parseDefaultStructureValue(Object defaultConfigValue) {
      return ImmutableMap.of(
          "from", ISO_DATE_TIME.format(LocalDate.now().atStartOfDay()),
          "to", ISO_DATE_TIME.format(LocalDate.now().atStartOfDay().plusDays(1).minusSeconds(1)));
    }

    @Override
    public Object adaptStructureValue(Object structureValue, Object defaultConfigValue) {
      if (structureValue instanceof Map) {
        return structureValue;
      }
      return parseDefaultStructureValue(defaultConfigValue);
    }
  },
  RADIO("radio") {
    @Override
    public Object parseDefaultStructureValue(Object defaultConfigValue) {
      return SELECT.parseDefaultStructureValue(defaultConfigValue);
    }

    @Override
    public Object adaptStructureValue(Object structureValue, Object defaultConfigValue) {
      return SELECT.adaptStructureValue(structureValue, defaultConfigValue);
    }
  },
  SELECT("select") {
    @Override
    public Object parseDefaultStructureValue(Object defaultConfigValue) {
      return getFirstItemFromList(defaultConfigValue);
    }

    @Override
    public Object adaptStructureValue(Object structureValue, Object defaultConfigValue) {
      List<?> configValues = toList(defaultConfigValue);
      if (configValues.contains(structureValue)) {
        return structureValue;
      }
      return getFirstItemFromList(defaultConfigValue);
    }
  },
  MULTISELECT("multiselect") {
    @Override
    public Object parseDefaultStructureValue(Object defaultConfigValue) {
      return ImmutableList.of(getFirstItemFromList(defaultConfigValue));
    }

    @Override
    public Object adaptStructureValue(Object structureValue, Object defaultConfigValue) {
      List<?> configValues = toList(defaultConfigValue);
      List<?> structureValues = toList(structureValue);
      structureValues.retainAll(configValues);
      if (!structureValues.isEmpty()) {
        return structureValues;
      }
      return parseDefaultStructureValue(defaultConfigValue);
    }
  };

  private static final String DEFAULT_VALUE = "";

  private final String name;

  public static SystemConfigPropertyType from(String name) {
    return Arrays.stream(SystemConfigPropertyType.values())
        .filter(v -> v.getName().equalsIgnoreCase(name))
        .findAny()
        .orElseThrow(() -> new IllegalArgumentException("Invalid config type: " + name));
  }

  public Object parseDefaultStructureValue(Object defaultConfigValue) {
    return ObjectUtils.defaultIfNull(defaultConfigValue, DEFAULT_VALUE);
  }

  public Object adaptStructureValue(Object structureValue, Object defaultConfigValue) {
    return structureValue;
  }

  private static List toList(Object defaultConfigValue) {
    return Optional.ofNullable(defaultConfigValue)
        .filter(List.class::isInstance)
        .map(List.class::cast)
        .orElse(Collections.emptyList());
  }

  private static Object getFirstItemFromList(Object defaultConfigValue) {
    return toList(defaultConfigValue).stream().findAny().orElse(DEFAULT_VALUE);
  }
}
