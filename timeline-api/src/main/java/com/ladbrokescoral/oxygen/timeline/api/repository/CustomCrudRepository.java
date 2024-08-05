package com.ladbrokescoral.oxygen.timeline.api.repository;

import org.springframework.data.repository.NoRepositoryBean;
import org.springframework.data.repository.PagingAndSortingRepository;

@NoRepositoryBean
public interface CustomCrudRepository<T> extends PagingAndSortingRepository<T, String> {}
