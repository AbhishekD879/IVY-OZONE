package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import java.util.List;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;

@Getter
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@EqualsAndHashCode
public class SportTabConfigListDto {

  private List<SportTabConfigDto> tabs;

  // FIXME: need rework. use lombok
  public static Builder builder(String baseTargetUri) {
    return new Builder(baseTargetUri);
  }

  // FIXME: need rework. use lombok
  public static class Builder {
    private SportTabConfigBuilder builder;

    private Builder(String baseTargetUri) {
      this.builder = new SportTabConfigBuilder(baseTargetUri);
    }

    public Builder addTab(SportTab tab) {
      builder.addTab(tab);
      return this;
    }

    public SportTabConfigListDto build() {
      return new SportTabConfigListDto(this.builder.getTabs());
    }
  }
}
