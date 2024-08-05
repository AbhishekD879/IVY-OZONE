package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.experimental.Accessors;
import org.springframework.util.ObjectUtils;

@Data
@Accessors(chain = true)
public class InPlayConfigDto implements SportPageModuleDataItem {
  private Integer sportId;
  private int maxEventCount;
  private List<InplaySportDto> homeInplaySports = new ArrayList<>();

  @Override
  public SportPageId sportPageId() {
    String id = ObjectUtils.isEmpty(sportId) ? null : String.valueOf(sportId);
    return new SportPageId(id, PageType.sport, SportModuleType.INPLAY);
  }
}
