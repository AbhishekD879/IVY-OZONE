package com.gvc.oxygen.betreceipts.repository;

import com.gvc.oxygen.betreceipts.dto.MetaEvent;
import java.util.List;

public interface MetaEventRepository extends CustomCrudRepository<MetaEvent> {

  List<MetaEvent> findAll();
}
