package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.annotation.AccessType;
import org.springframework.data.annotation.AccessType.Type;
import org.springframework.util.ObjectUtils;

@Data
@EqualsAndHashCode(callSuper = true)
public abstract class AbstractSportEntity extends SortableEntity
    implements PageRelatedEntity, HasBrand {
  protected static final String TITLE_PATTERN = "^[^%^*{}<>\\[\\]]*$";
  public static final String SPORT_HOME_PAGE = "0";

  @Brand protected String brand;
  private String pageId;
  private PageType pageType = PageType.sport;
  private boolean disabled = true;

  // We need below methods for backward compatibility
  public Integer getSportId() {
    Integer sportId = null;
    if (!ObjectUtils.isEmpty(pageId)) {
      sportId = Integer.valueOf(pageId);
    }
    return sportId;
  }

  @AccessType(Type.PROPERTY)
  public void setSportId(Integer sportId) {
    if (!ObjectUtils.isEmpty(sportId)) {
      pageId = sportId.toString();
    }
  }
}
