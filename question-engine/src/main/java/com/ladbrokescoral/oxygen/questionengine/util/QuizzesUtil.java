package com.ladbrokescoral.oxygen.questionengine.util;

import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import lombok.experimental.UtilityClass;

import java.time.Instant;

@UtilityClass
public class QuizzesUtil {

    public static boolean isLiveAndFutureQuizzes(Quiz quiz){
        return quiz.getDisplayTo().isAfter(Instant.now()) || quiz.getDisplayTo().equals(Instant.now());
    }

    public static boolean isLiveQuiz(Quiz quiz){
        return (null != quiz && quiz.getDisplayFrom().isBefore(Instant.now()) && quiz.getDisplayTo().isAfter(Instant.now()));
    }

}
