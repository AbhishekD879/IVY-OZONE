package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.service.impl.CachePurgeService;
import java.io.InputStream;

public interface BrandCacheService extends CachePurgeService {

  boolean uploadFile(String relativePath, String fileName, InputStream fileStream);

  boolean uploadJSON(String relativePath, String fileName, String json);

  boolean deleteFile(String relativePathAndName);
}
