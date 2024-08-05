package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.BankingMenuExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Repository
public class BankingMenuExtendedRepositoryImpl implements BankingMenuExtendedRepository {

  private MongoTemplate mongoTemplate;

  @Autowired
  public BankingMenuExtendedRepositoryImpl(MongoTemplate mongoTemplate) {
    this.mongoTemplate = mongoTemplate;
  }

  @Override
  public List<BankingMenu> findMenus(String brand) {

    Query query = new Query();
    query.addCriteria(
        Criteria.where("disabled")
            .is(false)
            .orOperator(
                Criteria.where("brand").in("retail", "connect"),
                Criteria.where("showItemFor").ne("loggedOut"))
            .and("brand")
            .is(brand));
    query.with(SortableService.SORT_BY_SORT_ORDER_ASC);

    return mongoTemplate.find(query, BankingMenu.class);
  }
}
