package com.ladbrokescoral.oxygen.questionengine.dto.cms;

import com.ladbrokescoral.oxygen.questionengine.model.cms.QELink;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.List;

@Data
@Accessors(chain = true)
public class QEQuickLinksDto {
  private String title;
  private List<QELink> links;

}
