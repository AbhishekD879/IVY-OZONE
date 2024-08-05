package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import java.util.ArrayList;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@AllArgsConstructor
@EqualsAndHashCode
@JsonPropertyOrder({"sportConfig", "tabs"})
public class SportPageConfigDto {

  @JsonProperty("config")
  private SportConfigDto sportConfig;

  private List<SportTabConfigDto> tabs;

  // FIXME: need rework. use lombok
  public static ConfigBuilder builder() {
    return new ConfigBuilder();
  }

  // FIXME: need rework. use lombok
  @NoArgsConstructor
  public static class ConfigBuilder {

    private SportCategory sportCategory;
    private SportConfigDto sportConfig;
    private List<SportTabConfigDto> tabs;

    public TabBuilder config(SportCategory sportCategory) {
      this.sportCategory = sportCategory;
      this.sportConfig = SportConfigDto.builder().config(sportCategory).build();
      this.tabs = new ArrayList<>();
      return new TabBuilder(this);
    }

    public ConfigBuilder tabs(List<SportTabConfigDto> tabs) {
      this.tabs = tabs;
      return this;
    }

    public SportPageConfigDto build() {
      return new SportPageConfigDto(sportConfig, tabs);
    }
  }

  public static class TabBuilder extends ConfigBuilder {

    private final ConfigBuilder parentBuilder;
    private SportTabConfigBuilder builder;

    private TabBuilder(ConfigBuilder parentBuilder) {
      this.parentBuilder = parentBuilder;
      this.builder = new SportTabConfigBuilder(parentBuilder.sportCategory.getTargetUri());
    }

    public TabBuilder addTab(SportTab tab) {
      builder.addTab(tab);
      return this;
    }

    public TabBuilder addSubTab(String tabName) {
      builder.addSubTab(tabName);
      return this;
    }

    @Override
    public SportPageConfigDto build() {
      return parentBuilder.tabs(this.builder.getTabs()).build();
    }
  }
}
