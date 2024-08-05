package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.MyStable;
import com.ladbrokescoral.oxygen.cms.api.repository.MyStableRepository;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class MyStableService extends SortableService<MyStable> {
  private final MyStableRepository myStableRepository;

  @Autowired
  public MyStableService(MyStableRepository myStableRepository) {
    super(myStableRepository);
    this.myStableRepository = myStableRepository;
  }

  public Optional<MyStable> findByIds(String id) {
    return myStableRepository.findById(id);
  }

  @Override
  public List<MyStable> findByBrand(String brand) {

    return myStableRepository.findByBrand(brand);
  }

  public MyStable getByBrand(String brand) {

    return myStableRepository.getByBrand(brand);
  }
}
