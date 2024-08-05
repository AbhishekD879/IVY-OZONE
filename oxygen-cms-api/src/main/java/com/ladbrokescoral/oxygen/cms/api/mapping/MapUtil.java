package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.google.common.collect.Lists;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import org.bson.types.ObjectId;
import org.mapstruct.Qualifier;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

@MapUtil.MapUtils
public class MapUtil {

  public static final Pattern NAME_FROM_PATH_PATTERN = Pattern.compile("\\W");
  public static final Pattern NAME_TO_ARRAY_PATTERN = Pattern.compile("\\W+");

  @UriSubstring
  public String toDtoUri(String entity) {
    return !StringUtils.isEmpty(entity) ? cutPublicPrefix(entity) : "";
  }

  private String cutPublicPrefix(String entity) {
    return entity.startsWith("public") ? entity.substring(6) : entity;
  }

  @NullToEmpty
  public String toDtoString(String entity) {
    return Objects.nonNull(entity) ? entity : "";
  }

  @NullToNull
  public String toDtoStringNull(String entity) {
    return !StringUtils.isEmpty(entity) ? entity : null;
  }

  @StringToList
  public List<String> stringToList(String typeIds) {
    return !StringUtils.isEmpty(typeIds)
        ? Lists.newArrayList(typeIds.split(","))
        : new ArrayList<>();
  }

  @ObjectIdListToStringList
  public List<String> stringToList(List<ObjectId> objectIds) {
    return Optional.ofNullable(objectIds)
        .map(ids -> ids.stream().map(ObjectId::toString).collect(Collectors.toList()))
        .orElseGet(Collections::emptyList);
  }

  @ShowTo
  public List<String> toDtoShowTo(String value) {
    List<String> result = new ArrayList<>();
    if (Objects.isNull(value)) {
      return result;
    }
    return value.equals("both") ? Arrays.asList("new", "existing") : Arrays.asList(value);
  }

  @EmptyList
  public <T> List<T> toList(List<T> entity) {
    return !CollectionUtils.isEmpty(entity) ? entity : new ArrayList<>();
  }

  /**
   * @param uri "/sport/ice-hockey"
   * @return "ice-hockey"
   */
  @PathFromUri
  public static String pathFromUri(String uri) {
    if (uri == null) {
      return "";
    }
    String name = org.apache.commons.lang3.StringUtils.substringAfterLast(uri, "/");
    return org.apache.commons.lang3.StringUtils.isEmpty(name) ? uri : name;
  }

  @NameFromUri
  public static String nameFromUri(String uri) {
    return nameFromPath(pathFromUri(uri));
  }

  @NameFromPath
  public static String nameFromPath(String path) {
    return NAME_FROM_PATH_PATTERN.matcher(path).replaceAll("");
  }

  @NamesToArray
  public static String[] namesToArray(String names) {
    return NAME_TO_ARRAY_PATTERN.split(names, 0);
  }

  @Qualifier
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.CLASS)
  @interface MapUtils {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface UriSubstring {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface NullToEmpty {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface NullToNull {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface StringToList {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface ShowTo {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface EmptyList {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface ObjectIdListToStringList {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface PathFromUri {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface NameFromPath {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface NamesToArray {}

  @Qualifier
  @Target(ElementType.METHOD)
  @Retention(RetentionPolicy.CLASS)
  @interface NameFromUri {}
}
