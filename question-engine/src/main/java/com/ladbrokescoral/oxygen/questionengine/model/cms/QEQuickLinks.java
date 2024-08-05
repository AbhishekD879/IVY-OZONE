package com.ladbrokescoral.oxygen.questionengine.model.cms;

import lombok.Data;

import java.util.List;

@Data
public class QEQuickLinks {
  private String title;
  private List<QELink> links;
}
