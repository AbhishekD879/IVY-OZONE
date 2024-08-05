package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import java.util.List;
import java.util.Optional;

public class AbstractService<T> implements CrudService<T> {

  protected CustomMongoRepository<T> repository;

  public AbstractService(CustomMongoRepository<T> repository) {
    this.repository = repository;
  }

  @Override
  public <S extends T> S save(S entity) {
    return repository.save(entity);
  }

  @Override
  public List<T> save(Iterable<T> entities) {
    return repository.saveAll(entities);
  }

  @Override
  public Optional<T> findOne(String id) {
    return repository.findById(id);
  }

  @Override
  public List<T> findAll() {
    return repository.findAll();
  }

  @Override
  public List<T> findByBrand(String brand) {
    return repository.findByBrand(brand);
  }

  @Override
  public void delete(String id) {
    repository.deleteById(id);
  }

  @Override
  public void delete(T entity) {
    repository.delete(entity);
  }

  @Override
  public void delete(Iterable<? extends T> entities) {
    repository.deleteAll(entities);
  }
}
