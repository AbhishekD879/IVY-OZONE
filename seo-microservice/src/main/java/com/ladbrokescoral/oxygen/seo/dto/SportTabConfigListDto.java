package com.ladbrokescoral.oxygen.seo.dto;

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
}
