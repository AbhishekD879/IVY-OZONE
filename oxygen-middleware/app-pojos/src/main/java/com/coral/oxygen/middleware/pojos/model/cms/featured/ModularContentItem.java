package com.coral.oxygen.middleware.pojos.model.cms.featured;

import com.coral.oxygen.middleware.pojos.model.cms.Module;
import java.util.LinkedList;
import java.util.List;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ModularContentItem extends SportPageModuleDataItem {

  private String directiveName;

  private List<Module> modules = new LinkedList<>();

  private String showTabOn;

  private String title;

  private boolean visible;

  private List<Long> enhMultiplesIds;

  private List<Long> eventsIds;

  private List<Long> outcomesIds;

  private List<Long> racingEventsIds;

  private List<Long> typeIds;

  private List<Long> marketIds;
}
