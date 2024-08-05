package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SsoPage;
import java.util.List;

public interface SsoPageExtendedRepository {

  List<SsoPage> findSsoPages(String brand, String osType);
}
