package com.ladbrokescoral.oxygen.cms.api.service;

import static org.springframework.data.mongodb.core.FindAndModifyOptions.options;
import static org.springframework.data.mongodb.core.query.Criteria.where;
import static org.springframework.data.mongodb.core.query.Query.query;

import com.ladbrokescoral.oxygen.cms.api.entity.IndexNumber;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Service;

@Service
public class IndexNumberService {

  private static final String ID_NAME_DELIMITER = "_";
  @Autowired private MongoOperations mongo;

  public int getNextIndexNumber(String collectionName, String brand) {
    IndexNumber counter =
        mongo.findAndModify(
            query(where("_id").is(collectionName + ID_NAME_DELIMITER + brand)),
            new Update().inc("indexNumber", 1),
            options().returnNew(true).upsert(true),
            IndexNumber.class);
    return counter.getIndexNumber();
  }
}
