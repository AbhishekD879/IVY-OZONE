package com.coral.oxygen.middleware.pojos.model.cms;

import javax.validation.constraints.NotNull;
import lombok.Data;

/**
 * This FanzonePage class is for holding basic fanzone configuration details which are getting from
 * Oxygen-cms-api. Its holding pagename and brand.
 */
@Data
public class FanzonePage {
  @NotNull private String pageName;
  @NotNull private String brand;
}
