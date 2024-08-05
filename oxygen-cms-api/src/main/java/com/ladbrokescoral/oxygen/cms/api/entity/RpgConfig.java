package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.annotation.Nullable;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;
import lombok.Data;
import org.hibernate.validator.constraints.Range;
import org.hibernate.validator.constraints.URL;

@Data
public class RpgConfig {

  private static final String URL_PATTERN = "^(https?)://\\w[\\w\\./-]+[\\w\\.\\s\\?=&-]*$";
  private static final String INVALID_URL_MESSAGE = "not valid URL";

  @Pattern(regexp = "^[\\w\\s\\(\\)]+$", message = "try to use only alpha-numeric and spaces")
  private String title;

  @Nullable
  @Size(max = 256)
  @URL(regexp = URL_PATTERN, message = INVALID_URL_MESSAGE)
  private String bundleUrl;

  /** to specify XBC url */
  @Nullable
  @Size(max = 256)
  @URL(regexp = URL_PATTERN, message = INVALID_URL_MESSAGE)
  private String loaderUrl;

  @Size(max = 256)
  @URL(regexp = URL_PATTERN, message = INVALID_URL_MESSAGE)
  private String seeMoreLink;

  @Range(min = 0, max = 100)
  private int gamesAmount;
}
