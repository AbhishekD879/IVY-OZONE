package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QuizzesByBrandAndSourceId;
import java.time.Instant;
import java.util.List;
import org.bson.types.ObjectId;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.aggregation.Aggregation;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

public interface QuestionEngineRepository extends CustomMongoRepository<Quiz> {
  List<Quiz> findByBrandAndSourceId(String brand, String sourceId);

  Page<Quiz> findByBrandAndSourceIdAndDisplayFromIsBeforeAndActiveIsTrueOrderByDisplayFromDesc(
      String brand, String sourceId, Instant displayFrom, Pageable pageable);

  Page<Quiz>
      findByBrandAndSourceIdAndDisplayFromIsBeforeAndDisplayToIsBeforeAndActiveIsTrueOrderByDisplayFromDesc(
          String brand, String sourceId, Instant displayFrom, Instant displayTo, Pageable pageable);

  default List<QuizzesByBrandAndSourceId> findHistoryGroupedByBrandAndSourceIdAndActiveIsTrue(
      MongoTemplate mongoTemplate, String brand, int limit) {
    return mongoTemplate
        .aggregate(
            Aggregation.newAggregation(
                Quiz.class,
                Aggregation.match(new Criteria("displayFrom").lt(Instant.now())),
                Aggregation.match(new Criteria("brand").is(brand)),
                Aggregation.match(new Criteria("active").is(true)),
                Aggregation.sort(Sort.by(Sort.Direction.DESC, "displayFrom")),
                Aggregation.group("brand", "sourceId").push("$$ROOT").as("quizzes"),
                Aggregation.project("quizzes").and("quizzes").slice(limit)),
            QuizzesByBrandAndSourceId.class)
        .getMappedResults();
  }

  /**
   * Quiz has to be unique by sourceId. Same source id is allowed if you:
   * <li>update quiz with same id
   * <li>create quiz with different brands
   * <li>create not active quiz
   * <li>create quiz with different displayFrom - displayTo range (not overlapping)
   *
   * @param sourceId unique link format id
   * @param id quiz id
   * @param brand quiz brand
   * @param displayTo end date
   * @param displayFrom start date
   * @return
   */
  boolean
      existsBySourceIdAndIdIsNotAndBrandAndActiveIsTrueAndDisplayFromIsLessThanAndDisplayToIsGreaterThan(
          String sourceId, String id, String brand, Instant displayTo, Instant displayFrom);

  default List<Quiz> findByQuickLinksId(MongoTemplate mongoTemplate, String qeQuickLinkId) {
    Query query = new Query();
    query.addCriteria(Criteria.where("qeQuickLinks._id").is(new ObjectId(qeQuickLinkId)));
    return mongoTemplate.find(query, Quiz.class);
  }

  default List<Quiz> findBySplashPageId(MongoTemplate mongoTemplate, String splashPageId) {
    Query query = new Query();
    query.addCriteria(Criteria.where("splashPage._id").is(new ObjectId(splashPageId)));
    return mongoTemplate.find(query, Quiz.class);
  }

  default List<Quiz> findByEndPageId(MongoTemplate mongoTemplate, String endPageId) {
    Query query = new Query();
    query.addCriteria(Criteria.where("endPage._id").is(new ObjectId(endPageId)));
    return mongoTemplate.find(query, Quiz.class);
  }
}
