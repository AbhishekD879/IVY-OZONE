package com.entain.oxygen.entity;

import com.egalacoral.spark.siteserver.model.Event;
import java.util.List;
import lombok.Data;

@Data
public class SSResponseBuilder {

  private String xmlns;
  private List<Event> children;
}
