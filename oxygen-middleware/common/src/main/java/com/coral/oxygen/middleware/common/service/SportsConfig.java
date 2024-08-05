package com.coral.oxygen.middleware.common.service;

import com.coral.oxygen.middleware.common.exceptions.InvalidConfigurationException;
import com.google.gson.Gson;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SportsConfig {

  private SportConfigItem nullObject = new ItemBuilder("", "").build();

  private Map<String, SportConfigItem> mapByName;

  private Map<String, SportConfigItem> mapById;

  @Autowired
  public SportsConfig(@Value("${sports.config.json}") Resource sportsConfigJson, Gson gson) {
    try (InputStreamReader sportsConfigInputStream =
        new InputStreamReader(sportsConfigJson.getInputStream())) {
      Map map = gson.fromJson(sportsConfigInputStream, Map.class);
      List<SportConfigItem> all = new ArrayList<>();
      if (map.get("gaming") instanceof Map) {
        all.addAll(buildList((Map) map.get("gaming"), false));
      }
      if (map.get("racing") instanceof Map) {
        all.addAll(buildList((Map) map.get("racing"), true));
      }
      mapById =
          all.stream()
              .collect(Collectors.toMap(SportConfigItem::getId, Function.identity(), (a, b) -> a));
      mapByName =
          all.stream()
              .collect(Collectors.toMap(SportConfigItem::getKey, Function.identity(), (a, b) -> a));
    } catch (IOException e) {
      throw new InvalidConfigurationException("Error parsing sports config", e);
    }
  }

  private List<SportConfigItem> buildList(Map<String, Object> container, boolean isRacing) {
    return container.entrySet().stream()
        .filter(entry -> entry.getValue() instanceof Map)
        .map(entry -> buildItem(entry.getKey(), (Map<String, Object>) entry.getValue(), isRacing))
        .collect(Collectors.toList());
  }

  private String parseString(Object obj) {
    if (obj == null) {
      return null;
    }
    return String.valueOf(obj);
  }

  private SportConfigItem buildItem(String key, Map<String, Object> item, boolean isRacing) {
    String id = (String) item.getOrDefault("id", "");
    ItemBuilder builder = new ItemBuilder(key, id);
    builder.setRacing(isRacing);
    builder.setPath(parseString(item.get("path")));
    builder.setMultiTemplateSport(parseBoolean(item.get("isMultiTemplateSport")));

    // where this field is set to rtue in bma project?
    builder.setOutrightSport(false);

    Object value = item.get("oddsCardHeaderType");
    if (value instanceof String) {
      String strValue = (String) value;
      if (StringUtils.isNotBlank(strValue) && !"false".equalsIgnoreCase(strValue)) {
        try {
          OddsCardHeaderType oddsCardHeaderType = OddsCardHeaderType.valueOf(strValue);
          builder.setOddsCardHeaderType(oddsCardHeaderType);
        } catch (Exception e) {
          log.error("Wrong OddsCardHeaderType: " + strValue, e);
        }
      }
    }

    value = item.get("specialsTypeIds");
    if (value instanceof String) {
      String strValue = (String) value;
      if (StringUtils.isNotBlank(strValue) && !"false".equalsIgnoreCase(strValue)) {
        builder.setSpecialsTypeIds(strValue.split(","));
      }
    }

    return builder.build();
  }

  private boolean parseBoolean(Object value) {
    if (value instanceof Boolean) {
      return (Boolean) value;
    } else if (value instanceof String) {
      return Boolean.parseBoolean((String) value);
    }
    return false;
  }

  public SportConfigItem getByName(String sportName) {
    SportConfigItem result = mapByName.get(sportName);
    if (result == null) {
      result = nullObject;
    }
    return result;
  }

  public SportConfigItem getBySportId(String sportId) {
    SportConfigItem result = mapById.get(sportId);
    if (result == null) {
      result = nullObject;
    }
    return result;
  }

  public static class SportConfigItem {

    private String key;
    private String id;

    private String path;
    private boolean multiTemplateSport;
    private boolean racing;
    private boolean outrightSport;
    private OddsCardHeaderType oddsCardHeaderType;
    private Collection<String> specialsTypeIds;

    public boolean isMultiTemplateSport() {
      return multiTemplateSport;
    }

    public boolean isRacing() {
      return racing;
    }

    public boolean isOutrightSport() {
      return outrightSport;
    }

    public Collection<String> getSpecialsTypeIds() {
      return specialsTypeIds;
    }

    public OddsCardHeaderType getOddsCardHeaderType() {
      return oddsCardHeaderType;
    }

    public String getKey() {
      return key;
    }

    public String getPath() {
      return path;
    }

    public String getId() {
      return id;
    }
  }

  public static class ItemBuilder {
    private final String key;
    private final String id;
    private String path;
    private boolean multiTemplateSport;
    private boolean racing;
    private boolean outrightSport;
    private OddsCardHeaderType oddsCardHeaderType;
    private Collection<String> specialsTypeIds;

    public ItemBuilder(String key, String id) {
      this.key = key;
      this.id = id;
    }

    public SportConfigItem build() {
      SportConfigItem item = new SportConfigItem();
      item.key = key;
      item.id = id;
      item.path = path;
      item.multiTemplateSport = multiTemplateSport;
      item.racing = racing;
      item.outrightSport = outrightSport;
      item.oddsCardHeaderType = oddsCardHeaderType;
      item.specialsTypeIds = specialsTypeIds == null ? Collections.emptySet() : specialsTypeIds;
      return item;
    }

    public ItemBuilder setPath(String path) {
      this.path = path;
      return this;
    }

    public ItemBuilder setMultiTemplateSport(boolean multiTemplateSport) {
      this.multiTemplateSport = multiTemplateSport;
      return this;
    }

    public ItemBuilder setRacing(boolean racing) {
      this.racing = racing;
      return this;
    }

    public ItemBuilder setOutrightSport(boolean outrightSport) {
      this.outrightSport = outrightSport;
      return this;
    }

    public ItemBuilder setOddsCardHeaderType(OddsCardHeaderType oddsCardHeaderType) {
      this.oddsCardHeaderType = oddsCardHeaderType;
      return this;
    }

    public ItemBuilder setSpecialsTypeIds(String... ids) {
      this.specialsTypeIds = Arrays.asList(ids);
      return this;
    }
  }
}
