package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QEQuickLinks;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.repository.QEQuickLinksRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository;
import java.util.List;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;

@Service
public class QEQuickLinksService extends AbstractService<QEQuickLinks> {

  private final QuestionEngineRepository questionEngineRepository;
  private final MongoTemplate mongoTemplate;

  public QEQuickLinksService(
      QEQuickLinksRepository repository,
      QuestionEngineRepository questionEngineRepository,
      MongoTemplate mongoTemplate) {
    super(repository);
    this.questionEngineRepository = questionEngineRepository;
    this.mongoTemplate = mongoTemplate;
  }

  public void updateQuizzesQuickLinks(QEQuickLinks qeQuickLinks) {
    List<Quiz> quizzesByQeQuickLinksId =
        questionEngineRepository.findByQuickLinksId(mongoTemplate, qeQuickLinks.getId());
    quizzesByQeQuickLinksId.forEach(
        quiz -> {
          quiz.setQeQuickLinks(qeQuickLinks);
          questionEngineRepository.save(quiz);
        });
  }

  public void deleteQuizzesQuickLinks(String id) {
    questionEngineRepository
        .findByQuickLinksId(mongoTemplate, id)
        .forEach(quiz -> questionEngineRepository.save(quiz.setQeQuickLinks(null)));
  }
}
