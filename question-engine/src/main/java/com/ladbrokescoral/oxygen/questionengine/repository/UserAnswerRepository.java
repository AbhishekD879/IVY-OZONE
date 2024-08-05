package com.ladbrokescoral.oxygen.questionengine.repository;

import com.ladbrokescoral.oxygen.questionengine.model.UserAnswer;
import org.springframework.data.repository.CrudRepository;

public interface UserAnswerRepository extends CrudRepository<UserAnswer, UserAnswer.Id>, CustomUserAnswerRepository {

}
