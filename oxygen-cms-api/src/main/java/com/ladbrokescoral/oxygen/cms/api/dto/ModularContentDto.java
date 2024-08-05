package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor // remove to make immutable
@EqualsAndHashCode(callSuper = true)
public class ModularContentDto extends BaseModularContentDto {
  @JsonProperty("title")
  private String title;

  @JsonProperty("directiveName")
  private String directiveName;

  @JsonProperty("visible")
  private Boolean visible;

  @JsonProperty("id")
  private String id;

  @JsonProperty("url")
  private String url;

  @JsonInclude(JsonInclude.Include.NON_EMPTY)
  @JsonProperty("modules")
  private List<ModuleDto> moduleDtos;

  @JsonProperty("showTabOn")
  private String showTabOn;

  @JsonProperty("devices")
  private List<String> devices;

  private Integer hubIndex;

  private Instant displayFrom;
  private Instant displayTo;

  private Boolean bybVisble;

  @Builder(toBuilder = true)
  public ModularContentDto(
      String title,
      String directiveName,
      Boolean visible,
      String id,
      String url,
      List<ModuleDto> moduleDtos,
      String showTabOn,
      List<String> devices,
      Integer hubIndex,
      Instant displayFrom,
      Instant displayTo,
      Boolean bybVisble) {
    this.title = title;
    this.directiveName = directiveName;
    this.visible = visible;
    this.id = id;
    this.url = url;
    this.moduleDtos = moduleDtos;
    this.showTabOn = showTabOn;
    this.devices = devices;
    this.hubIndex = hubIndex;
    this.displayFrom = displayFrom;
    this.displayTo = displayTo;
    this.bybVisble = bybVisble;
  }

  public ModularContentDto addModulesItem(ModuleDto modulesItem) {
    if (this.moduleDtos == null) {
      this.moduleDtos = new ArrayList<>();
    }
    this.moduleDtos.add(modulesItem);
    return this;
  }

  public ModularContentDto addDevicesItem(String devicesItem) {
    if (this.devices == null) {
      this.devices = new ArrayList<>();
    }
    this.devices.add(devicesItem);
    return this;
  }

  public ModularContentDto copy() {
    return this.toBuilder().build();
  }
}
