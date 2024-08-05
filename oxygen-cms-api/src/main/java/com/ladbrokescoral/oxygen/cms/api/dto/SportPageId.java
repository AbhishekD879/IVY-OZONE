package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import java.util.StringTokenizer;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import org.apache.commons.lang3.StringUtils;

@Data
@AllArgsConstructor
@Builder(toBuilder = true)
public class SportPageId {

  private final String id;
  private final PageType pageType;
  private final SportModuleType type;
  private final Integer moduleDataId;
  private final String title;

  public SportPageId(String id, PageType pageType, SportModuleType type) {
    this(id, pageType, type, 0, StringUtils.EMPTY);
  }

  public SportPageId(String id, PageType pageType, SportModuleType type, String title) {
    this(id, pageType, type, 0, title);
  }

  public SportPageId(String id, PageType pageType, SportModuleType type, Integer moduleDataId) {
    this(id, pageType, type, moduleDataId, StringUtils.EMPTY);
  }

  public static SportPageId fromSportModule(SportModule module) {
    return SportPageId.builder()
        .id(module.getPageId())
        .pageType(module.getPageType())
        .type(module.getModuleType())
        .moduleDataId(extractModuleDataId(module.getTitle()))
        .title(getRacingTitle(module))
        .build();
  }

  private static Integer extractModuleDataId(String title) {
    StringTokenizer toc = new StringTokenizer(title, "#");
    if (toc.countTokens() > 1 && toc.nextToken() != null) {
      String id = toc.nextToken();
      return id.matches("\\d+") ? Integer.parseInt(id) : 0;
    } else {
      return 0;
    }
  }

  private static String getRacingTitle(SportModule module) {
    return SportModuleType.RACING_MODULE.equals(module.getModuleType())
        ? module.getTitle()
        : StringUtils.EMPTY;
  }
}
