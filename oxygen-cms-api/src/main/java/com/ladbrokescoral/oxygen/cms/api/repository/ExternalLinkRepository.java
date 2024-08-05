package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.ExternalLink;
import java.util.List;

public interface ExternalLinkRepository extends CustomMongoRepository<ExternalLink> {

  List<ExternalLink> findAllByUrl(String url);

  List<ExternalLink> findAllByUrlAndBrand(String url, String brand);
}
