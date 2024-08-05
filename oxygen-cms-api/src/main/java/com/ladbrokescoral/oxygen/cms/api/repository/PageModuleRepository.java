package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.dto.SportPageModuleDataItem;
import org.springframework.data.repository.PagingAndSortingRepository;

public interface PageModuleRepository
    extends PagingAndSortingRepository<SportPageModuleDataItem, String> {}
