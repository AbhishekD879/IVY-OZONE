package com.ladbrokescoral.oxygen.cms.api.service;

import java.util.List;

public interface PageableCrudService<T> extends CrudService<T> {
  List<T> findAll(int offset, int limit);
}
