package com.oxygen.publisher.sportsfeatured.model.module.data;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.oxygen.publisher.model.OutputPrice;
import java.math.BigInteger;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "objId")
public class SurfaceBetModuleData extends EventsModuleData {
  private String title;
  private String content;
  private String contentHeader;
  private String svgId;
  private String svgBgImgPath;
  private String svgBgId;
  private BigInteger selectionId;
  private List<Long> eventIds;
  private OutputPrice oldPrice;
  private String objId;
  private Boolean displayOnDesktop;
}
