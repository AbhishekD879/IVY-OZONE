package com.coral.oxygen.middleware.featured.dto;

import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.VersionedPageKey;
import java.util.Set;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class FeaturedVersionResponse {

  private Set<VersionedPageKey> value;
}
