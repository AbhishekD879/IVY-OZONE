package com.ladbrokescoral.oxygen.cms.api.service;

import java.util.List;
import java.util.Optional;

public interface CrudService<T> extends ApiService<T> {

  <S extends T> S save(S entity);

  List<T> save(Iterable<T> entities);

  Optional<T> findOne(String id);

  List<T> findAll();

  // FIXME: need rework.
  // we can deleteById(String id) | DB will `findById` then `deleteByentity`
  // we can delete(T entity).
  // in code, redundant usage with findOne(String id) instead of exists(String id)
  // in code, double call for findOne(String id) - controller and service
  void delete(String id);

  void delete(T entity);

  void delete(Iterable<? extends T> entities);

  default T prepareModelBeforeSave(T model) {
    return model;
  }

  /**
   * By default, works as regular create operation
   *
   * @param existingEntity - entity currently in the database
   * @param updateEntity - updated entity from request
   * @return
   */
  default T update(T existingEntity, T updateEntity) {
    prepareModelBeforeSave(updateEntity);
    return save(updateEntity);
  }
}
