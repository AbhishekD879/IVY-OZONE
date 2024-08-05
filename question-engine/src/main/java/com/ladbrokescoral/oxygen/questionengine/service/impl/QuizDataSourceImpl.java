package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.service.AbstractDataSource;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.util.*;

@AllArgsConstructor
@Slf4j
public class QuizDataSourceImpl extends AbstractDataSource<Quiz> {

    private final Queue<Quiz> quizCache = new PriorityQueue<>(new QuizComparator());

    @Override
    public void addAll(List<Quiz> quizList) {
        quizCache.addAll(quizList);
    }

    @Override
    public void clear() {
        quizCache.clear();
    }

    @Override
    public Quiz getPeek(){
        return quizCache.peek();
    }

    @Override
    public Quiz getPoll(){
        return quizCache.poll();
    }

    @Override
    public Boolean isEmpty(){
        return quizCache.isEmpty();
    }

    @Override
    public int size(){
        return quizCache.size();
    }

    public static class QuizComparator implements Comparator<Quiz> {

        public int compare(Quiz q1, Quiz q2) {
            if (q1.getDisplayFrom().isAfter(q2.getDisplayFrom()))
                return 1;
            else if (q1.getDisplayFrom().isBefore(q2.getDisplayFrom()))
                return -1;
            return 0;
        }
    }
}
