package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = true)
public class VirtualSportWithTracksRefs extends VirtualSport {
  private List<VirtualSportTrackRef> tracksRefs;
}
