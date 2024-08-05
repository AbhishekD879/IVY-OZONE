package com.gvc.oxygen.betreceipts.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.NoRepositoryBean;

@NoRepositoryBean
public interface CustomCrudRepository<T> extends CrudRepository<T, String> {}
